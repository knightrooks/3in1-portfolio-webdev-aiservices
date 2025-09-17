"""
Emotionaljenny AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import emotionaljenny_api
from .socket import EmotionaljennySocketHandler, get_connection_stats
from .events import (
    event_manager,
    EmotionaljennyEventManager,
    EventType,
    EmotionaljennyEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'emotionaljenny_api',
    
    # WebSocket Handler
    'EmotionaljennySocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'EmotionaljennyEventManager',
    'EventType',
    'EmotionaljennyEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Emotionaljenny AI API"
API_DESCRIPTION = "Production-ready API for Emotionaljenny AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'emotionaljenny',
        'capabilities': ['emotional_intelligence', 'empathy', 'mood_support', 'personal_guidance'],
        'endpoints': {
            'rest': '/api/emotionaljenny',
            'websocket': '/emotionaljenny',
            'health': '/api/emotionaljenny/health',
            'analytics': '/api/emotionaljenny/analytics'
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
