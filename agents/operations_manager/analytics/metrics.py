"""
Operations Manager Agent Analytics Metrics
Operations optimization and process management analytics and performance tracking.
"""

import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path for base analytics
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from base_analytics import PerformanceTracker, ConversationMetrics

class OperationsManagerMetrics(PerformanceTracker):
    """Specialized metrics tracking for the Operations Manager agent."""
    
    def __init__(self, agent_name: str = "operations_manager"):
        super().__init__(agent_name)
        
        # Operations Manager-specific metrics
        self.specialized_metrics = {'process_optimization': 0, 'workflow_design': 0, 'efficiency_analysis': 0, 'resource_planning': 0}
        
        self.conversation_types = {'operations_review': 0, 'process_improvement': 0, 'workflow_consultation': 0, 'efficiency_audit': 0}
        
        self.deliverables = {'process_maps': 0, 'optimization_reports': 0, 'workflow_diagrams': 0, 'sop_documents': 0}
        
        self.business_impact = "high"
        
    def track_consultation(self, consultation_type: str, complexity: str = "moderate", 
                         deliverable_type: str = "consultation", execution_time: float = 0.0):
        """Track a operations manager consultation request."""
        conversation_metrics = ConversationMetrics(
            user_id=f"user_{datetime.now().timestamp()}",
            conversation_id=f"operations_manager_{datetime.now().timestamp()}",
            start_time=datetime.now(),
            agent_name=self.agent_name,
            conversation_type=consultation_type,
            custom_metrics={
                'consultation_type': consultation_type,
                'complexity': complexity,
                'deliverable_type': deliverable_type,
                'business_impact': self.business_impact
            }
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
        """Operations Manager performance insights."""
        total_consultations = sum(self.specialized_metrics.values())
        
        insights = {
            'most_requested_service': max(self.specialized_metrics.items(), key=lambda x: x[1])[0] if total_consultations > 0 else None,
            'conversation_distribution': dict(self.conversation_types),
            'popular_deliverables': sorted(self.deliverables.items(), key=lambda x: x[1], reverse=True),
            'avg_consultation_duration': self.get_avg_response_time(),
            'success_rate': len([c for c in self.conversations if c.success]) / max(len(self.conversations), 1) * 100,
            'business_impact_level': self.business_impact,
            'specialization_focus': "Operations optimization and process management"
        }
        
        return insights
        
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive operations manager performance report."""
        base_metrics = self.get_metrics_summary()
        specialized_insights = self.get_specialized_insights()
        
        return {
            'agent_name': self.agent_name,
            'agent_type': 'operations_manager',
            'specialization': 'Operations optimization and process management',
            'report_type': 'performance_analysis',
            'timestamp': datetime.now().isoformat(),
            'base_metrics': base_metrics,
            'specialized_insights': specialized_insights,
            'recommendations': self._generate_recommendations(specialized_insights)
        }
        
    def _generate_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate recommendations for operations manager improvement."""
        recommendations = []
        
        # Check service distribution
        most_popular = insights.get('most_requested_service')
        if most_popular:
            recommendations.append(f"Focus expertise development on {most_popular.replace('_', ' ')} - highest demand area")
            
        # Check conversation types
        conv_dist = insights.get('conversation_distribution', {})
        if conv_dist:
            top_conversation = max(conv_dist.items(), key=lambda x: x[1])[0]
            recommendations.append(f"Enhance {top_conversation.replace('_', ' ')} capabilities and templates")
            
        # Check deliverable preferences
        popular_deliverables = insights.get('popular_deliverables', [])
        if popular_deliverables:
            top_deliverable = popular_deliverables[0][0]
            recommendations.append(f"Improve {top_deliverable.replace('_', ' ')} quality and comprehensiveness")
            
        # Response time recommendations
        avg_duration = insights.get('avg_consultation_duration', 0)
        if avg_duration > 180:  # 3 minutes
            recommendations.append("Optimize consultation processes to reduce response time")
        elif avg_duration < 30:  # 30 seconds
            recommendations.append("Consider providing more thorough analysis and recommendations")
            
        return recommendations
