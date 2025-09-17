"""
Operations Manager AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import operations_manager_api
from .socket import OperationsmanagerSocketHandler, get_connection_stats
from .events import (
    event_manager,
    OperationsmanagerEventManager,
    EventType,
    OperationsmanagerEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'operations_manager_api',
    
    # WebSocket Handler
    'OperationsmanagerSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'OperationsmanagerEventManager',
    'EventType',
    'OperationsmanagerEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Operations Manager AI API"
API_DESCRIPTION = "Production-ready API for Operations Manager AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'operations_manager',
        'capabilities': ['process_optimization', 'resource_management', 'quality_assurance', 'workflow_design', 'performance_monitoring'],
        'endpoints': {
            'rest': '/api/operations_manager',
            'websocket': '/operations_manager',
            'health': '/api/operations_manager/health',
            'analytics': '/api/operations_manager/analytics'
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
