"""
Legal Routes - Flask Blueprint for Legal Pages
This module handles routes for legal documentation including terms of service,
privacy policy, cookie policy, and payment policies.
"""

import logging
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request

# Initialize blueprint
legal_bp = Blueprint("legal", __name__, url_prefix="/legal")

logger = logging.getLogger(__name__)


@legal_bp.route("/terms")
def terms():
    """Terms of Service page"""
    terms_data = {
        "last_updated": "September 17, 2025",
        "company_name": "3-in-1 Platform Services",
        "contact_email": "legal@platform.com",
        "sections": [
            {
                "title": "Acceptance of Terms",
                "content": "By accessing and using this platform, you accept and agree to be bound by the terms and provision of this agreement.",
            },
            {
                "title": "Portfolio Services",
                "content": "Our portfolio section showcases professional work and capabilities. All displayed work is proprietary and protected by copyright laws.",
            },
            {
                "title": "Web Development Services",
                "content": "Web development services are provided under separate service agreements. Terms include project scope, timelines, payments, and deliverables.",
            },
            {
                "title": "AI Services",
                "content": "AI services are provided as-is with no guarantees of accuracy. Users are responsible for validating AI-generated content before use.",
            },
            {
                "title": "User Accounts",
                "content": "Users are responsible for maintaining the confidentiality of their account credentials and for all activities under their account.",
            },
            {
                "title": "Payment Terms",
                "content": "All payments are processed securely through Stripe and PayPal. Refund policies vary by service type and are detailed in service agreements.",
            },
            {
                "title": "Limitation of Liability",
                "content": "The platform and its operators shall not be liable for any indirect, incidental, special, consequential, or punitive damages.",
            },
            {
                "title": "Modifications",
                "content": "We reserve the right to modify these terms at any time. Users will be notified of significant changes.",
            },
        ],
    }

    return render_template("legal/terms.html", terms=terms_data)


@legal_bp.route("/privacy")
def privacy():
    """Privacy Policy page"""
    privacy_data = {
        "last_updated": "September 17, 2025",
        "company_name": "3-in-1 Platform Services",
        "contact_email": "privacy@platform.com",
        "sections": [
            {
                "title": "Information We Collect",
                "content": "We collect information you provide directly to us, such as when you create an account, use our services, or contact us for support.",
                "details": [
                    "Account information (email, name, preferences)",
                    "Communication data (chat logs with AI agents)",
                    "Usage analytics and performance metrics",
                    "Payment information (processed by third parties)",
                ],
            },
            {
                "title": "How We Use Your Information",
                "content": "We use the information we collect to provide, maintain, and improve our services.",
                "details": [
                    "Provide AI agent interactions and conversations",
                    "Process payments for web development services",
                    "Send service updates and notifications",
                    "Improve AI model performance and user experience",
                ],
            },
            {
                "title": "AI Conversation Data",
                "content": "Conversations with AI agents are used to improve service quality and may be anonymized for research purposes.",
                "details": [
                    "Chat logs are encrypted and stored securely",
                    "Personal identifying information is anonymized",
                    "Data is used to improve AI response quality",
                    "Users can request conversation data deletion",
                ],
            },
            {
                "title": "Data Sharing",
                "content": "We do not sell or rent your personal information to third parties.",
                "details": [
                    "Service providers (payment processing, hosting)",
                    "Legal requirements (compliance, law enforcement)",
                    "Business transfers (with user notification)",
                ],
            },
            {
                "title": "Data Security",
                "content": "We implement appropriate technical and organizational measures to protect your personal information.",
                "details": [
                    "Encryption in transit and at rest",
                    "Access controls and authentication",
                    "Regular security audits and updates",
                    "Incident response procedures",
                ],
            },
            {
                "title": "Your Rights",
                "content": "You have certain rights regarding your personal information.",
                "details": [
                    "Access your personal data",
                    "Correct inaccurate information",
                    "Delete your account and data",
                    "Export your conversation history",
                ],
            },
            {
                "title": "Cookies and Tracking",
                "content": "We use cookies and similar technologies to enhance your experience.",
                "details": [
                    "Essential cookies for platform functionality",
                    "Analytics cookies to understand usage patterns",
                    "Preference cookies to remember your settings",
                    "You can control cookie settings in your browser",
                ],
            },
        ],
    }

    return render_template("legal/privacy.html", privacy=privacy_data)


