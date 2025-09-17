# Production Configuration Class
import os
from datetime import timedelta
from urllib.parse import urlparse


class ProductionConfig:
    """Production configuration settings"""
    
    # Flask Core Settings
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
    
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set in production")
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_timeout': 30,
        'max_overflow': 20
    }
    
    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    
    # Session Configuration
    SESSION_TYPE = 'redis'
    SESSION_REDIS = REDIS_URL
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'portfolio:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Security Settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_SSL_STRICT = True
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', REDIS_URL + '/1')
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    
    # Payment Gateway Configuration
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
    PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'live')  # 'live' or 'sandbox'
    
    # AI Service Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Application URLs
    DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'yourdomain.com')
    BASE_URL = f"https://{DOMAIN_NAME}"
    
    # Celery Configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
    CELERY_TASK_ROUTES = {
        'app.tasks.ai.*': {'queue': 'ai_processing'},
        'app.tasks.email.*': {'queue': 'email'},
        'app.tasks.analytics.*': {'queue': 'analytics'}
    }
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Monitoring Configuration
    PROMETHEUS_METRICS = True
    HEALTH_CHECK_ENABLED = True
    
    # CORS Settings
    CORS_ORIGINS = [
        f"https://{DOMAIN_NAME}",
        f"https://www.{DOMAIN_NAME}"
    ]
    
    # SocketIO Configuration
    SOCKETIO_CORS_ALLOWED_ORIGINS = CORS_ORIGINS
    SOCKETIO_ASYNC_MODE = 'gevent'
    
    # Security Headers
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://js.stripe.com https://www.paypal.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.stripe.com wss://; "
            "frame-src https://js.stripe.com https://www.paypal.com;"
        )
    }
    
    # Cache Settings
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = REDIS_URL + '/2'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'portfolio_cache:'
    
    # AI Agent Configuration
    AI_AGENT_TIMEOUT = 30  # seconds
    AI_AGENT_MAX_RETRIES = 3
    AI_AGENT_RATE_LIMIT = 60  # requests per minute per user
    
    # Database Migration Settings
    MIGRATE_REPO = 'migrations'
    
    # Backup Configuration
    BACKUP_SCHEDULE = os.getenv('BACKUP_SCHEDULE', '0 2 * * *')  # Daily at 2 AM
    BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', 30))
    BACKUP_S3_BUCKET = os.getenv('BACKUP_S3_BUCKET')
    
    # Performance Settings
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=365)
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # WebSocket Settings
    WEBSOCKET_TIMEOUT = 60
    WEBSOCKET_HEARTBEAT = 25
    
    @staticmethod
    def init_app(app):
        """Initialize production configuration"""
        # Set up logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = RotatingFileHandler(
            ProductionConfig.LOG_FILE,
            maxBytes=ProductionConfig.LOG_MAX_BYTES,
            backupCount=ProductionConfig.LOG_BACKUP_COUNT
        )
        
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, ProductionConfig.LOG_LEVEL))
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, ProductionConfig.LOG_LEVEL))
        app.logger.info('Portfolio Platform production startup')
        
        # Security headers middleware
        @app.after_request
        def add_security_headers(response):
            for header, value in ProductionConfig.SECURITY_HEADERS.items():
                response.headers[header] = value
            return response
        
        # Health check registration
        from app.routes.health import health_bp
        app.register_blueprint(health_bp)
        
        return app


class StagingConfig(ProductionConfig):
    """Staging environment configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Less strict security for staging
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_SSL_STRICT = False
    
    # PayPal sandbox mode
    PAYPAL_MODE = 'sandbox'
    
    # Different domain
    DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'staging.yourdomain.com')
    BASE_URL = f"https://{DOMAIN_NAME}"
    
    # More verbose logging
    LOG_LEVEL = 'DEBUG'
    
    @staticmethod
    def init_app(app):
        ProductionConfig.init_app(app)
        
        # Additional staging-specific initialization
        app.logger.info('Portfolio Platform staging environment startup')
        
        return app


class DockerConfig(ProductionConfig):
    """Docker-specific configuration"""
    
    # Docker-specific database URL format
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        # Docker-specific health checks
        import docker
        
        @app.route('/health/docker')
        def docker_health():
            try:
                client = docker.from_env()
                containers = client.containers.list(
                    filters={'label': 'com.docker.compose.project=portfolio'}
                )
                
                healthy_containers = [
                    c for c in containers 
                    if c.status == 'running'
                ]
                
                return {
                    'status': 'healthy' if len(healthy_containers) == len(containers) else 'degraded',
                    'total_containers': len(containers),
                    'healthy_containers': len(healthy_containers),
                    'timestamp': app.config.get('current_time', 'unknown')
                }
            except Exception as e:
                return {'status': 'error', 'error': str(e)}, 500
        
        return app


# Configuration dictionary
config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'docker': DockerConfig,
    'default': ProductionConfig
}