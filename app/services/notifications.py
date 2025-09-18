"""
Notifications Service Module
Handles email, SMS, and in-app notifications for the platform
"""

import json
import logging
import smtplib
import ssl
import threading
import time
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MimeBase
from email.mime.multipart import MimeMultipart
from email.mime.text import MimeText
from queue import Queue

import requests
from flask import current_app, render_template_string

from .db import User, db

logger = logging.getLogger(__name__)


class NotificationError(Exception):
    """Custom notification error"""

    pass


class NotificationService:
    """Notification service for handling various types of communications"""

    def __init__(self):
        self.email_queue = Queue()
        self.sms_queue = Queue()
        self.notification_worker = None
        self.is_running = False
        self._configure_services()

    def _configure_services(self):
        """Configure notification services"""
        self.smtp_configured = self._configure_smtp()
        self.twilio_configured = self._configure_twilio()
        self.push_configured = self._configure_push_notifications()

    def _configure_smtp(self):
        """Configure SMTP email service"""
        try:
            self.smtp_host = current_app.config.get("SMTP_HOST", "smtp.gmail.com")
            self.smtp_port = current_app.config.get("SMTP_PORT", 587)
            self.smtp_user = current_app.config.get("SMTP_USER")
            self.smtp_password = current_app.config.get("SMTP_PASSWORD")
            self.from_email = current_app.config.get("FROM_EMAIL", self.smtp_user)
            self.from_name = current_app.config.get(
                "FROM_NAME", "AI Portfolio Platform"
            )

            if self.smtp_user and self.smtp_password:
                logger.info("SMTP email service configured")
                return True
            else:
                logger.warning("SMTP not configured - missing credentials")
                return False

        except Exception as e:
            logger.error(f"SMTP configuration failed: {str(e)}")
            return False

    def _configure_twilio(self):
        """Configure Twilio SMS service"""
        try:
            self.twilio_account_sid = current_app.config.get("TWILIO_ACCOUNT_SID")
            self.twilio_auth_token = current_app.config.get("TWILIO_AUTH_TOKEN")
            self.twilio_phone = current_app.config.get("TWILIO_PHONE_NUMBER")

            if self.twilio_account_sid and self.twilio_auth_token:
                logger.info("Twilio SMS service configured")
                return True
            else:
                logger.warning("Twilio not configured - missing credentials")
                return False

        except Exception as e:
            logger.error(f"Twilio configuration failed: {str(e)}")
            return False

    def _configure_push_notifications(self):
        """Configure push notification service"""
        try:
            self.firebase_key = current_app.config.get("FIREBASE_SERVER_KEY")
            self.firebase_url = "https://fcm.googleapis.com/fcm/send"

            if self.firebase_key:
                logger.info("Push notifications configured")
                return True
            else:
                logger.warning("Push notifications not configured")
                return False

        except Exception as e:
            logger.error(f"Push notification configuration failed: {str(e)}")
            return False

    def start_notification_worker(self):
        """Start background notification worker"""
        if not self.is_running:
            self.is_running = True
            self.notification_worker = threading.Thread(
                target=self._notification_worker_thread
            )
            self.notification_worker.daemon = True
            self.notification_worker.start()
            logger.info("Notification worker started")

    def stop_notification_worker(self):
        """Stop background notification worker"""
        self.is_running = False
        if self.notification_worker:
            self.notification_worker.join(timeout=5)
            logger.info("Notification worker stopped")

    def _notification_worker_thread(self):
        """Background worker for processing notifications"""
        while self.is_running:
            try:
                # Process email queue
                if not self.email_queue.empty():
                    email_data = self.email_queue.get_nowait()
                    self._send_email_sync(**email_data)

                # Process SMS queue
                if not self.sms_queue.empty():
                    sms_data = self.sms_queue.get_nowait()
                    self._send_sms_sync(**sms_data)

                time.sleep(1)  # Prevent busy waiting

            except Exception as e:
                logger.error(f"Notification worker error: {str(e)}")
                time.sleep(5)  # Wait before retrying

    def send_email(
        self,
        to_email,
        subject,
        template_name=None,
        template_data=None,
        html_content=None,
        text_content=None,
        attachments=None,
        async_send=True,
    ):
        """Send email notification"""
        try:
            if not self.smtp_configured:
                logger.warning("Email not sent - SMTP not configured")
                return False

            email_data = {
                "to_email": to_email,
                "subject": subject,
                "template_name": template_name,
                "template_data": template_data,
                "html_content": html_content,
                "text_content": text_content,
                "attachments": attachments,
            }

            if async_send:
                self.email_queue.put(email_data)
                return True
            else:
                return self._send_email_sync(**email_data)

        except Exception as e:
            logger.error(f"Email queuing failed: {str(e)}")
            return False

    def _send_email_sync(
        self,
        to_email,
        subject,
        template_name=None,
        template_data=None,
        html_content=None,
        text_content=None,
        attachments=None,
    ):
        """Synchronously send email"""
        try:
            # Create message
            msg = MimeMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            # Generate content from template or use provided content
            if template_name:
                html_content, text_content = self._render_email_template(
                    template_name, template_data or {}
                )

            # Add text content
            if text_content:
                text_part = MimeText(text_content, "plain")
                msg.attach(text_part)

            # Add HTML content
            if html_content:
                html_part = MimeText(html_content, "html")
                msg.attach(html_part)

            # Add attachments
            if attachments:
                for attachment in attachments:
                    self._add_attachment(msg, attachment)

            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent to {to_email}: {subject}")
            return True

        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return False

    def _render_email_template(self, template_name, template_data):
        """Render email templates"""
        templates = {
            "welcome": {
                "html": """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Welcome to AI Portfolio Platform</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                        <h1 style="margin: 0; font-size: 28px;">Welcome {{ name }}!</h1>
                        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Your AI Portfolio Platform account is ready</p>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p>Thank you for joining our platform! You now have access to:</p>
                        
                        <ul style="color: #555; margin: 20px 0;">
                            <li>🤖 AI-powered conversations with multiple personas</li>
                            <li>💼 Professional portfolio showcase</li>
                            <li>🌐 Web development services</li>
                            <li>📊 Advanced analytics and insights</li>
                        </ul>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{{ dashboard_url }}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Get Started</a>
                        </div>
                        
                        <p style="font-size: 14px; color: #666;">Need help? Contact our support team at <a href="mailto:support@aiportfolio.com">support@aiportfolio.com</a></p>
                    </div>
                </body>
                </html>
                """,
                "text": """
                Welcome {{ name }}!
                
                Thank you for joining AI Portfolio Platform! You now have access to:
                
                - AI-powered conversations with multiple personas
                - Professional portfolio showcase  
                - Web development services
                - Advanced analytics and insights
                
                Get started: {{ dashboard_url }}
                
                Need help? Contact support@aiportfolio.com
                """,
            },
            "payment_success": {
                "html": """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Payment Confirmation</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                        <h1 style="margin: 0; font-size: 28px;">Payment Successful!</h1>
                        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Thank you for your purchase</p>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                        <h3>Payment Details</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li><strong>Plan:</strong> {{ plan_name }}</li>
                            <li><strong>Amount:</strong> ${{ amount }} {{ currency }}</li>
                            <li><strong>Billing Period:</strong> {{ billing_period }}</li>
                            <li><strong>Payment Date:</strong> {{ payment_date }}</li>
                        </ul>
                        
                        <p>Your subscription is now active and you have access to all premium features!</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{{ dashboard_url }}" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Access Dashboard</a>
                        </div>
                    </div>
                </body>
                </html>
                """,
                "text": """
                Payment Successful!
                
                Payment Details:
                - Plan: {{ plan_name }}
                - Amount: ${{ amount }} {{ currency }}
                - Billing Period: {{ billing_period }}
                - Payment Date: {{ payment_date }}
                
                Your subscription is now active!
                
                Access your dashboard: {{ dashboard_url }}
                """,
            },
            "support_ticket": {
                "html": """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Support Ticket Confirmation</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                        <h1 style="margin: 0; font-size: 28px;">Support Ticket Created</h1>
                        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">We've received your request</p>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p>Hello {{ name }},</p>
                        
                        <p>We've received your support request and will respond within 24 hours.</p>
                        
                        <div style="background: white; padding: 20px; border-radius: 5px; border: 1px solid #ddd; margin: 20px 0;">
                            <h4>Ticket Details:</h4>
                            <ul style="list-style: none; padding: 0;">
                                <li><strong>Ticket #:</strong> {{ ticket_number }}</li>
                                <li><strong>Subject:</strong> {{ subject }}</li>
                                <li><strong>Category:</strong> {{ category }}</li>
                                <li><strong>Priority:</strong> {{ priority }}</li>
                            </ul>
                        </div>
                        
                        <p>You can track your ticket status in your dashboard.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{{ ticket_url }}" style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">View Ticket</a>
                        </div>
                    </div>
                </body>
                </html>
                """,
                "text": """
                Support Ticket Created
                
                Hello {{ name }},
                
                We've received your support request and will respond within 24 hours.
                
                Ticket Details:
                - Ticket #: {{ ticket_number }}
                - Subject: {{ subject }}
                - Category: {{ category }}
                - Priority: {{ priority }}
                
                Track your ticket: {{ ticket_url }}
                """,
            },
        }

        if template_name not in templates:
            raise NotificationError(f"Template not found: {template_name}")

        template = templates[template_name]

        # Simple template rendering (replace {{ variable }} with values)
        html_content = template["html"]
        text_content = template["text"]

        for key, value in template_data.items():
            placeholder = f"{{{{ {key} }}}}"
            html_content = html_content.replace(placeholder, str(value))
            text_content = text_content.replace(placeholder, str(value))

        return html_content, text_content

    def _add_attachment(self, msg, attachment):
        """Add attachment to email message"""
        try:
            if isinstance(attachment, dict):
                filename = attachment.get("filename")
                content = attachment.get("content")
                content_type = attachment.get(
                    "content_type", "application/octet-stream"
                )
            else:
                # Assume it's a file path
                filename = attachment
                with open(attachment, "rb") as file:
                    content = file.read()
                content_type = "application/octet-stream"

            part = MimeBase("application", "octet-stream")
            part.set_payload(content)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            msg.attach(part)

        except Exception as e:
            logger.error(f"Attachment error: {str(e)}")

    def send_sms(self, phone_number, message, async_send=True):
        """Send SMS notification"""
        try:
            if not self.twilio_configured:
                logger.warning("SMS not sent - Twilio not configured")
                return False

            sms_data = {"phone_number": phone_number, "message": message}

            if async_send:
                self.sms_queue.put(sms_data)
                return True
            else:
                return self._send_sms_sync(**sms_data)

        except Exception as e:
            logger.error(f"SMS queuing failed: {str(e)}")
            return False

    def _send_sms_sync(self, phone_number, message):
        """Synchronously send SMS"""
        try:
            from twilio.rest import Client

            client = Client(self.twilio_account_sid, self.twilio_auth_token)

            message = client.messages.create(
                body=message, from_=self.twilio_phone, to=phone_number
            )

            logger.info(f"SMS sent to {phone_number}: {message.sid}")
            return True

        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            return False

    def send_push_notification(self, user_tokens, title, body, data=None):
        """Send push notification via Firebase"""
        try:
            if not self.push_configured:
                logger.warning("Push notification not sent - Firebase not configured")
                return False

            headers = {
                "Authorization": f"key={self.firebase_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "registration_ids": (
                    user_tokens if isinstance(user_tokens, list) else [user_tokens]
                ),
                "notification": {
                    "title": title,
                    "body": body,
                    "icon": "icon-192x192.png",
                    "click_action": "FLUTTER_NOTIFICATION_CLICK",
                },
            }

            if data:
                payload["data"] = data

            response = requests.post(
                self.firebase_url, headers=headers, data=json.dumps(payload)
            )

            if response.status_code == 200:
                logger.info(
                    f"Push notification sent to {len(user_tokens) if isinstance(user_tokens, list) else 1} devices"
                )
                return True
            else:
                logger.error(
                    f"Push notification failed: {response.status_code} - {response.text}"
                )
                return False

        except Exception as e:
            logger.error(f"Push notification error: {str(e)}")
            return False

    def send_in_app_notification(
        self, user_id, title, message, notification_type="info", action_url=None
    ):
        """Send in-app notification (store in database)"""
        try:
            # This would typically store in a notifications table
            # For now, we'll just log it
            notification_data = {
                "user_id": user_id,
                "title": title,
                "message": message,
                "type": notification_type,
                "action_url": action_url,
                "created_at": datetime.utcnow().isoformat(),
                "read": False,
            }

            # In a real implementation, you'd store this in a database table
            logger.info(f"In-app notification for user {user_id}: {title}")

            # Could also emit via WebSocket for real-time notifications
            return True

        except Exception as e:
            logger.error(f"In-app notification failed: {str(e)}")
            return False

    def notify_new_user(self, user):
        """Send welcome notification to new user"""
        try:
            template_data = {
                "name": user.full_name or user.username,
                "dashboard_url": f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/dashboard",
            }

            success = self.send_email(
                to_email=user.email,
                subject="Welcome to AI Portfolio Platform!",
                template_name="welcome",
                template_data=template_data,
            )

            # Also send in-app notification
            self.send_in_app_notification(
                user_id=user.id,
                title="Welcome to AI Portfolio Platform!",
                message="Your account has been created successfully. Start exploring our AI services!",
                notification_type="success",
                action_url="/ai-services",
            )

            return success

        except Exception as e:
            logger.error(f"New user notification failed: {str(e)}")
            return False

    def notify_payment_success(self, user, payment):
        """Send payment confirmation notification"""
        try:
            template_data = {
                "name": user.full_name or user.username,
                "plan_name": payment.product_name,
                "amount": float(payment.amount),
                "currency": payment.currency,
                "billing_period": payment.billing_period,
                "payment_date": (
                    payment.completed_at.strftime("%B %d, %Y")
                    if payment.completed_at
                    else "Today"
                ),
                "dashboard_url": f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/dashboard",
            }

            success = self.send_email(
                to_email=user.email,
                subject="Payment Confirmation - AI Portfolio Platform",
                template_name="payment_success",
                template_data=template_data,
            )

            # In-app notification
            self.send_in_app_notification(
                user_id=user.id,
                title="Payment Successful!",
                message=f"Your {payment.product_name} subscription is now active.",
                notification_type="success",
                action_url="/dashboard",
            )

            return success

        except Exception as e:
            logger.error(f"Payment notification failed: {str(e)}")
            return False

    def notify_support_ticket(self, user, ticket):
        """Send support ticket confirmation"""
        try:
            template_data = {
                "name": user.full_name if user else ticket.name,
                "ticket_number": ticket.ticket_number,
                "subject": ticket.subject,
                "category": ticket.category,
                "priority": ticket.priority,
                "ticket_url": f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/support/ticket/{ticket.id}",
            }

            success = self.send_email(
                to_email=ticket.email,
                subject=f"Support Ticket Created - {ticket.ticket_number}",
                template_name="support_ticket",
                template_data=template_data,
            )

            if user:
                self.send_in_app_notification(
                    user_id=user.id,
                    title="Support Ticket Created",
                    message=f"Your support ticket #{ticket.ticket_number} has been created.",
                    notification_type="info",
                    action_url=f"/support/ticket/{ticket.id}",
                )

            return success

        except Exception as e:
            logger.error(f"Support ticket notification failed: {str(e)}")
            return False

    def get_notification_preferences(self, user_id):
        """Get user notification preferences"""
        # This would typically be stored in a user preferences table
        # For now, return default preferences
        return {
            "email_notifications": True,
            "sms_notifications": False,
            "push_notifications": True,
            "marketing_emails": False,
            "product_updates": True,
            "security_alerts": True,
        }

    def update_notification_preferences(self, user_id, preferences):
        """Update user notification preferences"""
        try:
            # This would typically update a user preferences table
            logger.info(f"Notification preferences updated for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Preference update failed: {str(e)}")
            return False


# Global notification service instance
notification_service = NotificationService()
