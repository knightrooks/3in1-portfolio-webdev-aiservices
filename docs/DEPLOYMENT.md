# Deployment Guide

This guide covers deploying the 3-in-1 Portfolio Platform to various environments, from development to production.

## Table of Contents

- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [SSL Configuration](#ssl-configuration)
- [Monitoring Setup](#monitoring-setup)

---

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+ or SQLite
- Redis 6+
- Git

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/3in1-portfolio-webdev-aiservices.git
cd 3in1-portfolio-webdev-aiservices
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database Setup**
```bash
# Initialize database
python manage.py db init
python manage.py db migrate -m "Initial migration"
python manage.py db upgrade

# Optional: Load sample data
python manage.py seed
```

6. **Start Development Server**
```bash
python manage.py run --debug
```

Access the application at `http://localhost:5000`

### Development with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Run database migrations
docker-compose exec app python manage.py db upgrade

# Stop services
docker-compose down
```

---

## Production Deployment

### Server Requirements

**Minimum Requirements:**
- 2 CPU cores
- 4GB RAM
- 20GB storage
- Ubuntu 20.04+ / CentOS 8+

**Recommended for Production:**
- 4+ CPU cores
- 8GB+ RAM
- 50GB+ SSD storage
- Load balancer for high availability

### Manual Production Setup

1. **System Dependencies**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx postgresql redis-server

# CentOS/RHEL
sudo yum update
sudo yum install -y python3 python3-pip nginx postgresql-server redis
```

2. **Create Application User**
```bash
sudo useradd --system --shell /bin/bash --home /opt/portfolio portfolio
sudo mkdir -p /opt/portfolio
sudo chown portfolio:portfolio /opt/portfolio
```

3. **Deploy Application**
```bash
sudo -u portfolio git clone https://github.com/yourusername/3in1-portfolio-webdev-aiservices.git /opt/portfolio/app
cd /opt/portfolio/app

sudo -u portfolio python3 -m venv venv
sudo -u portfolio ./venv/bin/pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
sudo -u portfolio cp .env.example .env
sudo -u portfolio nano .env
# Configure production settings
```

5. **Database Setup**
```bash
# PostgreSQL setup
sudo -u postgres createuser portfolio
sudo -u postgres createdb portfolio_production -O portfolio
sudo -u postgres psql -c "ALTER USER portfolio PASSWORD 'secure_password';"

# Run migrations
sudo -u portfolio ./venv/bin/python manage.py db upgrade
```

6. **Gunicorn Configuration**
```bash
# Create gunicorn config
sudo -u portfolio cat > /opt/portfolio/app/gunicorn.conf.py << 'EOF'
import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 300
keepalive = 2
preload_app = True
EOF
```

7. **Systemd Service**
```bash
sudo cat > /etc/systemd/system/portfolio.service << 'EOF'
[Unit]
Description=Portfolio Flask Application
After=network.target

[Service]
User=portfolio
Group=portfolio
WorkingDirectory=/opt/portfolio/app
Environment="PATH=/opt/portfolio/app/venv/bin"
ExecStart=/opt/portfolio/app/venv/bin/gunicorn --config gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable portfolio
sudo systemctl start portfolio
```

8. **Nginx Configuration**
```bash
sudo cat > /etc/nginx/sites-available/portfolio << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/private.key;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    # Static files
    location /static {
        alias /opt/portfolio/app/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Docker Deployment

### Production Docker Setup

1. **Create Docker Compose for Production**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build: 
      context: .
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://portfolio:${DB_PASSWORD}@postgres:5432/portfolio_production
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - static_files:/app/app/static
      - ./logs:/app/logs
    networks:
      - portfolio_network

  postgres:
    image: postgres:13
    restart: unless-stopped
    environment:
      POSTGRES_DB: portfolio_production
      POSTGRES_USER: portfolio
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - portfolio_network

  redis:
    image: redis:6-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - portfolio_network

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - static_files:/var/www/static
    depends_on:
      - app
    networks:
      - portfolio_network

volumes:
  postgres_data:
  redis_data:
  static_files:

networks:
  portfolio_network:
    driver: bridge
```

2. **Production Dockerfile**
```dockerfile
# Dockerfile.prod
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

# Run gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
```

3. **Deploy with Docker**
```bash
# Set environment variables
echo "DB_PASSWORD=secure_password_here" > .env.prod

# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec app python manage.py db upgrade

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Cloud Deployment

### AWS Deployment

#### Using AWS ECS (Elastic Container Service)

1. **Build and Push to ECR**
```bash
# Create ECR repository
aws ecr create-repository --repository-name portfolio-app

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -f Dockerfile.prod -t portfolio-app .
docker tag portfolio-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/portfolio-app:latest

# Push image
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/portfolio-app:latest
```

2. **ECS Task Definition**
```json
{
  "family": "portfolio-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "portfolio-app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/portfolio-app:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "FLASK_ENV", "value": "production"},
        {"name": "DATABASE_URL", "value": "postgresql://user:pass@rds-endpoint:5432/db"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/portfolio-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Using AWS Elastic Beanstalk

1. **Prepare for Deployment**
```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
eb init

# Create environment
eb create portfolio-production

# Deploy application
eb deploy
```

2. **Configuration File**
```yaml
# .ebextensions/01_flask.config
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
    DATABASE_URL: postgresql://user:pass@rds-endpoint:5432/db
```

### Google Cloud Platform (GCP)

#### Using Google Cloud Run

1. **Build and Deploy**
```bash
# Build image
docker build -f Dockerfile.prod -t gcr.io/PROJECT-ID/portfolio-app .

# Push to Container Registry
docker push gcr.io/PROJECT-ID/portfolio-app

# Deploy to Cloud Run
gcloud run deploy portfolio-app \
  --image gcr.io/PROJECT-ID/portfolio-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,DATABASE_URL=postgresql://...
```

2. **Cloud SQL Setup**
```bash
# Create PostgreSQL instance
gcloud sql instances create portfolio-db \
  --database-version POSTGRES_13 \
  --tier db-f1-micro \
  --region us-central1

# Create database
gcloud sql databases create portfolio_production --instance portfolio-db

# Create user
gcloud sql users create portfolio --instance portfolio-db --password secure_password
```

### DigitalOcean App Platform

1. **App Spec Configuration**
```yaml
# .do/app.yaml
name: portfolio-app
services:
- name: web
  source_dir: /
  dockerfile_path: Dockerfile.prod
  instance_count: 1
  instance_size_slug: basic-xxs
  environment_slug: python
  env:
  - key: FLASK_ENV
    value: production
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
  http_port: 5000

databases:
- engine: PG
  name: db
  num_nodes: 1
  size: db-s-dev-database
  version: "13"
```

2. **Deploy**
```bash
# Install doctl
# Link: https://docs.digitalocean.com/reference/doctl/how-to/install/

# Deploy app
doctl apps create --spec .do/app.yaml
```

---

## Environment Variables

### Required Variables

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@host:5432/database
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Redis (for sessions and caching)
REDIS_URL=redis://host:6379/0

# Payment Gateways
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=live  # or 'sandbox' for testing

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourdomain.com

# AI Services (Optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_HOST=http://localhost:11434

# Security
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 hours in seconds
```

### Optional Variables

```bash
# Analytics
GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
HOTJAR_ID=1234567

# Social Media
FACEBOOK_URL=https://facebook.com/yourpage
TWITTER_URL=https://twitter.com/youraccount
LINKEDIN_URL=https://linkedin.com/in/yourprofile
GITHUB_URL=https://github.com/yourusername

# Performance
WEB_CONCURRENCY=4  # Number of Gunicorn workers
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=https://your-sentry-dsn
```

---

## Database Setup

### PostgreSQL Production Setup

1. **Install PostgreSQL**
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
```

2. **Configure PostgreSQL**
```bash
# Edit postgresql.conf
sudo nano /etc/postgresql/13/main/postgresql.conf

# Key settings:
# listen_addresses = '*'
# max_connections = 100
# shared_buffers = 256MB
# effective_cache_size = 1GB
```

3. **Setup Database and User**
```sql
-- Connect as postgres user
sudo -u postgres psql

-- Create database and user
CREATE DATABASE portfolio_production;
CREATE USER portfolio WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE portfolio_production TO portfolio;
ALTER USER portfolio CREATEDB;

-- Exit
\q
```

4. **Backup and Restore**
```bash
# Create backup
pg_dump -U portfolio -h localhost portfolio_production > backup.sql

# Restore backup
psql -U portfolio -h localhost portfolio_production < backup.sql
```

### MySQL/MariaDB Alternative

```bash
# Install MySQL
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Create database
mysql -u root -p
CREATE DATABASE portfolio_production;
CREATE USER 'portfolio'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON portfolio_production.* TO 'portfolio'@'localhost';
FLUSH PRIVILEGES;
```

---

## SSL Configuration

### Let's Encrypt with Certbot

1. **Install Certbot**
```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

2. **Obtain SSL Certificate**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Auto-renewal Setup**
```bash
# Test renewal
sudo certbot renew --dry-run

# Add to crontab
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Custom SSL Certificate

```nginx
# /etc/nginx/sites-available/portfolio
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_timeout 10m;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # ... rest of configuration
}
```

---

## Monitoring Setup

### Application Monitoring

1. **Health Check Endpoint**
```python
# app/routes/health.py
@bp.route('/api/health')
def health_check():
    """Health check endpoint for load balancers"""
    checks = {
        'database': check_database_connection(),
        'redis': check_redis_connection(),
        'disk_space': check_disk_space(),
        'memory': check_memory_usage()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return jsonify({
        'status': 'healthy' if all_healthy else 'unhealthy',
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code
```

2. **Logging Configuration**
```python
# config.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/portfolio.log',
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

3. **Performance Monitoring with Sentry**
```python
# app/__init__.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

if app.config.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[
            FlaskIntegration(),
            SqlalchemyIntegration()
        ],
        traces_sample_rate=0.1,
        environment=app.config.get('FLASK_ENV', 'production')
    )
```

### System Monitoring

1. **Prometheus + Grafana**
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus_data:
  grafana_data:
```

2. **Nginx Monitoring**
```nginx
# Add to nginx configuration
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

---

## Backup Strategy

### Database Backups

```bash
#!/bin/bash
# backup.sh - Daily database backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
DB_NAME="portfolio_production"
DB_USER="portfolio"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create database backup
pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Keep only last 30 days of backups
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete

# Optional: Upload to S3
# aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql.gz s3://your-backup-bucket/database/
```

### Application Backups

```bash
#!/bin/bash
# app_backup.sh - Application files backup

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
APP_DIR="/opt/portfolio/app"

# Backup uploaded files and logs
tar -czf $BACKUP_DIR/app_files_$DATE.tar.gz -C $APP_DIR uploads logs

# Keep only last 7 days of file backups
find $BACKUP_DIR -name "app_files_*.tar.gz" -mtime +7 -delete
```

---

## Troubleshooting

### Common Issues

1. **Application Won't Start**
```bash
# Check logs
sudo journalctl -u portfolio -f

# Check gunicorn process
ps aux | grep gunicorn

# Check port availability
sudo netstat -tlnp | grep :5000
```

2. **Database Connection Issues**
```bash
# Test database connection
psql -U portfolio -h localhost -d portfolio_production

# Check PostgreSQL status
sudo systemctl status postgresql

# Review PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log
```

3. **High Memory Usage**
```bash
# Monitor memory usage
htop

# Check for memory leaks in Python
pip install memory_profiler
python -m memory_profiler your_script.py
```

4. **SSL Certificate Issues**
```bash
# Check certificate validity
openssl x509 -in /path/to/cert.pem -text -noout

# Test SSL configuration
openssl s_client -connect yourdomain.com:443
```

### Performance Optimization

1. **Database Query Optimization**
```sql
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

-- Analyze slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

2. **Application Performance**
```python
# Use Flask-Caching for expensive operations
from flask_caching import Cache

cache = Cache(app)

@cache.memoize(timeout=300)
def expensive_function():
    # Expensive computation
    return result
```

3. **Static File Optimization**
```nginx
# Nginx static file caching
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary "Accept-Encoding";
    gzip_static on;
}
```

This deployment guide provides comprehensive coverage for deploying the 3-in-1 Portfolio Platform in various environments. Adjust the configurations based on your specific requirements and infrastructure setup.