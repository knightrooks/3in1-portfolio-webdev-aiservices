"""
Database Service Module
Handles database models and operations for the 3-in-1 platform
"""

import json
import uuid
from datetime import datetime, timedelta
from enum import Enum

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
migrate = Migrate()


class UserRole(Enum):
    """User roles enumeration"""

    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"


class User(db.Model):
    """User model for authentication and account management"""

    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    # Account settings
    role = db.Column(db.Enum(UserRole), default=UserRole.FREE, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(255))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    last_login = db.Column(db.DateTime)

    # AI Service usage
    daily_message_count = db.Column(db.Integer, default=0)
    last_message_date = db.Column(db.Date, default=datetime.utcnow().date)
    subscription_expires = db.Column(db.DateTime)

    # Relationships
    conversations = db.relationship(
        "Conversation", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    support_tickets = db.relationship("SupportTicket", backref="user", lazy="dynamic")
    payments = db.relationship("Payment", backref="user", lazy="dynamic")

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def can_send_message(self):
        """Check if user can send AI messages based on plan limits"""
        today = datetime.utcnow().date()

        # Reset daily count if new day
        if self.last_message_date != today:
            self.daily_message_count = 0
            self.last_message_date = today
            db.session.commit()

        if self.role == UserRole.FREE:
            return self.daily_message_count < 10
        elif self.role == UserRole.PRO:
            # Check subscription validity
            if (
                self.subscription_expires
                and self.subscription_expires > datetime.utcnow()
            ):
                return True
            else:
                # Expired subscription, revert to free
                self.role = UserRole.FREE
                db.session.commit()
                return self.daily_message_count < 10
        else:  # Enterprise or Admin
            return True

    def increment_message_count(self):
        """Increment daily message count"""
        self.daily_message_count += 1
        db.session.commit()

    @property
    def full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "role": self.role.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "daily_message_count": self.daily_message_count,
            "subscription_expires": (
                self.subscription_expires.isoformat()
                if self.subscription_expires
                else None
            ),
        }


class Conversation(db.Model):
    """AI conversation model"""

    __tablename__ = "conversations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, index=True
    )
    agent_id = db.Column(db.String(50), nullable=False, index=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)

    # Conversation metadata
    title = db.Column(db.String(200))  # Auto-generated from first message
    is_archived = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    messages = db.relationship(
        "Message", backref="conversation", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Convert conversation to dictionary"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "title": self.title,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_count": self.messages.count(),
        }


class Message(db.Model):
    """AI conversation message model"""

    __tablename__ = "messages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(
        db.String(36), db.ForeignKey("conversations.id"), nullable=False, index=True
    )

    # Message content
    content = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'agent'

    # AI metadata
    model_used = db.Column(db.String(50))
    processing_time = db.Column(db.Float)  # in seconds
    metadata = db.Column(db.JSON)  # Additional data like confidence, tokens, etc.

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def to_dict(self):
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "content": self.content,
            "sender": self.sender,
            "model_used": self.model_used,
            "processing_time": self.processing_time,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


class SupportTicket(db.Model):
    """Customer support ticket model"""

    __tablename__ = "support_tickets"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=True, index=True
    )  # Can be null for anonymous

    # Ticket details
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default="medium")  # low, medium, high, urgent
    status = db.Column(
        db.String(20), default="open"
    )  # open, in_progress, resolved, closed

    # Assignment
    assigned_to = db.Column(db.String(100))  # Staff member

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    resolved_at = db.Column(db.DateTime)

    def to_dict(self):
        """Convert ticket to dictionary"""
        return {
            "id": self.id,
            "ticket_number": self.ticket_number,
            "name": self.name,
            "email": self.email,
            "category": self.category,
            "subject": self.subject,
            "message": self.message,
            "priority": self.priority,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


class Payment(db.Model):
    """Payment transaction model"""

    __tablename__ = "payments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, index=True
    )

    # Payment details
    stripe_payment_id = db.Column(db.String(100), unique=True, index=True)
    paypal_payment_id = db.Column(db.String(100), unique=True, index=True)
    amount = db.Column(db.Decimal(10, 2), nullable=False)
    currency = db.Column(db.String(3), default="USD", nullable=False)

    # Product information
    product_type = db.Column(
        db.String(50), nullable=False
    )  # 'ai_subscription', 'webdev_service'
    product_name = db.Column(db.String(200), nullable=False)
    billing_period = db.Column(db.String(20))  # 'monthly', 'yearly', 'one_time'

    # Status
    status = db.Column(
        db.String(20), default="pending"
    )  # pending, completed, failed, refunded
    payment_method = db.Column(db.String(20))  # 'stripe', 'paypal'

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            "id": self.id,
            "amount": float(self.amount),
            "currency": self.currency,
            "product_type": self.product_type,
            "product_name": self.product_name,
            "billing_period": self.billing_period,
            "status": self.status,
            "payment_method": self.payment_method,
            "created_at": self.created_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }


