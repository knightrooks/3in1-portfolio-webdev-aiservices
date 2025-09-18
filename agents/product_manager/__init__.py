"""
Product Manager AI Blueprint Registration
Flask blueprint for Product Manager AI
"""

from flask import Blueprint
from .api.routes import product_manager_routes
from .api.socket import product_manager_socket


def create_product_manager_blueprint():
    """Create and configure the Product Manager AI blueprint"""

    bp = Blueprint(
        "product_manager",
        __name__,
        url_prefix="/ai/agents/product_manager",
        template_folder="templates",
        static_folder="static",
    )

    # Register routes
    bp.register_blueprint(product_manager_routes)

    # Register WebSocket handlers
    product_manager_socket.init_app(bp)

    return bp


# Export the blueprint
product_manager_bp = create_product_manager_blueprint()
