"""
Gossipqueen AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import gossipqueen_api
from .socket import GossipqueenSocketHandler, get_connection_stats
from .events import (
    event_manager,
    GossipqueenEventManager,
    EventType,
    GossipqueenEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    'gossipqueen_api',
    
    # WebSocket Handler
    'GossipqueenSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'GossipqueenEventManager',
    'EventType',
    'GossipqueenEvent',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Gossipqueen AI API"
API_DESCRIPTION = "Production-ready API for Gossipqueen AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'gossipqueen',
        'capabilities': ['social_updates', 'trending_topics', 'celebrity_news', 'entertainment_gossip'],
        'endpoints': {
            'rest': '/api/gossipqueen',
            'websocket': '/gossipqueen',
            'health': '/api/gossipqueen/health',
            'analytics': '/api/gossipqueen/analytics'
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
