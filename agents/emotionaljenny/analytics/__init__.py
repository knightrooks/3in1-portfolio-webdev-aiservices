"""
Emotionaljenny Agent Analytics Package
Comprehensive analytics suite for Emotional intelligence and empathy specialist performance.
"""

from .metrics import EmotionaljennyMetrics
from .logger import EmotionaljennyAnalyticsLogger, emotionaljenny_analytics_logger

# Initialize emotionaljenny analytics system
emotionaljenny_metrics = EmotionaljennyMetrics()
analytics_logger = emotionaljenny_analytics_logger

__all__ = [
    'EmotionaljennyMetrics',
    'EmotionaljennyAnalyticsLogger', 
    'emotionaljenny_metrics',
    'emotionaljenny_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Emotionaljenny AI agent'
