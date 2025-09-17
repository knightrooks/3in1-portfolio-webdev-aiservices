"""
Data Scientist AI Blueprint Registration
Flask blueprint for Data Scientist AI
"""

from flask import Blueprint
from .api.routes import data_scientist_routes
from .api.socket import data_scientist_socket


def create_data_scientist_blueprint():
    """Create and configure the Data Scientist AI blueprint"""

    bp = Blueprint(
        "data_scientist",
        __name__,
        url_prefix="/ai/agents/data_scientist",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(data_scientist_routes)

    # Register WebSocket handlers
    data_scientist_socket.init_app(bp)

    return bp


# Export the blueprint
data_scientist_bp = create_data_scientist_blueprint()
