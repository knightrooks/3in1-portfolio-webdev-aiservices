"""
Contact Routes - Flask Blueprint for Contact & Support
This module handles routes for customer support, help desk,
frequently asked questions, and feedback collection.
"""

import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

# Initialize blueprint
contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

logger = logging.getLogger(__name__)


@contact_bp.route("/support")
def support():
    """Customer support and help desk"""
    support_categories = [
        {
            "id": "technical",
            "name": "Technical Issues",
            "description": "Platform bugs, performance issues, login problems",
            "icon": "fas fa-cog",
            "priority": "high",
        },
        {
            "id": "billing",
            "name": "Billing & Payments",
            "description": "Payment issues, subscription changes, refunds",
            "icon": "fas fa-credit-card",
            "priority": "high",
        },
        {
            "id": "ai_services",
            "name": "AI Services",
            "description": "AI agent issues, conversation problems, feature requests",
            "icon": "fas fa-robot",
            "priority": "medium",
        },
        {
            "id": "webdev",
            "name": "Web Development",
            "description": "Project inquiries, service questions, consultations",
            "icon": "fas fa-code",
            "priority": "medium",
        },
        {
            "id": "account",
            "name": "Account Management",
            "description": "Profile settings, data requests, account deletion",
            "icon": "fas fa-user-cog",
            "priority": "low",
        },
        {
            "id": "general",
            "name": "General Inquiry",
            "description": "Questions, suggestions, partnership opportunities",
            "icon": "fas fa-question-circle",
            "priority": "low",
        },
    ]

    # Support hours and response times
    support_info = {
        "hours": {
            "weekdays": "9:00 AM - 6:00 PM EST",
            "weekends": "10:00 AM - 4:00 PM EST",
            "holidays": "Limited support",
        },
        "response_times": {
            "high": "2-4 hours",
            "medium": "4-8 hours",
            "low": "24-48 hours",
        },
        "contact_methods": [
            {
                "method": "Support Ticket",
                "description": "Best for detailed technical issues",
                "response_time": "Based on priority",
            },
            {
                "method": "Live Chat",
                "description": "Quick questions and immediate help",
                "response_time": "Real-time during business hours",
            },
            {
                "method": "Email",
                "description": "Non-urgent inquiries and documentation",
                "response_time": "24-48 hours",
            },
        ],
    }

    return render_template(
        "contact/support.html", categories=support_categories, support_info=support_info
    )