class WebDevProject(db.Model):
    """Web development project model"""

    __tablename__ = "webdev_projects"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, index=True
    )

    # Project details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_type = db.Column(
        db.String(50)
    )  # 'website', 'webapp', 'ecommerce', 'mobile'
    budget = db.Column(db.Decimal(10, 2))
    timeline = db.Column(db.String(50))

    # Status
    status = db.Column(
        db.String(20), default="inquiry"
    )  # inquiry, quoted, approved, in_progress, completed, cancelled
    progress_percentage = db.Column(db.Integer, default=0)

    # Requirements
    requirements = db.Column(db.JSON)  # Structured requirements data
    features = db.Column(db.JSON)  # Required features

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deadline = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        """Convert project to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project_type": self.project_type,
            "budget": float(self.budget) if self.budget else None,
            "timeline": self.timeline,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "requirements": self.requirements,
            "features": self.features,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }


class Feedback(db.Model):
    """User feedback model"""

    __tablename__ = "feedback"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=True, index=True
    )

    # Feedback details
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    feedback_type = db.Column(
        db.String(50), nullable=False
    )  # bug_report, feature_request, etc.
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    page_url = db.Column(db.String(500))
    browser_info = db.Column(db.String(200))

    # Status
    status = db.Column(
        db.String(20), default="new"
    )  # new, reviewed, in_progress, resolved, closed
    response = db.Column(db.Text)  # Staff response

    # Timestamps
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        """Convert feedback to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "feedback_type": self.feedback_type,
            "message": self.message,
            "rating": self.rating,
            "page_url": self.page_url,
            "browser_info": self.browser_info,
            "status": self.status,
            "response": self.response,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class AgentUsageStats(db.Model):
    """AI agent usage statistics"""

    __tablename__ = "agent_usage_stats"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = db.Column(db.String(50), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)

    # Usage metrics
    total_conversations = db.Column(db.Integer, default=0)
    total_messages = db.Column(db.Integer, default=0)
    unique_users = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Float, default=0.0)
    user_satisfaction = db.Column(db.Float, default=0.0)  # Average rating

    # Performance metrics
    total_processing_time = db.Column(db.Float, default=0.0)
    error_count = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint("agent_id", "date", name="unique_agent_date"),
    )

    def to_dict(self):
        """Convert stats to dictionary"""
        return {
            "agent_id": self.agent_id,
            "date": self.date.isoformat(),
            "total_conversations": self.total_conversations,
            "total_messages": self.total_messages,
            "unique_users": self.unique_users,
            "average_response_time": self.average_response_time,
            "user_satisfaction": self.user_satisfaction,
            "total_processing_time": self.total_processing_time,
            "error_count": self.error_count,
        }


# Database utility functions
def init_db(app):
    """Initialize database with app"""
    db.init_app(app)
    migrate.init_app(app, db)


def create_tables():
    """Create all database tables"""
    db.create_all()


def drop_tables():
    """Drop all database tables"""
    db.drop_all()


def get_user_by_email(email):
    """Get user by email address"""
    return User.query.filter_by(email=email).first()


def get_user_by_username(username):
    """Get user by username"""
    return User.query.filter_by(username=username).first()


def create_user(email, username, password, **kwargs):
    """Create new user"""
    user = User(email=email, username=username, **kwargs)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def get_conversation_history(user_id, agent_id, session_id, limit=50):
    """Get conversation history for user and agent"""
    conversation = Conversation.query.filter_by(
        user_id=user_id, agent_id=agent_id, session_id=session_id
    ).first()

    if not conversation:
        return []

    messages = (
        Message.query.filter_by(conversation_id=conversation.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    return [msg.to_dict() for msg in reversed(messages)]


def save_message(user_id, agent_id, session_id, content, sender, **metadata):
    """Save conversation message"""
    # Get or create conversation
    conversation = Conversation.query.filter_by(
        user_id=user_id, agent_id=agent_id, session_id=session_id
    ).first()

    if not conversation:
        conversation = Conversation(
            user_id=user_id,
            agent_id=agent_id,
            session_id=session_id,
            title=content[:50] + "..." if len(content) > 50 else content,
        )
        db.session.add(conversation)
        db.session.flush()  # Get the ID

    # Create message
    message = Message(
        conversation_id=conversation.id, content=content, sender=sender, **metadata
    )
    db.session.add(message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()

    db.session.commit()
    return message


def get_user_conversations(user_id, limit=20):
    """Get recent conversations for user"""
    conversations = (
        Conversation.query.filter_by(user_id=user_id, is_archived=False)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
        .all()
    )

    return [conv.to_dict() for conv in conversations]


def update_agent_usage_stats(agent_id, processing_time=None, error=False):
    """Update daily usage statistics for an agent"""
    today = datetime.utcnow().date()

    stats = AgentUsageStats.query.filter_by(agent_id=agent_id, date=today).first()
    if not stats:
        stats = AgentUsageStats(agent_id=agent_id, date=today)
        db.session.add(stats)

    stats.total_messages += 1
    if processing_time:
        stats.total_processing_time += processing_time
        stats.average_response_time = stats.total_processing_time / stats.total_messages

    if error:
        stats.error_count += 1

    db.session.commit()
    return stats
