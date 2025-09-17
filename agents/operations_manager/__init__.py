"""
Operations Manager AI Blueprint Registration
Flask blueprint for Operations Manager AI
"""

from flask import Blueprint
from .api.routes import operations_manager_routes
from .api.socket import operations_manager_socket

def create_operations_manager_blueprint():
    """Create and configure the Operations Manager AI blueprint"""
    
    bp = Blueprint('operations_manager', __name__, 
                   url_prefix='/ai/agents/operations_manager',
                   template_folder='templates',
                   static_folder='static')
    
    # Register routes
    bp.register_blueprint(operations_manager_routes)
    
    # Register WebSocket handlers
    operations_manager_socket.init_app(bp)
    
    return bp

# Export the blueprint
operations_manager_bp = create_operations_manager_blueprint()