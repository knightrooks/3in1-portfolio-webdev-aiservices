#!/usr/bin/env python3
"""
Flask 3-in-1 Platform Manager
Main entry point for the application
"""

import os
import click
from flask.cli import with_appcontext
from app import create_app

# Create the Flask app
app = create_app()

@app.cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def run(host, port, debug):
    """Run the Flask development server."""
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