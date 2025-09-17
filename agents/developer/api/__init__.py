"""
Developer AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import developer_api
from .socket import DeveloperSocketHandler, get_connection_stats
from .events import (
    event_manager,
    DeveloperEventManager,
    EventType,
    DeveloperEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred,
)

__all__ = [
    # REST API
    "developer_api",
    # WebSocket Handler
    "DeveloperSocketHandler",
    "get_connection_stats",
    # Event Management
    "event_manager",
    "DeveloperEventManager",
    "EventType",
    "DeveloperEvent",
    "emit_conversation_started",
    "emit_conversation_completed",
    "emit_error_occurred",
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Developer AI API"
API_DESCRIPTION = "Production-ready API for Developer AI Agent"


def get_api_info():
    """Get API information and status"""
    return {
        "name": API_NAME,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "agent": "developer",
        "capabilities": [
            "code_development",
            "architecture_design",
            "code_review",
            "debugging",
            "testing",
            "deployment",
        ],
        "endpoints": {
            "rest": "/api/developer",
            "websocket": "/developer",
            "health": "/api/developer/health",
            "analytics": "/api/developer/analytics",
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
