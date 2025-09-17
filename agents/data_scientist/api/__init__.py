"""
Data Scientist AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import data_scientist_api
from .socket import DatascientistSocketHandler, get_connection_stats
from .events import (
    event_manager,
    DatascientistEventManager,
    EventType,
    DatascientistEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'data_scientist_api',
    
    # WebSocket Handler
    'DatascientistSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'DatascientistEventManager',
    'EventType',
    'DatascientistEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Data Scientist AI API"
API_DESCRIPTION = "Production-ready API for Data Scientist AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'data_scientist',
        'capabilities': ['data_analysis', 'machine_learning', 'statistical_modeling', 'predictive_analytics', 'data_visualization'],
        'endpoints': {
            'rest': '/api/data_scientist',
            'websocket': '/data_scientist',
            'health': '/api/data_scientist/health',
            'analytics': '/api/data_scientist/analytics'
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
