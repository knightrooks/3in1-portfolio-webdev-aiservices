"""
Gossipqueen Agent Analytics Package
Comprehensive analytics suite for Social dynamics and networking specialist performance.
"""

from .metrics import GossipqueenMetrics
from .logger import GossipqueenAnalyticsLogger, gossipqueen_analytics_logger

# Initialize gossipqueen analytics system
gossipqueen_metrics = GossipqueenMetrics()
analytics_logger = gossipqueen_analytics_logger

__all__ = [
    "GossipqueenMetrics",
    "GossipqueenAnalyticsLogger",
    "gossipqueen_metrics",
    "gossipqueen_analytics_logger",
    "analytics_logger",
]

# Version info
__version__ = "1.0.0"
__author__ = "AI Portfolio Platform"
__description__ = "Advanced analytics system for Gossipqueen AI agent"
