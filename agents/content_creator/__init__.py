"""
Content Creator AI Blueprint Registration
Flask blueprint for Content Creator AI
"""

from flask import Blueprint
from .api.routes import content_creator_routes
from .api.socket import content_creator_socket


def create_content_creator_blueprint():
    """Create and configure the Content Creator AI blueprint"""

    bp = Blueprint(
        "content_creator",
        __name__,
        url_prefix="/ai/agents/content_creator",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(content_creator_routes)

    # Register WebSocket handlers
    content_creator_socket.init_app(bp)

    return bp


# Export the blueprint
content_creator_bp = create_content_creator_blueprint()
