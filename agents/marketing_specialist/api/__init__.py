"""
Marketing Specialist AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import marketing_specialist_api
from .socket import MarketingspecialistSocketHandler, get_connection_stats
from .events import (
    event_manager,
    MarketingspecialistEventManager,
    EventType,
    MarketingspecialistEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred,
)

__all__ = [
    # REST API
    "marketing_specialist_api",
    # WebSocket Handler
    "MarketingspecialistSocketHandler",
    "get_connection_stats",
    # Event Management
    "event_manager",
    "MarketingspecialistEventManager",
    "EventType",
    "MarketingspecialistEvent",
    "emit_conversation_started",
    "emit_conversation_completed",
    "emit_error_occurred",
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Marketing Specialist AI API"
API_DESCRIPTION = "Production-ready API for Marketing Specialist AI Agent"


def get_api_info():
    """Get API information and status"""
    return {
        "name": API_NAME,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "agent": "marketing_specialist",
        "capabilities": [
            "marketing_strategy",
            "campaign_management",
            "brand_development",
            "digital_marketing",
            "analytics",
        ],
        "endpoints": {
            "rest": "/api/marketing_specialist",
            "websocket": "/marketing_specialist",
            "health": "/api/marketing_specialist/health",
            "analytics": "/api/marketing_specialist/analytics",
        },
        "features": [
            "rate_limiting",
            "request_validation",
            "error_handling",
            "analytics_tracking",
            "websocket_support",
            "event_management",
            "session_management",
        ],
    }
