#!/bin/bash
# Production deployment script for 3-in-1 Portfolio Platform

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEPLOY_USER="portfolio"
DEPLOY_PATH="/opt/portfolio-production"
BACKUP_PATH="/opt/backups/portfolio"
LOG_FILE="/var/log/portfolio-deploy.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

error() {
    log "${RED}ERROR: $1${NC}"
    exit 1
}

success() {
    log "${GREEN}SUCCESS: $1${NC}"
}

warning() {
    log "${YELLOW}WARNING: $1${NC}"
}

info() {
    log "${BLUE}INFO: $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root for security reasons"
    fi
}

# Validate environment
validate_environment() {
    info "Validating deployment environment..."
    
    # Check required commands
    for cmd in docker docker-compose git curl; do
        if ! command -v "$cmd" &> /dev/null; then
            error "Required command '$cmd' is not installed"
        fi
    done
    
    # Check Docker is running
    if ! docker info &> /dev/null; then
        error "Docker is not running"
    fi
    
    # Check environment file exists
    if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
        error "Environment file .env not found. Copy .env.example and configure it."
    fi
    
    success "Environment validation passed"
}

# Create backup
create_backup() {
    info "Creating backup before deployment..."
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="$BACKUP_PATH/$backup_timestamp"
    
    # Create backup directory
    sudo mkdir -p "$backup_dir"
    
    # Backup database
    if docker-compose -f docker-compose.prod.yml exec -T db pg_dumpall -U portfolio_user > "$backup_dir/database.sql" 2>/dev/null; then
        success "Database backup created: $backup_dir/database.sql"
    else
        warning "Database backup failed or database not running"
    fi
    
    # Backup uploaded files
    if [[ -d "$DEPLOY_PATH/uploads" ]]; then
        sudo cp -r "$DEPLOY_PATH/uploads" "$backup_dir/"
        success "File uploads backup created"
    fi
    
    # Backup logs
    if [[ -d "$DEPLOY_PATH/logs" ]]; then
        sudo cp -r "$DEPLOY_PATH/logs" "$backup_dir/"
        success "Logs backup created"
    fi
    
    # Set backup permissions
    sudo chown -R "$USER:$USER" "$backup_dir"
    
    # Cleanup old backups (keep last 10)
    info "Cleaning up old backups..."
    sudo find "$BACKUP_PATH" -maxdepth 1 -type d -name "20*" | sort -r | tail -n +11 | xargs -r sudo rm -rf
    
    success "Backup completed: $backup_dir"
}

# Pull latest code
update_code() {
    info "Updating code from repository..."
    
    cd "$PROJECT_ROOT"
    
    # Stash any local changes
    if [[ -n $(git status --porcelain) ]]; then
        warning "Local changes detected, stashing them..."
        git stash push -m "Auto-stash before deployment $(date)"
    fi
    
    # Pull latest changes
    git fetch origin
    git checkout main
    git pull origin main
    
    success "Code updated successfully"
}

# Build and deploy containers
deploy_containers() {
    info "Deploying containers..."
    
    cd "$PROJECT_ROOT"
    
    # Pull latest images
    docker-compose -f docker-compose.prod.yml pull
    
    # Build application image
    docker-compose -f docker-compose.prod.yml build --no-cache app
    
    # Stop existing containers gracefully
    docker-compose -f docker-compose.prod.yml down --timeout 30
    
    # Start new containers
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for containers to be ready
    info "Waiting for containers to be ready..."
    sleep 30
    
    # Check container health
    for service in app db redis; do
        if ! docker-compose -f docker-compose.prod.yml ps "$service" | grep -q "Up"; then
            error "Service '$service' failed to start properly"
        fi
    done
    
    success "Containers deployed successfully"
}

# Run database migrations
run_migrations() {
    info "Running database migrations..."
    
    cd "$PROJECT_ROOT"
    
    # Run migrations
    docker-compose -f docker-compose.prod.yml exec -T app python manage.py db upgrade
    
    success "Database migrations completed"
}

