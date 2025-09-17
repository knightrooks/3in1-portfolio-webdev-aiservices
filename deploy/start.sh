#!/bin/bash
# Production startup script for 3-in-1 Portfolio Platform

set -e

echo "Starting 3-in-1 Portfolio Platform..."

# Wait for database to be ready
echo "Waiting for database connection..."
python -c "
import time
import psycopg2
from config import Config

max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        conn = psycopg2.connect(Config.DATABASE_URL)
        conn.close()
        print('Database connection successful')
        break
    except psycopg2.OperationalError:
        attempt += 1
        print(f'Database connection attempt {attempt}/{max_attempts} failed, retrying in 2 seconds...')
        time.sleep(2)
else:
    print('Failed to connect to database after all attempts')
    exit(1)
"

# Wait for Redis to be ready
echo "Waiting for Redis connection..."
python -c "
import time
import redis
from config import Config

max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        r = redis.from_url(Config.REDIS_URL)
        r.ping()
        print('Redis connection successful')
        break
    except redis.ConnectionError:
        attempt += 1
        print(f'Redis connection attempt {attempt}/{max_attempts} failed, retrying in 2 seconds...')
        time.sleep(2)
else:
    print('Failed to connect to Redis after all attempts')
    exit(1)
"

# Run database migrations
echo "Running database migrations..."
python manage.py db upgrade

# Create necessary directories
mkdir -p logs static/uploads data/cache

# Set proper permissions
chmod 755 logs static/uploads data/cache

# Initialize application data if needed
echo "Initializing application data..."
python -c "
from app import create_app
from app.models import db

app = create_app()
with app.app_context():
    # Create any missing tables
    db.create_all()
    
    # Initialize default data if needed
    print('Application initialization complete')
"

# Start supervisor to manage processes
echo "Starting application services..."
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf -n