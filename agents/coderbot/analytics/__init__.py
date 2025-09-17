"""
Coderbot Agent Analytics Package
Comprehensive analytics suite for Enthusiastic coding companion performance.
"""

from .metrics import CoderbotMetrics
from .logger import CoderbotAnalyticsLogger, coderbot_analytics_logger

# Initialize coderbot analytics system
coderbot_metrics = CoderbotMetrics()
analytics_logger = coderbot_analytics_logger

__all__ = [
    "CoderbotMetrics",
    "CoderbotAnalyticsLogger",
    "coderbot_metrics",
    "coderbot_analytics_logger",
    "analytics_logger",
]

# Version info
__version__ = "1.0.0"
__author__ = "AI Portfolio Platform"
__description__ = "Advanced analytics system for Coderbot AI agent"
