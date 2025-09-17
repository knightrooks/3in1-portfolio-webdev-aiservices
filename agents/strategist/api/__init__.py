"""
Business Strategist AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import strategist_api
from .socket import StrategistSocketHandler, get_connection_stats
from .events import (
    event_manager,
    StrategistEventManager,
    EventType,
    StrategistEvent,
    emit_consultation_started,
    emit_consultation_completed,
    emit_strategy_generated,
    emit_error_occurred
)

__all__ = [
    # REST API
    'strategist_api',
    
    # WebSocket Handler
    'StrategistSocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    'StrategistEventManager',
    'EventType',
    'StrategistEvent',
    'emit_consultation_started',
    'emit_consultation_completed', 
    'emit_strategy_generated',
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Strategist AI API"
API_DESCRIPTION = "Production-ready API for Business Strategist AI Agent"

def get_api_info():
    """Get API information and status"""
    return {
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': 'strategist',
        'capabilities': [
            'strategic_planning',
            'business_analysis',
            'market_research',
            'competitive_analysis',
            'growth_strategies',
            'risk_assessment',
            'business_plans',
            'performance_optimization'
        ],
        'endpoints': {
            'rest': '/api/strategist',
            'websocket': '/strategist',
            'health': '/api/strategist/health',
            'analytics': '/api/strategist/analytics'
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