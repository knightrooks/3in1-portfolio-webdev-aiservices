"""
Research Analyst Agent Analytics Logger
Advanced logging for Market research and competitive analysis activities.
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path for base analytics
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class ResearchAnalystAnalyticsLogger:
    """Advanced analytics logger for Research Analyst agent."""

    def __init__(self, log_level: str = "INFO"):
        self.agent_name = "research_analyst"
        self.setup_logger(log_level)

    def setup_logger(self, log_level: str):
        """Setup specialized logging for research analyst activities."""
        # Create logs directory if it doesn't exist
        log_dir = "logs/agents/research_analyst"
        os.makedirs(log_dir, exist_ok=True)

        # Main research_analyst logger
        self.logger = logging.getLogger(f"{self.agent_name}_analytics")
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Clear existing handlers
        self.logger.handlers.clear()

        # File handlers for different log types
        general_handler = logging.FileHandler(
            f"{log_dir}/research_analyst_activities.log"
        )
        consultation_handler = logging.FileHandler(
            f"{log_dir}/research_analyst_consultations.log"
        )
        metrics_handler = logging.FileHandler(f"{log_dir}/performance_metrics.log")
        error_handler = logging.FileHandler(f"{log_dir}/errors.log")

        # Set levels
        general_handler.setLevel(logging.INFO)
        consultation_handler.setLevel(logging.INFO)
        metrics_handler.setLevel(logging.DEBUG)
        error_handler.setLevel(logging.ERROR)

        # Formatters
        detailed_formatter = logging.Formatter(
            "%%(asctime)s | %%(name)s | %%(levelname)s | %%(funcName)s:%%(lineno)d | %%(message)s"
        )

        consultation_formatter = logging.Formatter(
            "%%(asctime)s | CONSULTATION | %%(message)s"
        )

        metrics_formatter = logging.Formatter("%%(asctime)s | METRICS | %%(message)s")

        # Apply formatters
        general_handler.setFormatter(detailed_formatter)
        consultation_handler.setFormatter(consultation_formatter)
        metrics_handler.setFormatter(metrics_formatter)
        error_handler.setFormatter(detailed_formatter)

        # Add handlers to logger
        self.logger.addHandler(general_handler)
        self.logger.addHandler(consultation_handler)
        self.logger.addHandler(metrics_handler)
        self.logger.addHandler(error_handler)

        # Separate loggers for specific activities
        self.consultation_logger = logging.getLogger(f"{self.agent_name}_consultations")
        self.consultation_logger.addHandler(consultation_handler)
        self.consultation_logger.setLevel(logging.INFO)

        self.metrics_logger = logging.getLogger(f"{self.agent_name}_metrics")
        self.metrics_logger.addHandler(metrics_handler)
        self.metrics_logger.setLevel(logging.DEBUG)

    def log_consultation_request(
        self, user_id: str, consultation_type: str, complexity: str = "moderate"
    ):
        """Log a new research analyst consultation request."""
        self.consultation_logger.info(
            f"USER_REQUEST | user_id={user_id} | consultation_type={consultation_type} | "
            f"complexity={complexity} | timestamp={datetime.now().isoformat()}"
        )

    def log_consultation_completion(
        self,
        conversation_id: str,
        total_duration: float,
        satisfaction_score: float,
        deliverable_count: int,
    ):
        """Log research analyst consultation completion."""
        self.consultation_logger.info(
            f"CONSULTATION_COMPLETED | conversation_id={conversation_id} | "
            f"total_duration={total_duration:.2f}s | satisfaction={satisfaction_score} | "
            f"deliverables={deliverable_count} | timestamp={datetime.now().isoformat()}"
        )

    def log_performance_metrics(self, metrics_data: Dict[str, Any]):
        """Log performance metrics update."""
        self.metrics_logger.debug(
            f"METRICS_UPDATE | response_time={metrics_data.get('avg_response_time', 0):.2f}s | "
            f"success_rate={metrics_data.get('success_rate', 0):.1f}% | "
            f"satisfaction={metrics_data.get('avg_satisfaction', 0):.2f} | "
            f"consultations_today={metrics_data.get('consultations_today', 0)} | "
            f"timestamp={datetime.now().isoformat()}"
        )

    def log_business_impact(
        self, conversation_id: str, impact_category: str, impact_level: str = "high"
    ):
        """Log business impact assessment."""
        self.consultation_logger.info(
            f"BUSINESS_IMPACT | conversation_id={conversation_id} | "
            f"category={impact_category} | level={impact_level} | "
            f"timestamp={datetime.now().isoformat()}"
        )

    def log_error(
        self, error_type: str, error_message: str, conversation_id: Optional[str] = None
    ):
        """Log errors in research analyst consultation process."""
        error_msg = f"CONSULTATION_ERROR | type={error_type} | message={error_message}"
        if conversation_id:
            error_msg += f" | conversation_id={conversation_id}"
        error_msg += f" | timestamp={datetime.now().isoformat()}"

        self.logger.error(error_msg)

    def get_log_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get summary of logged activities."""
        try:
            log_file = f"logs/agents/research_analyst/research_analyst_activities.log"
            return {
                "agent_name": "research_analyst",
                "agent_type": "Market research and competitive analysis",
                "period_hours": hours,
                "log_files_available": [
                    f"research_analyst_activities.log",
                    f"research_analyst_consultations.log",
                    "performance_metrics.log",
                    "errors.log",
                ],
                "last_updated": datetime.now().isoformat(),
                "status": "active",
            }

        except Exception as e:
            self.log_error("LOG_SUMMARY_ERROR", str(e))
            return {"error": f"Failed to generate log summary: {str(e)}"}


# Global logger instance
research_analyst_analytics_logger = ResearchAnalystAnalyticsLogger()
