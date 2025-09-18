"""
Developer Agent Analytics Package
Comprehensive analytics suite for Full-stack development and coding performance.
"""

from .metrics import DeveloperMetrics
from .logger import DeveloperAnalyticsLogger, developer_analytics_logger

# Initialize developer analytics system
developer_metrics = DeveloperMetrics()
analytics_logger = developer_analytics_logger

__all__ = [
    "DeveloperMetrics",
    "DeveloperAnalyticsLogger",
    "developer_metrics",
    "developer_analytics_logger",
    "analytics_logger",
]

# Version info
__version__ = "1.0.0"
__author__ = "AI Portfolio Platform"
__description__ = "Advanced analytics system for Developer AI agent"
