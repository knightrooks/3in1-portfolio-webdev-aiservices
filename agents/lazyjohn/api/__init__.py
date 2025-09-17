"""
Lazyjohn AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import lazyjohn_api
from .socket import LazyjohnSocketHandler, get_connection_stats
from .events import (
    event_manager,
    LazyjohnEventManager,
    EventType,
    LazyjohnEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'lazyjohn_api',
    
    # WebSocket Handler
    'LazyjohnSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'LazyjohnEventManager',
    'EventType',
    'LazyjohnEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Lazyjohn AI API"
API_DESCRIPTION = "Production-ready API for Lazyjohn AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'lazyjohn',
        'capabilities': ['casual_chat', 'humor', 'relaxed_conversation', 'entertainment'],
        'endpoints': {
            'rest': '/api/lazyjohn',
            'websocket': '/lazyjohn',
            'health': '/api/lazyjohn/health',
            'analytics': '/api/lazyjohn/analytics'
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
