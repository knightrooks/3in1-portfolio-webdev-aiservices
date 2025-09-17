"""
Data Scientist Agent Analytics Package
Comprehensive analytics suite for Data analysis and machine learning performance.
"""

from .metrics import DataScientistMetrics
from .logger import DataScientistAnalyticsLogger, data_scientist_analytics_logger

# Initialize data scientist analytics system
data_scientist_metrics = DataScientistMetrics()
analytics_logger = data_scientist_analytics_logger

__all__ = [
    'DataScientistMetrics',
    'DataScientistAnalyticsLogger', 
    'data_scientist_metrics',
    'data_scientist_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Data Scientist AI agent'
