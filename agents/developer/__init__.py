"""
Senior Developer AI Blueprint Registration
Flask blueprint for Senior Developer AI
"""

from flask import Blueprint
from .api.routes import developer_routes
from .api.socket import developer_socket


def create_developer_blueprint():
    """Create and configure the Senior Developer AI blueprint"""

    bp = Blueprint(
        "developer",
        __name__,
        url_prefix="/ai/agents/developer",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(developer_routes)

    # Register WebSocket handlers
    developer_socket.init_app(bp)

    return bp


# Export the blueprint
developer_bp = create_developer_blueprint()
