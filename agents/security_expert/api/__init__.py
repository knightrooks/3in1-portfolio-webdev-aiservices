"""
Security Expert AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import security_expert_api
from .socket import SecurityexpertSocketHandler, get_connection_stats
from .events import (
    event_manager,
    SecurityexpertEventManager,
    EventType,
    SecurityexpertEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'security_expert_api',
    
    # WebSocket Handler
    'SecurityexpertSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'SecurityexpertEventManager',
    'EventType',
    'SecurityexpertEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Security Expert AI API"
API_DESCRIPTION = "Production-ready API for Security Expert AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'security_expert',
        'capabilities': ['security_analysis', 'vulnerability_assessment', 'penetration_testing', 'compliance', 'threat_modeling'],
        'endpoints': {
            'rest': '/api/security_expert',
            'websocket': '/security_expert',
            'health': '/api/security_expert/health',
            'analytics': '/api/security_expert/analytics'
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
