"""
Business Strategist AI Blueprint Registration
Flask blueprint for Business Strategist AI
"""

from flask import Blueprint
from .api.routes import strategist_routes
from .api.socket import strategist_socket


def create_strategist_blueprint():
    """Create and configure the Business Strategist AI blueprint"""

    bp = Blueprint(
        "strategist",
        __name__,
        url_prefix="/ai/agents/strategist",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(strategist_routes)

    # Register WebSocket handlers
    strategist_socket.init_app(bp)

    return bp


# Export the blueprint
strategist_bp = create_strategist_blueprint()
