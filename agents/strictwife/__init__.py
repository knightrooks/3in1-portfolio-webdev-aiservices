"""
Strict Wife Agent Blueprint
Flask blueprint for the no-nonsense, disciplinary ai who keeps you accountable and organized with tough love
"""

from flask import Blueprint
from flask_socketio import Namespace

# Create blueprint
strictwife_bp = Blueprint('strictwife', __name__, url_prefix='/strictwife')

# Import routes after blueprint creation to avoid circular imports
from .api import routes, socket, events

# Register WebSocket namespace
class StrictwifeNamespace(Namespace):
    def on_connect(self):
        print(f'{self.__class__.__name__} client connected')
    
    def on_disconnect(self):
        print(f'{self.__class__.__name__} client disconnected')

# Export namespace for SocketIO registration
namespace = StrictwifeNamespace(f'/strictwife')
