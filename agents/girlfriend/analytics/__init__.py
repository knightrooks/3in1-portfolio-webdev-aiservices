"""
Girlfriend Agent Analytics Package
Comprehensive analytics suite for Supportive companion and advisor performance.
"""

from .metrics import GirlfriendMetrics
from .logger import GirlfriendAnalyticsLogger, girlfriend_analytics_logger

# Initialize girlfriend analytics system
girlfriend_metrics = GirlfriendMetrics()
analytics_logger = girlfriend_analytics_logger

__all__ = [
    'GirlfriendMetrics',
    'GirlfriendAnalyticsLogger', 
    'girlfriend_metrics',
    'girlfriend_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Girlfriend AI agent'
