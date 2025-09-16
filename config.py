import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or '3in1_portfolio'
    
    # Redis
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_DB = int(os.environ.get('REDIS_DB') or 0)
    
    # JWT Authentication
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Passage Authentication
    PASSAGE_APP_ID = os.environ.get('PASSAGE_APP_ID') or ''
    PASSAGE_API_KEY = os.environ.get('PASSAGE_API_KEY') or ''
    
    # Payments
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY') or ''
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or ''
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID') or ''
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET') or ''
    
    # AI Models
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL') or 'http://localhost:11434'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or ''
    
    # File Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'contact@axeyaxe.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'contact@axeyaxe.com'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    MYSQL_HOST = 'localhost'
    REDIS_HOST = 'localhost'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MYSQL_DB = 'test_3in1_portfolio'

# Config mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}