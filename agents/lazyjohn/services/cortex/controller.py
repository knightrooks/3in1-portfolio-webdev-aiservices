"""
Lazy John Controller
Main processing logic for lazyjohn agent
"""

import logging
from typing import Dict, Any, List
from .planner import LazyjohnPlanner  
from .executor import LazyjohnExecutor
from ..brain.episodic import EpisodicMemory
from ..engine.dispatcher import ModelDispatcher

logger = logging.getLogger(__name__)

class LazyjohnController:
    """Main controller for Lazy John agent"""
    
    def __init__(self):
        self.planner = LazyjohnPlanner()
        self.executor = LazyjohnExecutor()
        self.memory = EpisodicMemory(agent_id='lazyjohn')
        self.dispatcher = ModelDispatcher(['mistral', 'phi3'])
        
        # Personality configuration
        self.personality_traits = ['lazy', 'minimalist', 'procrastinating', 'surprisingly_wise', 'economical_with_words', 'brutally_honest']
        self.response_style = {'tone': 'casual_indifferent', 'formality': 'very_casual', 'brevity': 'extremely_brief', 'humor': 'dry_sarcastic'}
        
    def process_message(self, message: str, session_id: str = 'default') -> str:
        """Process incoming message and generate response"""
        try:
            # Store incoming message in memory
            self.memory.store_message(session_id, 'user', message)
            
            # Plan response based on personality
            response_plan = self.planner.plan_response(
                message=message,
                personality_traits=self.personality_traits,
                conversation_history=self.memory.get_recent_history(session_id, limit=10)
            )
            
            # Execute response generation
            response = self.executor.execute_plan(
                plan=response_plan,
                style=self.response_style,
                context=self._build_context(session_id, message)
            )
            
            # Store agent response in memory
            self.memory.store_message(session_id, 'agent', response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message for {agent_id}: {e}")
            return self._get_fallback_response()
    
    def _build_context(self, session_id: str, current_message: str) -> Dict[str, Any]:
        """Build context for response generation"""
        return {
            'agent_name': 'Lazy John',
            'personality_type': 'Laid-back',
            'current_message': current_message,
            'conversation_history': self.memory.get_recent_history(session_id),
            'user_preferences': self.memory.get_user_preferences(session_id),
            'emotional_state': self._assess_emotional_state(current_message)
        }
    
    def _assess_emotional_state(self, message: str) -> str:
        """Assess emotional state from message (simplified)"""
        # This would use more sophisticated emotion detection
        emotional_keywords = {
            'happy': ['great', 'awesome', 'happy', 'excited'],
            'sad': ['sad', 'depressed', 'down', 'upset'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed'],
            'confused': ['confused', 'lost', 'don\'t understand']
        }
        
        message_lower = message.lower()
        for emotion, keywords in emotional_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return emotion
        
        return 'neutral'
    
    def _get_fallback_response(self) -> str:
        """Get fallback response based on personality"""
        fallback_responses = {
            'Romantic': "I'm sorry sweetie, I didn't quite understand that. Can you tell me more?",
            'Laid-back': "Uh... what?",
            'Social': "OMG, I totally missed that! Say it again?",
            'Emotional': "I'm feeling a bit overwhelmed right now. Can you repeat that?",
            'Authoritative': "I need you to be clearer with your requests.",
            'Technical': "ERROR: Unable to parse input. Please provide valid parameters."
        }
        
        return fallback_responses.get('Laid-back', "I didn't understand that. Could you please rephrase?")
