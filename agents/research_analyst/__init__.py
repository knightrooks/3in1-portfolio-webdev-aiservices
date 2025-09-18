"""
Research Analyst AI Blueprint Registration
Flask blueprint for Research Analyst AI
"""

from flask import Blueprint
from .api.routes import research_analyst_routes
from .api.socket import research_analyst_socket


def create_research_analyst_blueprint():
    """Create and configure the Research Analyst AI blueprint"""

    bp = Blueprint(
        "research_analyst",
        __name__,
        url_prefix="/ai/agents/research_analyst",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(research_analyst_routes)

    # Register WebSocket handlers
    research_analyst_socket.init_app(bp)

    return bp


# Export the blueprint
research_analyst_bp = create_research_analyst_blueprint()
