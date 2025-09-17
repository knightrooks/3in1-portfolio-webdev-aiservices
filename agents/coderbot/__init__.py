"""
Coder Bot Agent Blueprint
Flask blueprint for the programming-focused ai assistant that speaks in code and technical jargon while being extremely helpful
"""

from flask import Blueprint
from flask_socketio import Namespace

# Create blueprint
coderbot_bp = Blueprint("coderbot", __name__, url_prefix="/coderbot")

# Import routes after blueprint creation to avoid circular imports
from .api import routes, socket, events


# Register WebSocket namespace
class CoderbotNamespace(Namespace):
    def on_connect(self):
        print(f"{self.__class__.__name__} client connected")

    def on_disconnect(self):
        print(f"{self.__class__.__name__} client disconnected")


# Export namespace for SocketIO registration
namespace = CoderbotNamespace(f"/coderbot")
