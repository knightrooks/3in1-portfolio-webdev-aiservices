"""
Virtual Girlfriend Agent Blueprint
Flask blueprint for the sweet, caring, and emotionally supportive ai companion who provides comfort and understanding
"""

from flask import Blueprint
from flask_socketio import Namespace

# Create blueprint
girlfriend_bp = Blueprint('girlfriend', __name__, url_prefix='/girlfriend')

# Import routes after blueprint creation to avoid circular imports
from .api import routes, socket, events

# Register WebSocket namespace
class GirlfriendNamespace(Namespace):
    def on_connect(self):
        print(f'{self.__class__.__name__} client connected')
    
    def on_disconnect(self):
        print(f'{self.__class__.__name__} client disconnected')

# Export namespace for SocketIO registration
namespace = GirlfriendNamespace(f'/girlfriend')
