"""
Marketing Specialist AI Blueprint Registration
Flask blueprint for Marketing Specialist AI
"""

from flask import Blueprint
from .api.routes import marketing_specialist_routes
from .api.socket import marketing_specialist_socket

def create_marketing_specialist_blueprint():
    """Create and configure the Marketing Specialist AI blueprint"""
    
    bp = Blueprint('marketing_specialist', __name__, 
                   url_prefix='/ai/agents/marketing_specialist',
                   template_folder='templates',
                   static_folder='static')
    
    # Register routes
    bp.register_blueprint(marketing_specialist_routes)
    
    # Register WebSocket handlers
    marketing_specialist_socket.init_app(bp)
    
    return bp

# Export the blueprint
marketing_specialist_bp = create_marketing_specialist_blueprint()