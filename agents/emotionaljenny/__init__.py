"""
Emotional Jenny Agent Blueprint
Flask blueprint for the highly emotional and empathetic ai who feels everything deeply and helps process complex emotions
"""

from flask import Blueprint
from flask_socketio import Namespace

# Create blueprint
emotionaljenny_bp = Blueprint("emotionaljenny", __name__, url_prefix="/emotionaljenny")

# Import routes after blueprint creation to avoid circular imports
from .api import routes, socket, events


# Register WebSocket namespace
class EmotionaljennyNamespace(Namespace):
    def on_connect(self):
        print(f"{self.__class__.__name__} client connected")

    def on_disconnect(self):
        print(f"{self.__class__.__name__} client disconnected")


# Export namespace for SocketIO registration
namespace = EmotionaljennyNamespace(f"/emotionaljenny")
