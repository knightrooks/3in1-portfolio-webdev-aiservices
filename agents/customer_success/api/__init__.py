"""
Customer Success AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import customer_success_api
from .socket import CustomersuccessSocketHandler, get_connection_stats
from .events import (
    event_manager,
    CustomersuccessEventManager,
    EventType,
    CustomersuccessEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'customer_success_api',
    
    # WebSocket Handler
    'CustomersuccessSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'CustomersuccessEventManager',
    'EventType',
    'CustomersuccessEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Customer Success AI API"
API_DESCRIPTION = "Production-ready API for Customer Success AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'customer_success',
        'capabilities': ['customer_support', 'relationship_management', 'retention_strategies', 'feedback_analysis'],
        'endpoints': {
            'rest': '/api/customer_success',
            'websocket': '/customer_success',
            'health': '/api/customer_success/health',
            'analytics': '/api/customer_success/analytics'
        },
        'features': [
            'rate_limiting',
            'request_validation',
            'error_handling',
            'analytics_tracking',
            'websocket_support',
            'event_management',
            'session_management'
        ]
    }
