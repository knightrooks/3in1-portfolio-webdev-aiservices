"""
Security Expert Agent Analytics Package
Comprehensive analytics suite for Cybersecurity and risk assessment performance.
"""

from .metrics import SecurityExpertMetrics
from .logger import SecurityExpertAnalyticsLogger, security_expert_analytics_logger

# Initialize security expert analytics system
security_expert_metrics = SecurityExpertMetrics()
analytics_logger = security_expert_analytics_logger

__all__ = [
    "SecurityExpertMetrics",
    "SecurityExpertAnalyticsLogger",
    "security_expert_metrics",
    "security_expert_analytics_logger",
    "analytics_logger",
]

# Version info
__version__ = "1.0.0"
__author__ = "AI Portfolio Platform"
__description__ = "Advanced analytics system for Security Expert AI agent"
