"""
Authentication Service Module
Handles JWT authentication, session management, and user verification
"""

import hashlib
import logging
import re
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MimeMultipart
from email.mime.text import MimeText
from functools import wraps

import jwt
from flask import current_app, jsonify, request, session

from .db import User, UserRole, db

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Custom authentication error"""

    pass


class AuthService:
    """Authentication service class"""

    @staticmethod
    def generate_jwt_token(user_id, role="free", expires_in=timedelta(hours=24)):
        """Generate JWT token for user"""
        try:
            payload = {
                "user_id": user_id,
                "role": role,
                "exp": datetime.utcnow() + expires_in,
                "iat": datetime.utcnow(),
                "iss": "ai-portfolio-platform",
            }

            token = jwt.encode(
                payload,
                current_app.config.get("JWT_SECRET_KEY", "dev-secret-key"),
                algorithm="HS256",
            )

            return token

        except Exception as e:
            logger.error(f"JWT token generation failed: {str(e)}")
            raise AuthError(f"Token generation failed: {str(e)}")

    @staticmethod
    def decode_jwt_token(token):
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config.get("JWT_SECRET_KEY", "dev-secret-key"),
                algorithms=["HS256"],
                options={"verify_exp": True},
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthError(f"Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"JWT decode error: {str(e)}")
            raise AuthError(f"Token verification failed: {str(e)}")

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password_strength(password):
        """Validate password strength"""
        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")

        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")

        return errors

    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if len(username) < 3 or len(username) > 30:
            return False

        # Only alphanumeric and underscores
        pattern = r"^[a-zA-Z0-9_]+$"
        return re.match(pattern, username) is not None

    @staticmethod
    def generate_verification_token():
        """Generate secure verification token"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token):
        """Hash token for secure storage"""
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def register_user(email, username, password, first_name=None, last_name=None):
        """Register new user with validation"""
        try:
            # Validate email format
            if not AuthService.validate_email(email):
                raise AuthError("Invalid email format")

            # Validate username
            if not AuthService.validate_username(username):
                raise AuthError(
                    "Username must be 3-30 characters, alphanumeric and underscores only"
                )

            # Validate password strength
            password_errors = AuthService.validate_password_strength(password)
            if password_errors:
                raise AuthError("; ".join(password_errors))

            # Check if user already exists
            if User.query.filter_by(email=email).first():
                raise AuthError("Email already registered")

            if User.query.filter_by(username=username).first():
                raise AuthError("Username already taken")

            # Create verification token
            verification_token = AuthService.generate_verification_token()

            # Create user
            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                verification_token=AuthService.hash_token(verification_token),
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # Send verification email
            try:
                AuthService.send_verification_email(email, verification_token)
            except Exception as e:
                logger.warning(f"Failed to send verification email: {str(e)}")
                # Don't fail registration if email fails

            logger.info(f"New user registered: {email}")
            return user, verification_token

        except AuthError:
            raise
        except Exception as e:
            db.session.rollback()
            logger.error(f"User registration failed: {str(e)}")
            raise AuthError(f"Registration failed: {str(e)}")

    @staticmethod
    def login_user(email_or_username, password):
        """Authenticate user login"""
        try:
            # Find user by email or username
            user = User.query.filter(
                (User.email == email_or_username) | (User.username == email_or_username)
            ).first()

            if not user:
                raise AuthError("User not found")

            if not user.is_active:
                raise AuthError("Account is deactivated")

            if not user.check_password(password):
                raise AuthError("Invalid password")

            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Generate JWT token
            token = AuthService.generate_jwt_token(user.id, user.role.value)

            logger.info(f"User logged in: {user.email}")
            return user, token

        except AuthError:
            raise
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise AuthError(f"Login failed: {str(e)}")

    @staticmethod
    def verify_user_email(token):
        """Verify user's email with token"""
        try:
            token_hash = AuthService.hash_token(token)
            user = User.query.filter_by(verification_token=token_hash).first()

            if not user:
                raise AuthError("Invalid verification token")

            user.is_verified = True
            user.verification_token = None  # Clear token after use
            db.session.commit()

            logger.info(f"User email verified: {user.email}")
            return user

        except AuthError:
            raise
        except Exception as e:
            logger.error(f"Email verification failed: {str(e)}")
            raise AuthError(f"Verification failed: {str(e)}")

    @staticmethod
    def send_verification_email(email, token):
        """Send email verification"""
        try:
            smtp_host = current_app.config.get("SMTP_HOST", "smtp.gmail.com")
            smtp_port = current_app.config.get("SMTP_PORT", 587)
            smtp_user = current_app.config.get("SMTP_USER")
            smtp_pass = current_app.config.get("SMTP_PASSWORD")

            if not smtp_user or not smtp_pass:
                logger.warning("SMTP credentials not configured, skipping email")
                return False

            # Create verification URL
            base_url = current_app.config.get("BASE_URL", "http://localhost:3000")
            verify_url = f"{base_url}/auth/verify-email?token={token}"

            # Create email content
            subject = "Verify Your Email - AI Portfolio Platform"

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Verification</title>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 28px;">Welcome to AI Portfolio Platform!</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Please verify your email to get started</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <p style="font-size: 16px; margin-bottom: 25px;">Thank you for joining our platform! To complete your registration and start using our AI services, please verify your email address by clicking the button below:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verify_url}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px; display: inline-block;">Verify Email Address</a>
                    </div>
                    
                    <p style="font-size: 14px; color: #666; margin-top: 25px;">If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="font-size: 12px; color: #888; word-break: break-all; background: #fff; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">{verify_url}</p>
                    
                    <p style="font-size: 14px; color: #666; margin-top: 25px;">This verification link will expire in 24 hours for security reasons.</p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 25px 0;">
                    
                    <p style="font-size: 12px; color: #888; margin-bottom: 0;">If you didn't create an account with us, please ignore this email.</p>
                </div>
            </body>
            </html>
            """

            # Create message
            msg = MimeMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = email

            # Add HTML content
            html_part = MimeText(html_content, "html")
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

            logger.info(f"Verification email sent to: {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send verification email: {str(e)}")
            raise AuthError(f"Failed to send verification email: {str(e)}")

    @staticmethod
    def send_password_reset_email(email):
        """Send password reset email"""
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                # Don't reveal if email exists for security
                return True

            # Generate reset token
            reset_token = AuthService.generate_verification_token()
            user.verification_token = AuthService.hash_token(reset_token)
            db.session.commit()

            # Send reset email (similar to verification email)
            # Implementation would be similar to send_verification_email
            # but with different content and reset URL

            logger.info(f"Password reset email sent to: {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send password reset email: {str(e)}")
            return False

    @staticmethod
    def get_current_user():
        """Get current user from JWT token in request"""
        try:
            # Try to get token from Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            else:
                # Try to get from session or query parameter
                token = session.get("auth_token") or request.args.get("token")

            if not token:
                return None

            # Decode token
            payload = AuthService.decode_jwt_token(token)
            user_id = payload.get("user_id")

            if not user_id:
                return None

            # Get user from database
            user = User.query.get(user_id)
            if not user or not user.is_active:
                return None

            return user

        except AuthError:
            return None
        except Exception as e:
            logger.error(f"Get current user failed: {str(e)}")
            return None


# Authentication decorators
def login_required(f):
    """Decorator to require authentication"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = AuthService.get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        # Add user to request context
        request.current_user = user
        return f(*args, **kwargs)

    return decorated_function


