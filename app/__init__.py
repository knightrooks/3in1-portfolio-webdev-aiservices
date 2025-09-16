from flask import Flask, render_template
from config import config
import os

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions (will add later)
    # init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    from app.routes.home import home_bp
    from app.routes.portfolio import portfolio_bp
    from app.routes.webdev import webdev_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(webdev_bp)

def register_error_handlers(app):
    """Register error handlers."""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500