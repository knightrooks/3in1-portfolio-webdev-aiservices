"""
Research Analyst Agent Analytics Package
Comprehensive analytics suite for Market research and competitive analysis performance.
"""

from .metrics import ResearchAnalystMetrics
from .logger import ResearchAnalystAnalyticsLogger, research_analyst_analytics_logger

# Initialize research analyst analytics system
research_analyst_metrics = ResearchAnalystMetrics()
analytics_logger = research_analyst_analytics_logger

__all__ = [
    "ResearchAnalystMetrics",
    "ResearchAnalystAnalyticsLogger",
    "research_analyst_metrics",
    "research_analyst_analytics_logger",
    "analytics_logger",
]

# Version info
__version__ = "1.0.0"
__author__ = "AI Portfolio Platform"
__description__ = "Advanced analytics system for Research Analyst AI agent"
