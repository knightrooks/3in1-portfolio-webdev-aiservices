"""
Cybersecurity Expert AI Blueprint Registration
Flask blueprint for Cybersecurity Expert AI
"""

from flask import Blueprint
from .api.routes import security_expert_routes
from .api.socket import security_expert_socket


def create_security_expert_blueprint():
    """Create and configure the Cybersecurity Expert AI blueprint"""

    bp = Blueprint(
        "security_expert",
        __name__,
        url_prefix="/ai/agents/security_expert",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(security_expert_routes)

    # Register WebSocket handlers
    security_expert_socket.init_app(bp)

    return bp


# Export the blueprint
security_expert_bp = create_security_expert_blueprint()
