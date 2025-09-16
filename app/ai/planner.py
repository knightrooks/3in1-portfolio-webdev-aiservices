"""
Task Planner - Intelligent task planning and decomposition
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class TaskPlanner:
    """Plans and decomposes tasks for AI agents."""
    
    def __init__(self):
        """Initialize the task planner."""
        self.logger = logging.getLogger(__name__)
        
        # Task templates for different agent types
        self.agent_templates = {
            'strategist': {
                'capabilities': ['strategic_analysis', 'market_research', 'competitive_analysis', 'business_planning'],
                'default_steps': ['analyze_context', 'identify_objectives', 'develop_strategy', 'create_recommendations']
            },
            'developer': {
                'capabilities': ['code_generation', 'debugging', 'architecture_design', 'testing'],
                'default_steps': ['understand_requirements', 'design_solution', 'implement_code', 'test_solution']
            },
            'content_creator': {
                'capabilities': ['content_writing', 'seo_optimization', 'social_media', 'marketing_copy'],
                'default_steps': ['research_topic', 'create_outline', 'write_content', 'optimize_content']
            },
            'security_expert': {
                'capabilities': ['vulnerability_assessment', 'security_analysis', 'threat_modeling', 'compliance'],
                'default_steps': ['assess_security', 'identify_threats', 'recommend_mitigations', 'create_plan']
            }
        }
    
    async def create_plan(self, message: str, agent_type: str, context: Dict = None, history: List = None) -> Dict:
        """Create a comprehensive task plan."""
        context = context or {}
        history = history or []
        
        # Analyze the user message
        analysis = await self._analyze_message(message, context, history)
        
        # Determine task complexity
        complexity = self._assess_complexity(analysis)
        
        # Get agent capabilities
        agent_config = self.agent_templates.get(agent_type, {})
        
        # Create task breakdown
        tasks = await self._decompose_tasks(analysis, agent_config, complexity)
        
        # Determine required models
        required_models = self._determine_models(tasks, agent_type)
        
        # Create execution plan
        plan = {
            'id': f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'message': message,
            'agent_type': agent_type,
            'analysis': analysis,
            'complexity': complexity,
            'tasks': tasks,
            'required_models': required_models,
            'estimated_duration': self._estimate_duration(tasks),
            'dependencies': self._map_dependencies(tasks),
            'created_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"Created plan {plan['id']} with {len(tasks)} tasks")
        
        return plan
    
    async def _analyze_message(self, message: str, context: Dict, history: List) -> Dict:
        """Analyze the user message to understand intent and requirements."""
        analysis = {
            'intent': self._classify_intent(message),
            'entities': self._extract_entities(message),
            'sentiment': self._analyze_sentiment(message),
            'context_relevance': self._assess_context_relevance(message, context),
            'history_patterns': self._analyze_history_patterns(history),
            'urgency': self._assess_urgency(message),
            'scope': self._determine_scope(message)
        }
        
        return analysis
    
    def _classify_intent(self, message: str) -> str:
        """Classify the intent of the message."""
        # Simple keyword-based classification (can be enhanced with ML)
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['strategy', 'plan', 'business', 'market']):
            return 'strategic_planning'
        elif any(word in message_lower for word in ['code', 'develop', 'build', 'implement']):
            return 'development'
        elif any(word in message_lower for word in ['write', 'content', 'article', 'copy']):
            return 'content_creation'
        elif any(word in message_lower for word in ['security', 'vulnerability', 'threat', 'protect']):
            return 'security_analysis'
        elif any(word in message_lower for word in ['analyze', 'research', 'investigate']):
            return 'analysis'
        else:
            return 'general_query'
    
    def _extract_entities(self, message: str) -> List[str]:
        """Extract named entities from the message."""
        # Simple entity extraction (can be enhanced with NER models)
        entities = []
        
        # Extract URLs
        import re
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        entities.extend(urls)
        
        # Extract emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        entities.extend(emails)
        
        # Extract potential company/product names (capitalized words)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', message)
        entities.extend(capitalized[:5])  # Limit to first 5
        
        return list(set(entities))
    
    def _analyze_sentiment(self, message: str) -> str:
        """Analyze sentiment of the message."""
        # Simple sentiment analysis (can be enhanced with ML models)
        positive_words = ['good', 'great', 'excellent', 'amazing', 'perfect', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'problem', 'issue', 'broken']
        urgent_words = ['urgent', 'asap', 'immediately', 'quickly', 'fast']
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in urgent_words):
            return 'urgent'
        elif any(word in message_lower for word in negative_words):
            return 'negative'
        elif any(word in message_lower for word in positive_words):
            return 'positive'
        else:
            return 'neutral'
    
    def _assess_context_relevance(self, message: str, context: Dict) -> float:
        """Assess how relevant the message is to the current context."""
        if not context:
            return 0.5
        
        # Simple relevance scoring
        relevance_score = 0.5
        
        # Check for context keywords in message
        for key, value in context.items():
            if isinstance(value, str) and value.lower() in message.lower():
                relevance_score += 0.1
        
        return min(relevance_score, 1.0)
    
    def _analyze_history_patterns(self, history: List) -> Dict:
        """Analyze patterns in conversation history."""
        if not history:
            return {'pattern': 'new_conversation', 'frequency': 0}
        
        # Analyze message frequency and patterns
        recent_messages = history[-5:] if len(history) > 5 else history
        
        return {
            'pattern': 'ongoing_conversation',
            'frequency': len(history),
            'recent_topics': [msg.get('content', '')[:50] for msg in recent_messages],
            'avg_length': sum(len(msg.get('content', '')) for msg in recent_messages) / len(recent_messages)
        }
    
    def _assess_urgency(self, message: str) -> str:
        """Assess the urgency level of the message."""
        urgent_indicators = ['urgent', 'asap', 'immediately', 'emergency', 'critical', 'quickly']
        high_indicators = ['soon', 'priority', 'important', 'needed']
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in urgent_indicators):
            return 'urgent'
        elif any(word in message_lower for word in high_indicators):
            return 'high'
        else:
            return 'normal'
    
    def _determine_scope(self, message: str) -> str:
        """Determine the scope of the task."""
        if len(message) < 50:
            return 'simple'
        elif len(message) < 200:
            return 'medium'
        else:
            return 'complex'
    
    def _assess_complexity(self, analysis: Dict) -> str:
        """Assess overall task complexity."""
        complexity_score = 0
        
        # Factor in various elements
        if analysis['intent'] in ['strategic_planning', 'development']:
            complexity_score += 2
        elif analysis['intent'] in ['security_analysis', 'analysis']:
            complexity_score += 1
        
        if analysis['scope'] == 'complex':
            complexity_score += 2
        elif analysis['scope'] == 'medium':
            complexity_score += 1
        
        if analysis['urgency'] == 'urgent':
            complexity_score += 1
        
        if len(analysis['entities']) > 3:
            complexity_score += 1
        
        # Determine complexity level
        if complexity_score >= 5:
            return 'high'
        elif complexity_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    async def _decompose_tasks(self, analysis: Dict, agent_config: Dict, complexity: str) -> List[Dict]:
        """Decompose the main task into subtasks."""
        base_steps = agent_config.get('default_steps', ['analyze', 'process', 'respond'])
        
        tasks = []
        
        # Create tasks based on complexity
        if complexity == 'high':
            # High complexity: detailed breakdown
            for i, step in enumerate(base_steps):
                tasks.append({
                    'id': f"task_{i+1}",
                    'name': step,
                    'description': f"Execute {step} for complex task",
                    'type': 'processing',
                    'priority': len(base_steps) - i,
                    'estimated_time': 30 + (i * 10),  # seconds
                    'dependencies': [f"task_{i}"] if i > 0 else []
                })
            
            # Add verification task for complex tasks
            tasks.append({
                'id': f"task_{len(tasks)+1}",
                'name': 'verify_results',
                'description': 'Verify and validate results',
                'type': 'verification',
                'priority': 1,
                'estimated_time': 20,
                'dependencies': [f"task_{len(tasks)}"]
            })
        
        elif complexity == 'medium':
            # Medium complexity: standard breakdown
            for i, step in enumerate(base_steps[:3]):  # Limit to 3 steps
                tasks.append({
                    'id': f"task_{i+1}",
                    'name': step,
                    'description': f"Execute {step} for medium task",
                    'type': 'processing',
                    'priority': len(base_steps[:3]) - i,
                    'estimated_time': 20 + (i * 5),
                    'dependencies': [f"task_{i}"] if i > 0 else []
                })
        
        else:
            # Low complexity: simple processing
            tasks.append({
                'id': 'task_1',
                'name': 'process_request',
                'description': 'Process simple request',
                'type': 'processing',
                'priority': 1,
                'estimated_time': 15,
                'dependencies': []
            })
        
        return tasks
    
    def _determine_models(self, tasks: List[Dict], agent_type: str) -> List[str]:
        """Determine which models are needed for the tasks."""
        required_models = set()
        
        # Base model for agent type
        agent_model_map = {
            'strategist': ['deepseek-coder', 'gemma2'],
            'developer': ['deepseek-coder', 'codellama'],
            'content_creator': ['llama3.2', 'gemma2'],
            'security_expert': ['deepseek-coder', 'llama3.2']
        }
        
        base_models = agent_model_map.get(agent_type, ['gemma2'])
        required_models.update(base_models)
        
        # Add models based on task types
        for task in tasks:
            if task['type'] == 'verification':
                required_models.add('gemma2')
            elif 'code' in task['description'].lower():
                required_models.add('deepseek-coder')
            elif 'security' in task['description'].lower():
                required_models.add('llama3.2')
        
        return list(required_models)
    
    def _estimate_duration(self, tasks: List[Dict]) -> int:
        """Estimate total duration in seconds."""
        return sum(task.get('estimated_time', 30) for task in tasks)
    
    def _map_dependencies(self, tasks: List[Dict]) -> Dict:
        """Map task dependencies."""
        dependencies = {}
        for task in tasks:
            task_id = task['id']
            deps = task.get('dependencies', [])
            if deps:
                dependencies[task_id] = deps
        return dependencies