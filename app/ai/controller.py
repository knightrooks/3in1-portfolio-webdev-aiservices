"""
AI Controller - Central orchestrator for AI models and tasks
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import yaml
import json

from .planner import TaskPlanner
from .executor import TaskExecutor
from .memory import MemoryManager

class AIController:
    """Central AI controller that manages models, tasks, and orchestration."""
    
    def __init__(self, config_path: str = None):
        """Initialize the AI Controller."""
        self.config_path = config_path or 'app/ai/registry.yaml'
        self.planner = TaskPlanner()
        self.executor = TaskExecutor()
        self.memory = MemoryManager()
        self.models = {}
        self.agents = {}
        self.active_sessions = {}
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Load configuration
        self._load_config()
        self._initialize_models()
    
    def _load_config(self):
        """Load AI configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file {self.config_path} not found. Using defaults.")
            self.config = {
                'models': {},
                'agents': {},
                'settings': {
                    'max_concurrent_tasks': 5,
                    'default_timeout': 300,
                    'memory_limit': 1000
                }
            }
    
    def _initialize_models(self):
        """Initialize all available AI models."""
        for model_name, model_config in self.config.get('models', {}).items():
            try:
                # Import and initialize model
                model_class = self._import_model_class(model_config['class'])
                self.models[model_name] = model_class(model_config)
                self.logger.info(f"Initialized model: {model_name}")
            except Exception as e:
                self.logger.error(f"Failed to initialize model {model_name}: {e}")
    
    def _import_model_class(self, class_path: str):
        """Dynamically import model class."""
        module_path, class_name = class_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)
    
    async def create_session(self, agent_type: str, user_id: str = None, context: Dict = None) -> str:
        """Create a new AI session."""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id or 'anonymous'}"
        
        session_data = {
            'id': session_id,
            'agent_type': agent_type,
            'user_id': user_id,
            'context': context or {},
            'created_at': datetime.now().isoformat(),
            'messages': [],
            'state': 'active'
        }
        
        self.active_sessions[session_id] = session_data
        self.logger.info(f"Created session {session_id} for agent {agent_type}")
        
        return session_id
    
    async def process_message(self, session_id: str, message: str, attachments: List = None) -> Dict:
        """Process a message within a session."""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        agent_type = session['agent_type']
        
        # Add message to session history
        message_data = {
            'id': len(session['messages']) + 1,
            'timestamp': datetime.now().isoformat(),
            'content': message,
            'attachments': attachments or [],
            'type': 'user'
        }
        session['messages'].append(message_data)
        
        # Plan the response
        task_plan = await self.planner.create_plan(
            message=message,
            agent_type=agent_type,
            context=session['context'],
            history=session['messages']
        )
        
        # Execute the plan
        response = await self.executor.execute_plan(
            plan=task_plan,
            models=self.models,
            session_context=session
        )
        
        # Add response to session
        response_data = {
            'id': len(session['messages']) + 1,
            'timestamp': datetime.now().isoformat(),
            'content': response['content'],
            'metadata': response.get('metadata', {}),
            'type': 'assistant'
        }
        session['messages'].append(response_data)
        
        # Update memory
        await self.memory.store_interaction(
            session_id=session_id,
            user_message=message,
            assistant_response=response['content'],
            context=response.get('metadata', {})
        )
        
        return response
    
    async def get_session(self, session_id: str) -> Dict:
        """Get session data."""
        if session_id not in self.active_sessions:
            return None
        return self.active_sessions[session_id]
    
    async def list_sessions(self, user_id: str = None) -> List[Dict]:
        """List all sessions, optionally filtered by user."""
        sessions = list(self.active_sessions.values())
        if user_id:
            sessions = [s for s in sessions if s.get('user_id') == user_id]
        return sessions
    
    async def close_session(self, session_id: str):
        """Close and archive a session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session['state'] = 'closed'
            session['closed_at'] = datetime.now().isoformat()
            
            # Archive to memory
            await self.memory.archive_session(session)
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            self.logger.info(f"Closed session {session_id}")
    
    def get_model_status(self) -> Dict:
        """Get status of all models."""
        status = {}
        for name, model in self.models.items():
            status[name] = {
                'status': getattr(model, 'status', 'unknown'),
                'last_used': getattr(model, 'last_used', None),
                'total_requests': getattr(model, 'request_count', 0)
            }
        return status
    
    def get_system_stats(self) -> Dict:
        """Get system statistics."""
        return {
            'active_sessions': len(self.active_sessions),
            'total_models': len(self.models),
            'memory_usage': self.memory.get_usage_stats(),
            'uptime': datetime.now().isoformat()
        }

# Global AI controller instance
ai_controller = None

def get_ai_controller() -> AIController:
    """Get or create the global AI controller instance."""
    global ai_controller
    if ai_controller is None:
        ai_controller = AIController()
    return ai_controller

def initialize_ai_system():
    """Initialize the AI system."""
    global ai_controller
    ai_controller = AIController()
    return ai_controller