"""
Flask 3-in-1 Platform: Portfolio, Web Dev Services, and AI Services
Main application entry point
"""

from flask import Flask, render_template, request, jsonify
import os

# Create Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Import blueprints
from blueprints.portfolio import portfolio_bp
from blueprints.services import services_bp
from blueprints.ai_services import ai_services_bp

# Register blueprints
app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
app.register_blueprint(services_bp, url_prefix='/services')
app.register_blueprint(ai_services_bp, url_prefix='/ai')

@app.route('/')
def home():
    """Main landing page showcasing all three areas"""
    return render_template('home.html')

@app.route('/about')
def about():
    """About the platform"""
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)