@contact_bp.route("/faq")
def faq():
    """Frequently Asked Questions"""
    faq_categories = {
        "general": {
            "name": "General",
            "questions": [
                {
                    "question": "What is the 3-in-1 Platform?",
                    "answer": "Our platform combines a professional portfolio, web development services, and AI services in one comprehensive solution. You can showcase your work, offer services, and interact with advanced AI agents all in one place.",
                },
                {
                    "question": "How do I create an account?",
                    "answer": 'Click the "Sign Up" button in the top navigation, fill out the registration form with your email and password, and verify your email address. You\'ll have immediate access to free tier features.',
                },
                {
                    "question": "Is my data secure?",
                    "answer": "Yes, we use industry-standard security measures including SSL encryption, secure data storage, and regular security audits. Your personal information and conversations are protected.",
                },
            ],
        },
        "ai_services": {
            "name": "AI Services",
            "questions": [
                {
                    "question": "How do AI agents work?",
                    "answer": "Our AI agents are powered by advanced language models with unique personalities and specializations. They can help with various tasks from casual conversation to technical assistance.",
                },
                {
                    "question": "What's the difference between free and paid AI services?",
                    "answer": "Free tier includes limited daily messages with basic agents. Paid plans offer unlimited messages, access to all agents, conversation history, and priority support.",
                },
                {
                    "question": "Can I export my conversation history?",
                    "answer": "Yes, paid subscribers can export their conversation history in various formats (JSON, PDF, TXT) from their account settings.",
                },
                {
                    "question": "Are conversations with AI agents private?",
                    "answer": "Yes, your conversations are private and encrypted. We use anonymized data to improve AI performance, but your personal conversations remain confidential.",
                },
            ],
        },
        "webdev": {
            "name": "Web Development",
            "questions": [
                {
                    "question": "What web development services do you offer?",
                    "answer": "We offer comprehensive web development services including custom websites, web applications, e-commerce solutions, mobile apps, SEO optimization, and ongoing maintenance.",
                },
                {
                    "question": "How long does a typical web project take?",
                    "answer": "Project timelines vary based on complexity. Simple websites take 2-4 weeks, while complex applications may take 2-6 months. We provide detailed timelines during project planning.",
                },
                {
                    "question": "Do you provide hosting and maintenance?",
                    "answer": "Yes, we offer hosting solutions and maintenance packages. This includes regular updates, security patches, backups, and technical support for your website.",
                },
                {
                    "question": "What technologies do you use?",
                    "answer": "We use modern technologies including Python/Flask, JavaScript/React, HTML5/CSS3, databases (PostgreSQL, MongoDB), cloud platforms (AWS, Azure), and more based on project needs.",
                },
            ],
        },
        "billing": {
            "name": "Billing & Payments",
            "questions": [
                {
                    "question": "What payment methods do you accept?",
                    "answer": "We accept major credit cards, PayPal, and bank transfers. For enterprise clients, we also accept cryptocurrency payments and can arrange custom billing terms.",
                },
                {
                    "question": "Can I cancel my subscription anytime?",
                    "answer": "Yes, you can cancel your AI services subscription at any time. You'll retain access until the end of your current billing period and receive a prorated refund for unused time.",
                },
                {
                    "question": "How do refunds work for web development projects?",
                    "answer": "Web development refunds depend on project progress. Full refunds available before work begins, partial refunds based on completed work phases. See our payment policy for details.",
                },
                {
                    "question": "Do you offer discounts for long-term commitments?",
                    "answer": "Yes, we offer discounts for annual AI service subscriptions and long-term web development partnerships. Contact our sales team for custom pricing.",
                },
            ],
        },
        "technical": {
            "name": "Technical Support",
            "questions": [
                {
                    "question": "Why is the AI agent not responding?",
                    "answer": "Check your internet connection and try refreshing the page. If the issue persists, the agent may be temporarily unavailable due to high demand or maintenance.",
                },
                {
                    "question": "How do I reset my password?",
                    "answer": 'Click "Forgot Password" on the login page, enter your email address, and follow the instructions in the reset email. Check your spam folder if you don\'t receive it within a few minutes.',
                },
                {
                    "question": "What browsers are supported?",
                    "answer": "We support all modern browsers including Chrome, Firefox, Safari, and Edge. For the best experience, please use the latest version of your preferred browser.",
                },
                {
                    "question": "Can I use the platform on mobile devices?",
                    "answer": "Yes, our platform is fully responsive and works on mobile devices. We also plan to release dedicated mobile apps in the future.",
                },
            ],
        },
    }

    return render_template("contact/faq.html", faq_categories=faq_categories)


@contact_bp.route("/feedback")
def feedback():
    """User feedback form"""
    feedback_types = [
        {"value": "bug_report", "label": "Bug Report", "icon": "fas fa-bug"},
        {
            "value": "feature_request",
            "label": "Feature Request",
            "icon": "fas fa-lightbulb",
        },
        {
            "value": "improvement",
            "label": "Improvement Suggestion",
            "icon": "fas fa-arrow-up",
        },
        {"value": "compliment", "label": "Compliment", "icon": "fas fa-heart"},
        {
            "value": "complaint",
            "label": "Complaint",
            "icon": "fas fa-exclamation-triangle",
        },
        {"value": "other", "label": "Other", "icon": "fas fa-comment"},
    ]

    return render_template("contact/feedback.html", feedback_types=feedback_types)


