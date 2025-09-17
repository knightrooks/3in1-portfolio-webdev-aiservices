"""
Content Creator AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import content_creator_api
from .socket import ContentcreatorSocketHandler, get_connection_stats
from .events import (
    event_manager,
    ContentcreatorEventManager,
    EventType,
    ContentcreatorEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'content_creator_api',
    
    # WebSocket Handler
    'ContentcreatorSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'ContentcreatorEventManager',
    'EventType',
    'ContentcreatorEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Content Creator AI API"
API_DESCRIPTION = "Production-ready API for Content Creator AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'content_creator',
        'capabilities': ['content_strategy', 'copywriting', 'seo_optimization', 'social_media', 'brand_messaging'],
        'endpoints': {
            'rest': '/api/content_creator',
            'websocket': '/content_creator',
            'health': '/api/content_creator/health',
            'analytics': '/api/content_creator/analytics'
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
