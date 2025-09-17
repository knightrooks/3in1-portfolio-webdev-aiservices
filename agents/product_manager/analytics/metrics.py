"""
Product Manager Agent Analytics Metrics
Product strategy and roadmap planning analytics and performance tracking.
"""

import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path for base analytics
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from base_analytics import PerformanceTracker, ConversationMetrics


class ProductManagerMetrics(PerformanceTracker):
    """Specialized metrics tracking for the Product Manager agent."""

    def __init__(self, agent_name: str = "product_manager"):
        super().__init__(agent_name)

        # Product Manager-specific metrics
        self.specialized_metrics = {
            "feature_planning": 0,
            "roadmap_creation": 0,
            "stakeholder_management": 0,
            "market_research": 0,
        }

        self.conversation_types = {
            "product_planning": 0,
            "feature_specification": 0,
            "roadmap_review": 0,
            "market_analysis": 0,
        }

        self.deliverables = {
            "product_specs": 0,
            "roadmaps": 0,
            "feature_docs": 0,
            "market_research": 0,
        }

        self.business_impact = "very_high"

    def track_consultation(
        self,
        consultation_type: str,
        complexity: str = "moderate",
        deliverable_type: str = "consultation",
        execution_time: float = 0.0,
    ):
        """Track a product manager consultation request."""
        conversation_metrics = ConversationMetrics(
            user_id=f"user_{datetime.now().timestamp()}",
            conversation_id=f"product_manager_{datetime.now().timestamp()}",
            start_time=datetime.now(),
            agent_name=self.agent_name,
            conversation_type=consultation_type,
            custom_metrics={
                "consultation_type": consultation_type,
                "complexity": complexity,
                "deliverable_type": deliverable_type,
                "business_impact": self.business_impact,
            },
        )

        conversation_metrics.end_time = datetime.now()
        conversation_metrics.total_duration = execution_time or 2.5  # Default duration
        conversation_metrics.success = True
        conversation_metrics.satisfaction_score = 4.3  # Default high satisfaction

        # Update specialized counters
        if consultation_type in self.specialized_metrics:
            self.specialized_metrics[consultation_type] += 1

        if consultation_type in self.conversation_types:
            self.conversation_types[consultation_type] += 1

        if deliverable_type in self.deliverables:
            self.deliverables[deliverable_type] += 1

        self.add_conversation(conversation_metrics)

    def get_specialized_insights(self) -> Dict[str, Any]:
        """Product Manager performance insights."""
        total_consultations = sum(self.specialized_metrics.values())

        insights = {
            "most_requested_service": (
                max(self.specialized_metrics.items(), key=lambda x: x[1])[0]
                if total_consultations > 0
                else None
            ),
            "conversation_distribution": dict(self.conversation_types),
            "popular_deliverables": sorted(
                self.deliverables.items(), key=lambda x: x[1], reverse=True
            ),
            "avg_consultation_duration": self.get_avg_response_time(),
            "success_rate": len([c for c in self.conversations if c.success])
            / max(len(self.conversations), 1)
            * 100,
            "business_impact_level": self.business_impact,
            "specialization_focus": "Product strategy and roadmap planning",
        }

        return insights

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive product manager performance report."""
        base_metrics = self.get_metrics_summary()
        specialized_insights = self.get_specialized_insights()

        return {
            "agent_name": self.agent_name,
            "agent_type": "product_manager",
            "specialization": "Product strategy and roadmap planning",
            "report_type": "performance_analysis",
            "timestamp": datetime.now().isoformat(),
            "base_metrics": base_metrics,
            "specialized_insights": specialized_insights,
            "recommendations": self._generate_recommendations(specialized_insights),
        }

    def _generate_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate recommendations for product manager improvement."""
        recommendations = []

        # Check service distribution
        most_popular = insights.get("most_requested_service")
        if most_popular:
            recommendations.append(
                f"Focus expertise development on {most_popular.replace('_', ' ')} - highest demand area"
            )

        # Check conversation types
        conv_dist = insights.get("conversation_distribution", {})
        if conv_dist:
            top_conversation = max(conv_dist.items(), key=lambda x: x[1])[0]
            recommendations.append(
                f"Enhance {top_conversation.replace('_', ' ')} capabilities and templates"
            )

        # Check deliverable preferences
        popular_deliverables = insights.get("popular_deliverables", [])
        if popular_deliverables:
            top_deliverable = popular_deliverables[0][0]
            recommendations.append(
                f"Improve {top_deliverable.replace('_', ' ')} quality and comprehensiveness"
            )

        # Response time recommendations
        avg_duration = insights.get("avg_consultation_duration", 0)
        if avg_duration > 180:  # 3 minutes
            recommendations.append(
                "Optimize consultation processes to reduce response time"
            )
        elif avg_duration < 30:  # 30 seconds
            recommendations.append(
                "Consider providing more thorough analysis and recommendations"
            )

        return recommendations
