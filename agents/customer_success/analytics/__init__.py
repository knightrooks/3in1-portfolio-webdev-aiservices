"""
Customer Success Agent Analytics Package
Comprehensive analytics suite for Customer relationship and success management performance.
"""

from .metrics import CustomerSuccessMetrics
from .logger import CustomerSuccessAnalyticsLogger, customer_success_analytics_logger

# Initialize customer success analytics system
customer_success_metrics = CustomerSuccessMetrics()
analytics_logger = customer_success_analytics_logger

__all__ = [
    "CustomerSuccessMetrics",
    "CustomerSuccessAnalyticsLogger",
    "customer_success_metrics",
    "customer_success_analytics_logger",
    "analytics_logger",
]

# Version info
__version__ = "1.0.0"
__author__ = "AI Portfolio Platform"
__description__ = "Advanced analytics system for Customer Success AI agent"