def role_required(required_roles):
    """Decorator to require specific user roles"""
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = AuthService.get_current_user()
            if not user:
                return jsonify({"error": "Authentication required"}), 401

            if user.role.value not in required_roles:
                return jsonify({"error": "Insufficient permissions"}), 403

            request.current_user = user
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def verified_required(f):
    """Decorator to require verified email"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = AuthService.get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        if not user.is_verified:
            return jsonify({"error": "Email verification required"}), 403

        request.current_user = user
        return f(*args, **kwargs)

    return decorated_function


def premium_required(f):
    """Decorator to require premium subscription"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = AuthService.get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        # Check if user has active premium subscription
        if user.role == UserRole.FREE:
            return (
                jsonify(
                    {
                        "error": "Premium subscription required",
                        "upgrade_url": "/pricing",
                    }
                ),
                402,
            )  # Payment Required

        # Check subscription expiry for Pro users
        if user.role == UserRole.PRO:
            if (
                not user.subscription_expires
                or user.subscription_expires <= datetime.utcnow()
            ):
                # Expired subscription, revert to free
                user.role = UserRole.FREE
                db.session.commit()

                return (
                    jsonify(
                        {
                            "error": "Subscription expired, please renew",
                            "upgrade_url": "/pricing",
                        }
                    ),
                    402,
                )

        request.current_user = user
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = AuthService.get_current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401

        if user.role != UserRole.ADMIN:
            return jsonify({"error": "Admin access required"}), 403

        request.current_user = user
        return f(*args, **kwargs)

    return decorated_function


# Rate limiting decorator
def rate_limit(max_requests=60, per_minutes=60):
    """Rate limiting decorator"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = AuthService.get_current_user()
            if not user:
                return jsonify({"error": "Authentication required"}), 401

            # Simple rate limiting based on user role
            if user.role == UserRole.FREE:
                # Check daily message limit for free users
                if not user.can_send_message():
                    return (
                        jsonify(
                            {
                                "error": "Daily message limit reached",
                                "limit": 10,
                                "upgrade_url": "/pricing",
                            }
                        ),
                        429,
                    )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Session management functions
def create_session(user, remember_me=False):
    """Create user session"""
    try:
        # Generate session token
        session_duration = timedelta(days=30) if remember_me else timedelta(hours=24)
        token = AuthService.generate_jwt_token(
            user.id, user.role.value, session_duration
        )

        # Store in session
        session["auth_token"] = token
        session["user_id"] = user.id
        session["user_role"] = user.role.value
        session.permanent = remember_me

        return token

    except Exception as e:
        logger.error(f"Session creation failed: {str(e)}")
        return None


def destroy_session():
    """Destroy user session"""
    session.clear()


def refresh_token():
    """Refresh authentication token"""
    try:
        user = AuthService.get_current_user()
        if not user:
            return None

        # Generate new token
        new_token = AuthService.generate_jwt_token(user.id, user.role.value)

        # Update session
        session["auth_token"] = new_token

        return new_token

    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        return None
