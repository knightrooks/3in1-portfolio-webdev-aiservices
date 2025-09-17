"""
Marketing Specialist Agent Analytics Package
Comprehensive analytics suite for Marketing strategy and campaign management performance.
"""

from .metrics import MarketingSpecialistMetrics
from .logger import MarketingSpecialistAnalyticsLogger, marketing_specialist_analytics_logger

# Initialize marketing specialist analytics system
marketing_specialist_metrics = MarketingSpecialistMetrics()
analytics_logger = marketing_specialist_analytics_logger

__all__ = [
    'MarketingSpecialistMetrics',
    'MarketingSpecialistAnalyticsLogger', 
    'marketing_specialist_metrics',
    'marketing_specialist_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Marketing Specialist AI agent'