@legal_bp.route("/cookies")
def cookies():
    """Cookie Policy page"""
    cookie_data = {
        "last_updated": "September 17, 2025",
        "company_name": "3-in-1 Platform Services",
        "cookie_types": [
            {
                "type": "Essential Cookies",
                "purpose": "Required for basic platform functionality",
                "examples": ["Session management", "Authentication", "Security"],
                "can_disable": False,
                "duration": "Session or 30 days",
            },
            {
                "type": "Functional Cookies",
                "purpose": "Remember your preferences and settings",
                "examples": [
                    "Language preferences",
                    "Theme settings",
                    "Agent preferences",
                ],
                "can_disable": True,
                "duration": "1 year",
            },
            {
                "type": "Analytics Cookies",
                "purpose": "Help us understand how you use the platform",
                "examples": ["Page views", "Feature usage", "Performance metrics"],
                "can_disable": True,
                "duration": "2 years",
            },
            {
                "type": "Marketing Cookies",
                "purpose": "Show relevant advertisements and track campaigns",
                "examples": [
                    "Ad preferences",
                    "Campaign tracking",
                    "Social media integration",
                ],
                "can_disable": True,
                "duration": "1 year",
            },
        ],
        "third_party_cookies": [
            {
                "provider": "Google Analytics",
                "purpose": "Website analytics and performance monitoring",
                "privacy_policy": "https://policies.google.com/privacy",
            },
            {
                "provider": "Stripe",
                "purpose": "Payment processing and fraud prevention",
                "privacy_policy": "https://stripe.com/privacy",
            },
            {
                "provider": "PayPal",
                "purpose": "Alternative payment processing",
                "privacy_policy": "https://www.paypal.com/privacy",
            },
        ],
    }

    return render_template("legal/cookies.html", cookies=cookie_data)


@legal_bp.route("/payments")
def payments():
    """Payment Policy page"""
    payment_data = {
        "last_updated": "September 17, 2025",
        "company_name": "3-in-1 Platform Services",
        "sections": [
            {
                "title": "Accepted Payment Methods",
                "content": "We accept various payment methods for different services.",
                "methods": [
                    "Credit/Debit Cards (Visa, MasterCard, American Express)",
                    "PayPal Account",
                    "Bank Transfer (for enterprise services)",
                    "Cryptocurrency (Bitcoin, Ethereum - enterprise only)",
                ],
            },
            {
                "title": "Web Development Services",
                "content": "Payment terms for custom web development projects.",
                "terms": [
                    "50% deposit required to start project",
                    "50% balance due upon project completion",
                    "Payment due within 30 days of invoice",
                    "Late payments subject to 1.5% monthly interest",
                    "Refunds available for unused work (prorated)",
                ],
            },
            {
                "title": "AI Service Subscriptions",
                "content": "Subscription billing and management policies.",
                "terms": [
                    "Monthly or annual billing cycles",
                    "Auto-renewal unless cancelled",
                    "Prorated refunds for cancellations",
                    "No refunds for partial month usage",
                    "7-day free trial for new users",
                ],
            },
            {
                "title": "Security and Processing",
                "content": "Payment security and data protection measures.",
                "measures": [
                    "PCI DSS compliant payment processing",
                    "SSL encryption for all transactions",
                    "No storage of credit card information",
                    "Fraud detection and prevention",
                    "Secure tokenization of payment methods",
                ],
            },
            {
                "title": "Refund Policy",
                "content": "Conditions and procedures for requesting refunds.",
                "conditions": [
                    "Web development: Full refund if project not started",
                    "AI subscriptions: Prorated refund for unused time",
                    "Refund requests must be submitted within 30 days",
                    "Refunds processed within 5-10 business days",
                    "Chargebacks may result in account suspension",
                ],
            },
            {
                "title": "Disputes and Support",
                "content": "How to resolve payment disputes and get support.",
                "procedures": [
                    "Contact support before initiating chargebacks",
                    "Provide detailed information about the dispute",
                    "Allow 48 hours for initial response",
                    "Escalation to management if unresolved",
                    "Legal mediation for complex disputes",
                ],
            },
        ],
    }

    return render_template("legal/payments.html", payments=payment_data)


@legal_bp.route("/api/consent", methods=["POST"])
def cookie_consent():
    """Handle cookie consent preferences"""
    try:
        data = request.get_json()
        consent_preferences = {
            "essential": True,  # Always required
            "functional": data.get("functional", False),
            "analytics": data.get("analytics", False),
            "marketing": data.get("marketing", False),
            "timestamp": datetime.now().isoformat(),
        }

        # Store consent in session (in production, store in database)
        from flask import session

        session["cookie_consent"] = consent_preferences

        return jsonify(
            {
                "success": True,
                "message": "Cookie preferences saved",
                "preferences": consent_preferences,
            }
        )

    except Exception as e:
        logger.error(f"Error saving cookie consent: {e}")
        return jsonify({"error": "Failed to save preferences"}), 500


@legal_bp.route("/api/data-request", methods=["POST"])
def data_request():
    """Handle user data requests (access, deletion, export)"""
    try:
        data = request.get_json()
        request_type = data.get("type")  # 'access', 'delete', 'export'
        user_email = data.get("email")

        if not request_type or not user_email:
            return jsonify({"error": "Missing required fields"}), 400

        # In production, this would create a ticket in a support system
        # For now, we'll just log the request
        logger.info(f"Data request received: {request_type} for {user_email}")

        request_id = f"DR-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return jsonify(
            {
                "success": True,
                "message": f"Your {request_type} request has been submitted",
                "request_id": request_id,
                "estimated_completion": "5-10 business days",
            }
        )

    except Exception as e:
        logger.error(f"Error processing data request: {e}")
        return jsonify({"error": "Failed to process request"}), 500


# Error handlers
@legal_bp.errorhandler(404)
def legal_not_found(error):
    """Custom 404 handler for legal pages"""
    return render_template("legal/404.html"), 404


@legal_bp.errorhandler(500)
def legal_internal_error(error):
    """Custom 500 handler for legal pages"""
    return render_template("legal/500.html"), 500
