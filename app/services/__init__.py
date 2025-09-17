"""
Services Module Init
Imports and exposes all service modules for the application
"""

from .db import (
    db, migrate, init_db, create_tables, drop_tables,
    User, Conversation, Message, SupportTicket, Payment,
    WebDevProject, Feedback, AgentUsageStats, UserRole,
    get_user_by_email, get_user_by_username, create_user,
    get_conversation_history, save_message, get_user_conversations,
    update_agent_usage_stats
)

from .auth import (
    AuthService, AuthError,
    login_required, role_required, verified_required,
    premium_required, admin_required, rate_limit,
    create_session, destroy_session, refresh_token
)

from .payments import (
    PaymentService, PaymentError,
    payment_service
)

from .notifications import (
    NotificationService, NotificationError,
    notification_service
)

from .utils import (
    UtilityService, ValidationError, FileError,
    utils
)

__all__ = [
    # Database
    'db', 'migrate', 'init_db', 'create_tables', 'drop_tables',
    'User', 'Conversation', 'Message', 'SupportTicket', 'Payment',
    'WebDevProject', 'Feedback', 'AgentUsageStats', 'UserRole',
    'get_user_by_email', 'get_user_by_username', 'create_user',
    'get_conversation_history', 'save_message', 'get_user_conversations',
    'update_agent_usage_stats',
    
    # Authentication
    'AuthService', 'AuthError',
    'login_required', 'role_required', 'verified_required',
    'premium_required', 'admin_required', 'rate_limit',
    'create_session', 'destroy_session', 'refresh_token',
    
    # Payments
    'PaymentService', 'PaymentError', 'payment_service',
    
    # Notifications
    'NotificationService', 'NotificationError', 'notification_service',
    
    # Utilities
    'UtilityService', 'ValidationError', 'FileError', 'utils'
]