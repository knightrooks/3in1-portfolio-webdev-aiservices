"""
Strictwife AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import strictwife_api
from .socket import StrictwifeSocketHandler, get_connection_stats
from .events import (
    event_manager,
    StrictwifeEventManager,
    EventType,
    StrictwifeEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred,
)

__all__ = [
    # REST API
    "strictwife_api",
    # WebSocket Handler
    "StrictwifeSocketHandler",
    "get_connection_stats",
    # Event Management
    "event_manager",
    "StrictwifeEventManager",
    "EventType",
    "StrictwifeEvent",
    "emit_conversation_started",
    "emit_conversation_completed",
    "emit_error_occurred",
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Strictwife AI API"
API_DESCRIPTION = "Production-ready API for Strictwife AI Agent"


def get_api_info():
    """Get API information and status"""
    return {
        "name": API_NAME,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "agent": "strictwife",
        "capabilities": [
            "discipline",
            "organization",
            "accountability",
            "structured_guidance",
        ],
        "endpoints": {
            "rest": "/api/strictwife",
            "websocket": "/strictwife",
            "health": "/api/strictwife/health",
            "analytics": "/api/strictwife/analytics",
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
