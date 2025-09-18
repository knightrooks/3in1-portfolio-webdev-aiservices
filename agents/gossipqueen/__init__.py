"""
Gossip Queen Agent Blueprint
Flask blueprint for the chatty, social butterfly who loves to talk about everything and everyone with infectious enthusiasm
"""

from flask import Blueprint
from flask_socketio import Namespace

# Create blueprint
gossipqueen_bp = Blueprint("gossipqueen", __name__, url_prefix="/gossipqueen")

# Import routes after blueprint creation to avoid circular imports
from .api import routes, socket, events


# Register WebSocket namespace
class GossipqueenNamespace(Namespace):
    def on_connect(self):
        print(f"{self.__class__.__name__} client connected")

    def on_disconnect(self):
        print(f"{self.__class__.__name__} client disconnected")


# Export namespace for SocketIO registration
namespace = GossipqueenNamespace(f"/gossipqueen")
