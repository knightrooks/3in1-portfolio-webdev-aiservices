"""
Services Module Init
Imports and exposes all service modules for the application
"""

from .auth import (
    AuthError,
    AuthService,
    admin_required,
    create_session,
    destroy_session,
    login_required,
    premium_required,
    rate_limit,
    refresh_token,
    role_required,
    verified_required,
)
from .db import (
    AgentUsageStats,
    Conversation,
    Feedback,
    Message,
    Payment,
    SupportTicket,
    User,
    UserRole,
    WebDevProject,
    create_tables,
    create_user,
    db,
    drop_tables,
    get_conversation_history,
    get_user_by_email,
    get_user_by_username,
    get_user_conversations,
    init_db,
    migrate,
    save_message,
    update_agent_usage_stats,
)
from .notifications import NotificationError, NotificationService, notification_service
from .payments import PaymentError, PaymentService, payment_service
from .utils import FileError, UtilityService, ValidationError, utils

__all__ = [
    # Database
    "db",
    "migrate",
    "init_db",
    "create_tables",
    "drop_tables",
    "User",
    "Conversation",
    "Message",
    "SupportTicket",
    "Payment",
    "WebDevProject",
    "Feedback",
    "AgentUsageStats",
    "UserRole",
    "get_user_by_email",
    "get_user_by_username",
    "create_user",
    "get_conversation_history",
    "save_message",
    "get_user_conversations",
    "update_agent_usage_stats",
    # Authentication
    "AuthService",
    "AuthError",
    "login_required",
    "role_required",
    "verified_required",
    "premium_required",
    "admin_required",
    "rate_limit",
    "create_session",
    "destroy_session",
    "refresh_token",
    # Payments
    "PaymentService",
    "PaymentError",
    "payment_service",
    # Notifications
    "NotificationService",
    "NotificationError",
    "notification_service",
    # Utilities
    "UtilityService",
    "ValidationError",
    "FileError",
    "utils",
]