# Verify deployment
verify_deployment() {
    info "Verifying deployment..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -f -s http://localhost:8000/health > /dev/null; then
            success "Health check passed on attempt $attempt"
            break
        else
            if [[ $attempt -eq $max_attempts ]]; then
                error "Health check failed after $max_attempts attempts"
            fi
            warning "Health check failed, attempt $attempt/$max_attempts, retrying in 10 seconds..."
            sleep 10
            ((attempt++))
        fi
    done
    
    # Test API endpoints
    info "Testing API endpoints..."
    
    local endpoints=("/api/health" "/api/portfolio" "/api/webdev/pricing")
    for endpoint in "${endpoints[@]}"; do
        if curl -f -s "http://localhost:8000$endpoint" > /dev/null; then
            success "API endpoint $endpoint is working"
        else
            warning "API endpoint $endpoint is not responding properly"
        fi
    done
    
    # Check logs for errors
    info "Checking application logs..."
    if docker-compose -f docker-compose.prod.yml logs --tail=50 app | grep -i error; then
        warning "Errors found in application logs"
    else
        success "No errors found in recent logs"
    fi
    
    success "Deployment verification completed"
}

# Cleanup Docker resources
cleanup_docker() {
    info "Cleaning up Docker resources..."
    
    # Remove unused images
    docker image prune -a -f
    
    # Remove unused volumes
    docker volume prune -f
    
    # Remove unused networks
    docker network prune -f
    
    success "Docker cleanup completed"
}

# Send notification
send_notification() {
    local status="$1"
    local message="$2"
    
    # Slack notification (if webhook URL is configured)
    if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
        local payload="{\"text\":\"🚀 Portfolio Deployment $status: $message\"}"
        curl -X POST -H 'Content-type: application/json' \
             --data "$payload" \
             "$SLACK_WEBHOOK_URL" &> /dev/null || true
    fi
    
    # Email notification (if configured)
    if command -v mail &> /dev/null && [[ -n "${ADMIN_EMAIL:-}" ]]; then
        echo "$message" | mail -s "Portfolio Deployment $status" "$ADMIN_EMAIL" || true
    fi
}

# Rollback function
rollback() {
    warning "Initiating rollback..."
    
    cd "$PROJECT_ROOT"
    
    # Stop current containers
    docker-compose -f docker-compose.prod.yml down
    
    # Find latest backup
    local latest_backup=$(sudo find "$BACKUP_PATH" -maxdepth 1 -type d -name "20*" | sort -r | head -n 1)
    
    if [[ -n "$latest_backup" ]]; then
        info "Rolling back to backup: $latest_backup"
        
        # Restore database if backup exists
        if [[ -f "$latest_backup/database.sql" ]]; then
            docker-compose -f docker-compose.prod.yml up -d db
            sleep 10
            docker-compose -f docker-compose.prod.yml exec -T db psql -U portfolio_user -d postgres -c "DROP DATABASE IF EXISTS portfolio_db;"
            docker-compose -f docker-compose.prod.yml exec -T db psql -U portfolio_user -d postgres -c "CREATE DATABASE portfolio_db;"
            docker-compose -f docker-compose.prod.yml exec -T db psql -U portfolio_user -d portfolio_db < "$latest_backup/database.sql"
        fi
        
        # Restore files
        if [[ -d "$latest_backup/uploads" ]]; then
            sudo cp -r "$latest_backup/uploads" "$DEPLOY_PATH/"
        fi
        
        # Start containers with previous image
        docker-compose -f docker-compose.prod.yml up -d
        
        success "Rollback completed"
    else
        error "No backup found for rollback"
    fi
}

# Main deployment function
main() {
    local start_time=$(date)
    
    info "Starting deployment at $start_time"
    
    # Trap for cleanup on script exit
    trap 'if [[ $? -ne 0 ]]; then error "Deployment failed, consider rollback"; send_notification "FAILED" "Deployment failed at $(date)"; fi' EXIT
    
    check_root
    validate_environment
    create_backup
    update_code
    deploy_containers
    run_migrations
    verify_deployment
    cleanup_docker
    
    local end_time=$(date)
    local success_message="Deployment completed successfully. Started: $start_time, Finished: $end_time"
    
    success "$success_message"
    send_notification "SUCCESS" "$success_message"
    
    # Remove trap on successful completion
    trap - EXIT
}

# Handle command line arguments
case "${1:-deploy}" in
    deploy)
        main
        ;;
    rollback)
        rollback
        ;;
    verify)
        verify_deployment
        ;;
    backup)
        create_backup
        ;;
    help)
        echo "Usage: $0 [deploy|rollback|verify|backup|help]"
        echo "  deploy   - Full deployment (default)"
        echo "  rollback - Rollback to previous backup"
        echo "  verify   - Verify current deployment"
        echo "  backup   - Create backup only"
        echo "  help     - Show this help"
        ;;
    *)
        error "Unknown command: $1. Use 'help' for usage information."
        ;;
esac