@contact_bp.route("/api/support-ticket", methods=["POST"])
def create_support_ticket():
    """Create a new support ticket"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["name", "email", "category", "subject", "message"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Generate ticket ID
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Create ticket data
        ticket = {
            "id": ticket_id,
            "name": data["name"],
            "email": data["email"],
            "category": data["category"],
            "subject": data["subject"],
            "message": data["message"],
            "priority": data.get("priority", "medium"),
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "attachments": data.get("attachments", []),
        }

        # Save ticket (in production, save to database)
        tickets_file = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "support_tickets.json"
        )
        try:
            with open(tickets_file, "r") as f:
                tickets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tickets = []

        tickets.append(ticket)

        # Ensure data directory exists
        os.makedirs(os.path.dirname(tickets_file), exist_ok=True)
        with open(tickets_file, "w") as f:
            json.dump(tickets, f, indent=2)

        # Send confirmation email (implement email service)
        try:
            send_ticket_confirmation_email(ticket)
        except Exception as e:
            logger.warning(f"Failed to send confirmation email: {e}")

        return jsonify(
            {
                "success": True,
                "message": "Support ticket created successfully",
                "ticket_id": ticket_id,
                "estimated_response": get_estimated_response_time(data["category"]),
            }
        )

    except Exception as e:
        logger.error(f"Error creating support ticket: {e}")
        return jsonify({"error": "Failed to create support ticket"}), 500


@contact_bp.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["type", "message"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Generate feedback ID
        feedback_id = f"FB-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Create feedback data
        feedback = {
            "id": feedback_id,
            "type": data["type"],
            "message": data["message"],
            "name": data.get("name", "Anonymous"),
            "email": data.get("email", ""),
            "rating": data.get("rating"),
            "page_url": data.get("page_url", ""),
            "browser_info": data.get("browser_info", ""),
            "created_at": datetime.now().isoformat(),
            "status": "new",
        }

        # Save feedback (in production, save to database)
        feedback_file = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "feedback.json"
        )
        try:
            with open(feedback_file, "r") as f:
                feedbacks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            feedbacks = []

        feedbacks.append(feedback)

        # Ensure data directory exists
        os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
        with open(feedback_file, "w") as f:
            json.dump(feedbacks, f, indent=2)

        return jsonify(
            {
                "success": True,
                "message": "Feedback submitted successfully",
                "feedback_id": feedback_id,
            }
        )

    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return jsonify({"error": "Failed to submit feedback"}), 500


@contact_bp.route("/api/live-chat/init", methods=["POST"])
def init_live_chat():
    """Initialize live chat session"""
    try:
        data = request.get_json()

        # Create chat session
        session_id = f"CHAT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Check if support is available
        is_available = is_support_available()

        chat_session = {
            "id": session_id,
            "user_name": data.get("name", "Guest"),
            "user_email": data.get("email", ""),
            "category": data.get("category", "general"),
            "status": "waiting" if is_available else "offline",
            "created_at": datetime.now().isoformat(),
            "messages": [],
        }

        return jsonify(
            {
                "success": True,
                "session_id": session_id,
                "is_available": is_available,
                "queue_position": get_queue_position() if is_available else 0,
                "estimated_wait": get_estimated_wait_time() if is_available else None,
            }
        )

    except Exception as e:
        logger.error(f"Error initializing live chat: {e}")
        return jsonify({"error": "Failed to initialize chat"}), 500


def send_ticket_confirmation_email(ticket):
    """Send confirmation email for support ticket"""
    # Implementation would use actual email service (SendGrid, AWS SES, etc.)
    logger.info(
        f"Confirmation email would be sent to {ticket['email']} for ticket {ticket['id']}"
    )


def get_estimated_response_time(category):
    """Get estimated response time based on category"""
    response_times = {
        "technical": "2-4 hours",
        "billing": "2-4 hours",
        "ai_services": "4-8 hours",
        "webdev": "4-8 hours",
        "account": "24-48 hours",
        "general": "24-48 hours",
    }
    return response_times.get(category, "24-48 hours")


def is_support_available():
    """Check if live support is currently available"""
    # Implementation would check current time against business hours
    current_hour = datetime.now().hour
    # Business hours: 9 AM to 6 PM EST (simplified)
    return 9 <= current_hour <= 18


def get_queue_position():
    """Get current position in support queue"""
    # Implementation would check actual queue
    import random

    return random.randint(1, 5)


def get_estimated_wait_time():
    """Get estimated wait time for support"""
    # Implementation would calculate based on queue and agent availability
    queue_pos = get_queue_position()
    return f"{queue_pos * 3}-{queue_pos * 5} minutes"


# Error handlers
@contact_bp.errorhandler(404)
def contact_not_found(error):
    """Custom 404 handler for contact pages"""
    return render_template("contact/404.html"), 404


@contact_bp.errorhandler(500)
def contact_internal_error(error):
    """Custom 500 handler for contact pages"""
    return render_template("contact/500.html"), 500
