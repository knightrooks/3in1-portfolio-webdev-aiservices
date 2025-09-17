"""
Product Manager Agent Analytics Package
Comprehensive analytics suite for Product strategy and roadmap planning performance.
"""

from .metrics import ProductManagerMetrics
from .logger import ProductManagerAnalyticsLogger, product_manager_analytics_logger

# Initialize product manager analytics system
product_manager_metrics = ProductManagerMetrics()
analytics_logger = product_manager_analytics_logger

__all__ = [
    'ProductManagerMetrics',
    'ProductManagerAnalyticsLogger', 
    'product_manager_metrics',
    'product_manager_analytics_logger',
    'analytics_logger'
]

# Version info
__version__ = '1.0.0'
__author__ = 'AI Portfolio Platform'
__description__ = 'Advanced analytics system for Product Manager AI agent'
