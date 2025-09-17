"""
Business Strategist AI Controller
Main orchestration controller for strategist agent
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from .planner import StrategistPlanner
from .executor import StrategistExecutor
from ..brain.episodic import EpisodicMemory
from ..engine.dispatcher import ModelDispatcher

logger = logging.getLogger(__name__)

class StrategistController:
    """Main controller for Business Strategist AI"""
    
    def __init__(self):
        self.planner = StrategistPlanner()
        self.executor = StrategistExecutor()
        self.memory = EpisodicMemory('strategist')
        self.dispatcher = ModelDispatcher('strategist')
        
        self.session_data = {}
        self.performance_metrics = {
            'requests_processed': 0,
            'average_response_time': 0.0,
            'success_rate': 0.0,
            'user_satisfaction': 0.0
        }
        
        logger.info(f"Initialized {self.__class__.__name__}")
    
    async def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """Process incoming message and generate response"""
        start_time = datetime.now()
        
        try:
            # Initialize session if new
            if session_id not in self.session_data:
                self.session_data[session_id] = {
                    'created_at': start_time,
                    'conversation_history': [],
                    'user_profile': {},
                    'context': {}
                }
            
            session = self.session_data[session_id]
            
            # Plan the response approach
            plan = await self.planner.create_plan(message, session)
            
            # Execute the plan
            response = await self.executor.execute_plan(plan, session)
            
            # Store in memory
            await self.memory.store_interaction(session_id, message, response)
            
            # Update session
            session['conversation_history'].append({
                'timestamp': start_time.isoformat(),
                'user_message': message,
                'agent_response': response.get('content', ''),
                'confidence': response.get('confidence', 0.0)
            })
            
            # Update metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(processing_time, response.get('success', True))
            
            return {
                'response': response.get('content', ''),
                'confidence': response.get('confidence', 0.0),
                'session_id': session_id,
                'processing_time': processing_time,
                'agent': 'strategist',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                'error': str(e),
                'agent': 'strategist',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health status"""
        return {
            'agent': 'strategist',
            'status': 'healthy',
            'uptime': datetime.now().isoformat(),
            'active_sessions': len(self.session_data),
            'performance_metrics': self.performance_metrics
        }
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            'Expert in business strategy, market analysis, and strategic planning',
            'Multi-model intelligence',
            'Context-aware responses',
            'Session management',
            'Performance monitoring'
        ]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.performance_metrics
    
    def _update_metrics(self, processing_time: float, success: bool):
        """Update performance metrics"""
        self.performance_metrics['requests_processed'] += 1
        
        # Update average response time
        current_avg = self.performance_metrics['average_response_time']
        total_requests = self.performance_metrics['requests_processed']
        self.performance_metrics['average_response_time'] = (
            (current_avg * (total_requests - 1) + processing_time) / total_requests
        )
        
        # Update success rate
        if success:
            current_success = self.performance_metrics['success_rate']
            self.performance_metrics['success_rate'] = (
                (current_success * (total_requests - 1) + 1.0) / total_requests
            )