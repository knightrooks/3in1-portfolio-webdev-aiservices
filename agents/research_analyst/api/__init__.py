"""
Research Analyst AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import research_analyst_api
from .socket import ResearchanalystSocketHandler, get_connection_stats
from .events import (
    event_manager,
    ResearchanalystEventManager,
    EventType,
    ResearchanalystEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'research_analyst_api',
    
    # WebSocket Handler
    'ResearchanalystSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'ResearchanalystEventManager',
    'EventType',
    'ResearchanalystEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Research Analyst AI API"
API_DESCRIPTION = "Production-ready API for Research Analyst AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'research_analyst',
        'capabilities': ['market_research', 'data_analysis', 'trend_analysis', 'competitive_intelligence', 'reporting'],
        'endpoints': {
            'rest': '/api/research_analyst',
            'websocket': '/research_analyst',
            'health': '/api/research_analyst/health',
            'analytics': '/api/research_analyst/analytics'
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
