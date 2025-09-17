from flask import Flask, render_template, jsonify
from config import config
import os
import time

def create_app(config_name=None):
    """Application factory pattern for 3-in-1 Portfolio WebDev AI Services."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    app.config['START_TIME'] = time.time()  # For health checks
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints for all 4 core service areas
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register global context processors
    register_context_processors(app)
    
    return app
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def init_extensions(app):
    """Initialize Flask extensions."""
    # Initialize any extensions here (database, login manager, etc.)
    # SocketIO and other extensions can be added here when needed
    pass

def register_blueprints(app):
    """Register Flask blueprints for all 4 core service areas."""
    # Core application routes
    from app.routes.home import home_bp
    from app.routes.contact import contact_bp
    from app.routes.legal import legal_bp
    
    # 1. AGENTS - AI Services (16 agents)
    from app.routes.agents import agents_bp
    
    # 2. WEBDEV - Web Development Services
    from app.routes.webdev import webdev_bp
    
    # 3. PORTFOLIO - Portfolio & Showcase
    from app.routes.portfolio import portfolio_bp
    
    # 4. MODELS - AI Model Management
    from app.routes.models import models_bp
    
    # Additional service routes
    from app.routes.analytics import analytics_bp
    
    # Register core application blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(contact_bp, url_prefix='/contact')
    app.register_blueprint(legal_bp, url_prefix='/legal')
    
    # Register 4 main service area blueprints
    app.register_blueprint(agents_bp, url_prefix='/agents')      # AI Services - 16 agents
    app.register_blueprint(webdev_bp, url_prefix='/webdev')      # Web Development Services  
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio') # Portfolio & Showcase
    app.register_blueprint(models_bp, url_prefix='/models')      # AI Model Management
    
    # Register additional services
    app.register_blueprint(analytics_bp, url_prefix='/analytics')

def register_context_processors(app):
    """Register global template context processors."""
    @app.context_processor
    def inject_global_vars():
        return {
            'current_year': time.strftime('%Y'),
            'app_name': '3-in-1 Portfolio WebDev AI Services',
            'service_areas': [
                {'name': 'AI Agents', 'url': '/agents', 'icon': '🤖'},
                {'name': 'Web Development', 'url': '/webdev', 'icon': '🌐'},
                {'name': 'Portfolio', 'url': '/portfolio', 'icon': '💼'},
                {'name': 'AI Models', 'url': '/models', 'icon': '🧠'}
            ]
        }

def register_error_handlers(app):
    """Register error handlers."""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500