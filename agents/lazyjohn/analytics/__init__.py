"""
Lazyjohn Agent Analytics Package
Comprehensive analytics suite for Productivity and motivation coach performance.
"""

from .metrics import LazyjohnMetrics
from .logger import LazyjohnAnalyticsLogger, lazyjohn_analytics_logger

# Initialize lazyjohn analytics system
lazyjohn_metrics = LazyjohnMetrics()
analytics_logger = lazyjohn_analytics_logger

__all__ = [
    'LazyjohnMetrics',
    'LazyjohnAnalyticsLogger', 
    'lazyjohn_metrics',
    'lazyjohn_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Lazyjohn AI agent'
