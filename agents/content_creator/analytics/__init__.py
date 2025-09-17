"""
Content Creator Agent Analytics Package
Comprehensive analytics suite for Content strategy and creative development performance.
"""

from .metrics import ContentCreatorMetrics
from .logger import ContentCreatorAnalyticsLogger, content_creator_analytics_logger

# Initialize content creator analytics system
content_creator_metrics = ContentCreatorMetrics()
analytics_logger = content_creator_analytics_logger

__all__ = [
    'ContentCreatorMetrics',
    'ContentCreatorAnalyticsLogger', 
    'content_creator_metrics',
    'content_creator_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Content Creator AI agent'
