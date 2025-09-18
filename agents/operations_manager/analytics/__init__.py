"""
Operations Manager Agent Analytics Package
Comprehensive analytics suite for Operations optimization and process management performance.
"""

from .metrics import OperationsManagerMetrics
from .logger import (
    OperationsManagerAnalyticsLogger,
    operations_manager_analytics_logger,
)

# Initialize operations manager analytics system
operations_manager_metrics = OperationsManagerMetrics()
analytics_logger = operations_manager_analytics_logger

__all__ = [
    "OperationsManagerMetrics",
    "OperationsManagerAnalyticsLogger",
    "operations_manager_metrics",
    "operations_manager_analytics_logger",
    "analytics_logger",
]

# Version info
__version__ = "1.0.0"
__author__ = "AI Portfolio Platform"
__description__ = "Advanced analytics system for Operations Manager AI agent"
