"""
Strictwife Agent Analytics Package
Comprehensive analytics suite for Accountability and discipline coach performance.
"""

from .metrics import StrictwifeMetrics
from .logger import StrictwifeAnalyticsLogger, strictwife_analytics_logger

# Initialize strictwife analytics system
strictwife_metrics = StrictwifeMetrics()
analytics_logger = strictwife_analytics_logger

__all__ = [
    'StrictwifeMetrics',
    'StrictwifeAnalyticsLogger', 
    'strictwife_metrics',
    'strictwife_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Strictwife AI agent'
