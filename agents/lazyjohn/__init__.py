"""
Lazy John Agent Blueprint
Flask blueprint for the extremely lazy but surprisingly wise ai who gives minimal effort responses with unexpected depth
"""

from flask import Blueprint
from flask_socketio import Namespace

# Create blueprint
lazyjohn_bp = Blueprint("lazyjohn", __name__, url_prefix="/lazyjohn")

# Import routes after blueprint creation to avoid circular imports
from .api import routes, socket, events


# Register WebSocket namespace
class LazyjohnNamespace(Namespace):
    def on_connect(self):
        print(f"{self.__class__.__name__} client connected")

    def on_disconnect(self):
        print(f"{self.__class__.__name__} client disconnected")


# Export namespace for SocketIO registration
namespace = LazyjohnNamespace(f"/lazyjohn")
