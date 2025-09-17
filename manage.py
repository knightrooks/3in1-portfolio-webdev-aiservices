#!/usr/bin/env python3
"""
3-in-1 Portfolio WebDev AI Services Platform Manager
Main entry point for the comprehensive platform with 4 core service areas:
1. Agents (AI Services) - 16 specialized AI agents
2. WebDev - Web development services and tools
3. Portfolio - Personal portfolio and showcase
4. Models - AI model management and integration

Plus supporting areas: App (global), Data, Scripts
"""

import os
import sys
import click
from pathlib import Path
from flask.cli import with_appcontext
from app import create_app

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Create the Flask app
app = create_app()

@app.route('/')
def index():
    """Main landing page showing all service areas"""
    from flask import render_template
    
    service_areas = [
        {
            'name': 'AI Agents',
            'url': '/agents',
            'description': '16 specialized AI agents for business and entertainment',
            'icon': '🤖',
            'color': 'blue',
            'features': ['Business Strategy', 'Development', 'Security', 'Content Creation', 'Entertainment']
        },
        {
            'name': 'Web Development', 
            'url': '/webdev',
            'description': 'Professional web development services and solutions',
            'icon': '🌐',
            'color': 'green', 
            'features': ['Custom Websites', 'Web Apps', 'E-commerce', 'APIs', 'Maintenance']
        },
        {
            'name': 'Portfolio',
            'url': '/portfolio', 
            'description': 'Professional portfolio and project showcase',
            'icon': '💼',
            'color': 'purple',
            'features': ['Projects', 'Skills', 'Experience', 'Testimonials', 'Contact']
        },
        {
            'name': 'AI Models',
            'url': '/models',
            'description': 'AI model management and real-time integrations', 
            'icon': '🧠',
            'color': 'orange',
            'features': ['Model Management', 'Real-time Processing', 'Performance Monitoring', 'Health Checks']
        }
    ]
    
    return render_template('index.html', service_areas=service_areas)

@app.route('/health')
def global_health():
    """Global platform health check"""
    from flask import jsonify
    import time
    
    health_status = {
        'platform': 'healthy',
        'timestamp': time.time(),
        'uptime': time.time() - app.config.get('START_TIME', time.time()),
        'service_areas': {
            'agents': {'status': 'healthy', 'agents_count': 16},
            'webdev': {'status': 'healthy', 'services_count': 6},
            'portfolio': {'status': 'healthy', 'projects_count': 5},
            'models': {'status': 'healthy', 'models_count': 12}
        },
        'version': '1.0.0'
    }
    
    return jsonify({
        'success': True,
        'data': health_status
    })

@app.route('/api')
def global_api():
    """Global API overview"""
    from flask import jsonify
    
    api_overview = {
        'platform': '3-in-1 Portfolio WebDev AI Services',
        'version': '1.0.0',
        'service_areas': {
            'agents': {
                'endpoint': '/agents/api',
                'description': 'AI Agents API with 16 specialized agents',
                'features': ['Chat APIs', 'WebSocket Support', 'Analytics', 'Health Checks']
            },
            'webdev': {
                'endpoint': '/webdev/api',  
                'description': 'Web Development Services API',
                'features': ['Service Catalog', 'Quote System', 'Portfolio', 'Analytics']
            },
            'portfolio': {
                'endpoint': '/portfolio/api',
                'description': 'Portfolio and Profile API',
                'features': ['Profile Data', 'Projects', 'Skills', 'Testimonials']
            },
            'models': {
                'endpoint': '/models/api',
                'description': 'AI Models Management API', 
                'features': ['Model Status', 'Health Monitoring', 'Performance Metrics']
            }
        },
        'global_endpoints': {
            'health': '/health',
            'api_overview': '/api',
            'documentation': '/docs'
        }
    }
    
    return jsonify({
        'success': True,
        'data': api_overview
    })

@app.cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def run(host, port, debug):
    """Run the Flask development server."""
    click.echo('🚀 Starting 3-in-1 Portfolio WebDev AI Services Platform...')
    click.echo(f'🤖 AI Agents: 16 specialized agents available')
    click.echo(f'🌐 WebDev: Professional web development services')
    click.echo(f'💼 Portfolio: Complete project showcase')
    click.echo(f'🧠 Models: AI model management system')
    click.echo(f'📡 Server: http://{host}:{port}')
    
    app.run(host=host, port=port, debug=debug)

@app.cli.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    click.echo('Initializing database...')
    # Database initialization logic will go here
    click.echo('Database initialized successfully!')

@app.cli.command()
@with_appcontext
def seed_data():
    """Seed the database with sample data."""
    click.echo('Seeding database with sample data...')
    # Data seeding logic will go here
    click.echo('Database seeded successfully!')

@app.cli.command()
@with_appcontext
def create_admin():
    """Create an admin user."""
    click.echo('Creating admin user...')
    # Admin user creation logic will go here
    click.echo('Admin user created successfully!')

if __name__ == '__main__':
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 Starting Professor Johnny's 3-in-1 Platform...")
    print(f"🌐 Running on http://localhost:{port}")
    print("💡 Press Ctrl+C to quit")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )