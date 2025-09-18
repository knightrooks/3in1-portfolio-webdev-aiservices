"""
Test Configuration and Fixtures
Provides common test utilities, fixtures, and configuration for the test suite
"""

import os
import sys
import tempfile
from unittest.mock import MagicMock, Mock

import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from config import Config


class TestConfig(Config):
    """Test configuration class"""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-secret-key"

    # Disable external services in tests
    STRIPE_SECRET_KEY = "sk_test_fake_key"
    STRIPE_PUBLISHABLE_KEY = "pk_test_fake_key"
    PAYPAL_CLIENT_ID = "test_paypal_client"
    PAYPAL_CLIENT_SECRET = "test_paypal_secret"
    PAYPAL_MODE = "sandbox"


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test runner"""
    return app.test_cli_runner()


@pytest.fixture
def mock_payment_processor():
    """Mock payment processor for testing"""
    mock = MagicMock()
    mock.calculate_agent_price.return_value = 5.00
    mock.create_stripe_payment_intent.return_value = {
        "success": True,
        "client_secret": "pi_test_client_secret",
        "payment_intent_id": "pi_test_123",
        "amount": 5.00,
        "currency": "usd",
    }
    mock.create_paypal_payment.return_value = {
        "success": True,
        "payment_id": "PAY-test-123",
        "approval_url": "https://paypal.com/approve",
        "amount": 5.00,
    }
    mock.check_subscription_access.return_value = {
        "has_access": True,
        "subscription": {
            "tier": "weekly",
            "end_date": "2024-01-15T00:00:00",
            "usage_count": 5,
            "max_usage": -1,
            "days_remaining": 5,
        },
    }
    return mock


@pytest.fixture
def mock_ai_agent():
    """Mock AI agent for testing"""
    mock = MagicMock()
    mock.process_message.return_value = "Test AI response"
    mock.get_agent_info.return_value = {
        "id": "test_agent",
        "name": "Test Agent",
        "description": "Test AI Agent",
        "icon": "🤖",
        "status": "online",
    }
    return mock


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {"id": "test_user_123", "email": "test@example.com", "name": "Test User"}


@pytest.fixture
def sample_project_data():
    """Sample web development project data"""
    return {
        "project_type": "business_website",
        "features": ["responsive_design", "contact_form", "seo_optimization"],
        "timeline": "standard",
        "pages": 5,
        "budget": 1500,
    }


@pytest.fixture
def sample_agent_subscription():
    """Sample agent subscription data"""
    return {
        "user_id": "test_user_123",
        "agent_id": "strategist",
        "tier": "weekly",
        "payment_method": "stripe",
        "status": "active",
    }


class MockResponse:
    """Mock HTTP response for testing external APIs"""

    def __init__(self, json_data=None, status_code=200, text=""):
        self.json_data = json_data or {}
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data

    @property
    def ok(self):
        return self.status_code < 400


# Test utilities
def assert_template_used(client, endpoint, template_name):
    """Assert that a specific template was used for rendering"""
    with client.application.test_request_context():
        response = client.get(endpoint)
        assert template_name in str(response.data)


def assert_contains_text(response, text):
    """Assert that response contains specific text"""
    assert text.encode() in response.data


def assert_json_response(response, expected_keys=None):
    """Assert valid JSON response with expected keys"""
    assert response.content_type == "application/json"
    json_data = response.get_json()
    assert json_data is not None

    if expected_keys:
        for key in expected_keys:
            assert key in json_data

    return json_data


def create_temp_file(content="", extension=".txt"):
    """Create temporary file for testing"""
    fd, path = tempfile.mkstemp(suffix=extension)
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path


def mock_env_vars(monkeypatch, **env_vars):
    """Mock environment variables for testing"""
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
