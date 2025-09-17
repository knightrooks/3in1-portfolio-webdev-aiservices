"""
Girlfriend AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import girlfriend_api
from .socket import GirlfriendSocketHandler, get_connection_stats
from .events import (
    event_manager,
    GirlfriendEventManager,
    EventType,
    GirlfriendEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'girlfriend_api',
    
    # WebSocket Handler
    'GirlfriendSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'GirlfriendEventManager',
    'EventType',
    'GirlfriendEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Girlfriend AI API"
API_DESCRIPTION = "Production-ready API for Girlfriend AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'girlfriend',
        'capabilities': ['emotional_support', 'relationship_advice', 'casual_conversation', 'companionship'],
        'endpoints': {
            'rest': '/api/girlfriend',
            'websocket': '/girlfriend',
            'health': '/api/girlfriend/health',
            'analytics': '/api/girlfriend/analytics'
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
