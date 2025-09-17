"""
Customer Success AI Blueprint Registration
Flask blueprint for Customer Success AI
"""

from flask import Blueprint
from .api.routes import customer_success_routes
from .api.socket import customer_success_socket


def create_customer_success_blueprint():
    """Create and configure the Customer Success AI blueprint"""

    bp = Blueprint(
        "customer_success",
        __name__,
        url_prefix="/ai/agents/customer_success",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(customer_success_routes)

    # Register WebSocket handlers
    customer_success_socket.init_app(bp)

    return bp


# Export the blueprint
customer_success_bp = create_customer_success_blueprint()
