"""
Product Manager AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import product_manager_api
from .socket import ProductmanagerSocketHandler, get_connection_stats
from .events import (
    event_manager,
    ProductmanagerEventManager,
    EventType,
    ProductmanagerEvent,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred,
)

__all__ = [
    # REST API
    "product_manager_api",
    # WebSocket Handler
    "ProductmanagerSocketHandler",
    "get_connection_stats",
    # Event Management
    "event_manager",
    "ProductmanagerEventManager",
    "EventType",
    "ProductmanagerEvent",
    "emit_conversation_started",
    "emit_conversation_completed",
    "emit_error_occurred",
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "Product Manager AI API"
API_DESCRIPTION = "Production-ready API for Product Manager AI Agent"


def get_api_info():
    """Get API information and status"""
    return {
        "name": API_NAME,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "agent": "product_manager",
        "capabilities": [
            "product_strategy",
            "roadmap_planning",
            "feature_prioritization",
            "user_research",
            "stakeholder_management",
        ],
        "endpoints": {
            "rest": "/api/product_manager",
            "websocket": "/product_manager",
            "health": "/api/product_manager/health",
            "analytics": "/api/product_manager/analytics",
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
