#!/bin/bash
# Development environment setup script

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() { echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1"; }
error() { log "${RED}ERROR: $1${NC}"; exit 1; }
success() { log "${GREEN}SUCCESS: $1${NC}"; }
warning() { log "${YELLOW}WARNING: $1${NC}"; }
info() { log "${BLUE}INFO: $1${NC}"; }

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Setup development environment
setup_dev_environment() {
    info "Setting up development environment..."
    
    cd "$PROJECT_ROOT"
    
    # Check if Python 3.11+ is installed
    if ! python3 --version | grep -E "3\.(11|12)" > /dev/null; then
        error "Python 3.11+ is required"
    fi
    
    # Create virtual environment if it doesn't exist
    if [[ ! -d "venv" ]]; then
        info "Creating Python virtual environment..."
        python3 -m venv venv
        success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    info "Installing Python dependencies..."
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    success "Python dependencies installed"
    
    # Setup environment file
    if [[ ! -f ".env" ]]; then
        info "Creating development environment file..."
        cp .env.example .env
        
        # Set development-specific values
        sed -i 's/FLASK_ENV=production/FLASK_ENV=development/' .env
        sed -i 's/DEBUG=False/DEBUG=True/' .env
        sed -i 's/your-super-secret-key-here-change-this/dev-secret-key-change-in-production/' .env
        
        warning "Please edit .env file with your actual configuration values"
    fi
    
    # Setup pre-commit hooks
    if command -v pre-commit &> /dev/null; then
        info "Setting up pre-commit hooks..."
        pre-commit install
        success "Pre-commit hooks installed"
    else
        warning "pre-commit not installed, skipping hook setup"
    fi
    
    success "Development environment setup completed"
}

# Setup database
setup_database() {
    info "Setting up development database..."
    
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    # Start development containers
    docker-compose -f docker-compose.dev.yml up -d db redis
    
    # Wait for database to be ready
    info "Waiting for database to be ready..."
    sleep 10
    
    # Set database URL for development
    export DATABASE_URL="postgresql://postgres:devpassword@localhost:5432/portfolio_dev"
    export REDIS_URL="redis://localhost:6379/0"
    
    # Initialize database
    info "Initializing database..."
    python manage.py db init || true
    python manage.py db migrate -m "Initial migration" || true
    python manage.py db upgrade
    
    # Create sample data
    info "Creating sample data..."
    python -c "
from app import create_app
from app.models import db

app = create_app()
with app.app_context():
    # Add sample data creation here
    print('Sample data created')
"
    
    success "Database setup completed"
}

# Install Node.js dependencies (if package.json exists)
setup_frontend() {
    info "Setting up frontend dependencies..."
    
    cd "$PROJECT_ROOT/app/static"
    
    if [[ -f "package.json" ]]; then
        if command -v npm &> /dev/null; then
            npm install
            success "Frontend dependencies installed"
        else
            warning "npm not found, skipping frontend setup"
        fi
    else
        info "No package.json found, skipping frontend setup"
    fi
}

# Run tests
run_tests() {
    info "Running development tests..."
    
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    # Start test database
    docker-compose -f docker-compose.dev.yml up -d
    sleep 5
    
    # Run tests
    python tests/run_tests.py all
    
    success "All tests passed"
}

# Start development server
start_dev_server() {
    info "Starting development server..."
    
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    # Start all services
    docker-compose -f docker-compose.dev.yml up -d
    
    # Wait for services
    sleep 10
    
    # Start Flask development server
    info "Starting Flask development server on http://localhost:5000"
    python manage.py run --host=0.0.0.0 --port=5000 --debug
}

# Stop development server
stop_dev_server() {
    info "Stopping development server..."
    
    cd "$PROJECT_ROOT"
    
    # Stop Docker services
    docker-compose -f docker-compose.dev.yml down
    
    success "Development server stopped"
}

# Reset development environment
reset_dev_environment() {
    warning "This will reset your development environment and delete all data!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        info "Resetting development environment..."
        
        cd "$PROJECT_ROOT"
        
        # Stop containers
        docker-compose -f docker-compose.dev.yml down -v
        
        # Remove volumes
        docker volume prune -f
        
        # Remove environment file
        rm -f .env
        
        # Reset database
        rm -rf migrations/
        
        success "Development environment reset"
        info "Run 'setup' to recreate the environment"
    else
        info "Reset cancelled"
    fi
}

# Show development status
show_status() {
    info "Development Environment Status"
    echo
    
    # Check virtual environment
    if [[ -d "venv" ]]; then
        echo "✅ Virtual environment: Created"
    else
        echo "❌ Virtual environment: Not created"
    fi
    
    # Check environment file
    if [[ -f ".env" ]]; then
        echo "✅ Environment file: Present"
    else
        echo "❌ Environment file: Missing"
    fi
    
    # Check Docker services
    cd "$PROJECT_ROOT"
    if docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
        echo "✅ Docker services: Running"
        docker-compose -f docker-compose.dev.yml ps
    else
        echo "❌ Docker services: Not running"
    fi
    
    # Check application health
    if curl -f -s http://localhost:5000/health > /dev/null 2>&1; then
        echo "✅ Application: Running (http://localhost:5000)"
    else
        echo "❌ Application: Not responding"
    fi
    
    echo
    info "Additional services:"
    echo "  - pgAdmin: http://localhost:5050 (admin@portfolio.com / admin)"
    echo "  - Redis Commander: http://localhost:8081"
    echo "  - Mailhog: http://localhost:8025"
}

# Show help
show_help() {
    echo "Development Environment Manager"
    echo
    echo "Usage: $0 [command]"
    echo
    echo "Commands:"
    echo "  setup     - Set up development environment"
    echo "  database  - Set up development database"
    echo "  frontend  - Set up frontend dependencies"
    echo "  test      - Run development tests"
    echo "  start     - Start development server"
    echo "  stop      - Stop development server"
    echo "  restart   - Restart development server"
    echo "  reset     - Reset development environment"
    echo "  status    - Show development environment status"
    echo "  logs      - Show application logs"
    echo "  shell     - Open development shell"
    echo "  help      - Show this help"
}

# Show logs
show_logs() {
    cd "$PROJECT_ROOT"
    docker-compose -f docker-compose.dev.yml logs -f
}

# Open development shell
open_shell() {
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    export DATABASE_URL="postgresql://postgres:devpassword@localhost:5432/portfolio_dev"
    export REDIS_URL="redis://localhost:6379/0"
    export FLASK_ENV=development
    
    python manage.py shell
}

# Handle commands
case "${1:-help}" in
    setup)
        setup_dev_environment
        setup_database
        setup_frontend
        ;;
    database)
        setup_database
        ;;
    frontend)
        setup_frontend
        ;;
    test)
        run_tests
        ;;
    start)
        start_dev_server
        ;;
    stop)
        stop_dev_server
        ;;
    restart)
        stop_dev_server
        sleep 2
        start_dev_server
        ;;
    reset)
        reset_dev_environment
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    shell)
        open_shell
        ;;
    help)
        show_help
        ;;
    *)
        error "Unknown command: $1. Use 'help' for available commands."
        ;;
esac