"""
Coderbot AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import coderbot_api
from .socket import CoderbotSocketHandler, get_connection_stats
from .events import (
    event_manager,
    CoderbotEventManager,
    EventType,
    CoderbotEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'coderbot_api',
    
    # WebSocket Handler
    'CoderbotSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'CoderbotEventManager',
    'EventType',
    'CoderbotEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Coderbot AI API"
API_DESCRIPTION = "Production-ready API for Coderbot AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'coderbot',
        'capabilities': ['coding_assistance', 'programming_tutorials', 'code_debugging', 'technical_support'],
        'endpoints': {
            'rest': '/api/coderbot',
            'websocket': '/coderbot',
            'health': '/api/coderbot/health',
            'analytics': '/api/coderbot/analytics'
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
