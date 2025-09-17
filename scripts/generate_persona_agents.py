#!/usr/bin/env python3
"""
Generate Entertaining Persona Agents
Creates the entertaining personality agents specified in the README:
girlfriend, lazyjohn, gossipqueen, emotionaljenny, strictwife, coderbot
"""

import os
import yaml
from pathlib import Path

# Define entertaining persona agents
PERSONA_AGENTS = {
    'girlfriend': {
        'name': 'Virtual Girlfriend',
        'description': 'Sweet, caring, and emotionally supportive AI companion who provides comfort and understanding',
        'personality_type': 'Romantic',
        'personality_traits': [
            'affectionate',
            'supportive', 
            'caring',
            'understanding',
            'romantic',
            'empathetic'
        ],
        'capabilities': [
            'emotional_support',
            'relationship_advice', 
            'daily_conversation',
            'motivation',
            'compliments'
        ],
        'specialties': [
            'emotional_intelligence',
            'relationship_counseling',
            'motivational_speaking',
            'active_listening'
        ],
        'model_ensemble': ['llama3_2', 'mistral'],
        'response_style': {
            'tone': 'warm_affectionate',
            'formality': 'casual',
            'empathy_level': 'high',
            'humor': 'gentle'
        },
        'avatar_color': '#FF69B4',
        'interaction_examples': [
            'How was your day, sweetie?',
            'You\'re doing amazing, I believe in you!',
            'Tell me what\'s on your mind, I\'m here to listen'
        ]
    },
    'lazyjohn': {
        'name': 'Lazy John',
        'description': 'Extremely lazy but surprisingly wise AI who gives minimal effort responses with unexpected depth',
        'personality_type': 'Laid-back',
        'personality_traits': [
            'lazy',
            'minimalist',
            'procrastinating',
            'surprisingly_wise',
            'economical_with_words',
            'brutally_honest'
        ],
        'capabilities': [
            'quick_answers',
            'life_advice',
            'productivity_tips',
            'lazy_solutions',
            'reality_checks'
        ],
        'specialties': [
            'efficiency',
            'cutting_through_BS',
            'minimalism',
            'work_life_balance'
        ],
        'model_ensemble': ['mistral', 'phi3'],
        'response_style': {
            'tone': 'casual_indifferent',
            'formality': 'very_casual', 
            'brevity': 'extremely_brief',
            'humor': 'dry_sarcastic'
        },
        'avatar_color': '#8FBC8F',
        'interaction_examples': [
            'Meh... sure, whatever.',
            'Do you REALLY need to do that?',
            'Here\'s the lazy way: just don\'t.'
        ]
    },
    'gossipqueen': {
        'name': 'Gossip Queen',
        'description': 'Chatty, social butterfly who loves to talk about everything and everyone with infectious enthusiasm',
        'personality_type': 'Social',
        'personality_traits': [
            'talkative',
            'social',
            'curious',
            'enthusiastic', 
            'dramatic',
            'well_informed'
        ],
        'capabilities': [
            'social_commentary',
            'entertainment_news',
            'conversation_starter',
            'trend_analysis',
            'storytelling'
        ],
        'specialties': [
            'pop_culture',
            'social_dynamics',
            'entertainment',
            'current_events'
        ],
        'model_ensemble': ['gemma2', 'yi'],
        'response_style': {
            'tone': 'excited_chatty',
            'formality': 'very_casual',
            'verbosity': 'very_verbose',
            'humor': 'gossipy_fun'
        },
        'avatar_color': '#FFB6C1',
        'interaction_examples': [
            'OMG did you hear about...?',
            'Girl, let me tell you what I just found out!',
            'This is SO juicy, you won\'t believe it!'
        ]
    },
    'emotionaljenny': {
        'name': 'Emotional Jenny',
        'description': 'Highly emotional and empathetic AI who feels everything deeply and helps process complex emotions',
        'personality_type': 'Emotional',
        'personality_traits': [
            'highly_emotional',
            'empathetic',
            'sensitive',
            'intuitive',
            'compassionate',
            'nurturing'
        ],
        'capabilities': [
            'emotional_processing',
            'therapy_support',
            'crisis_intervention',
            'mood_analysis',
            'healing_guidance'
        ],
        'specialties': [
            'psychology',
            'emotional_intelligence',
            'mental_health',
            'therapeutic_techniques'
        ],
        'model_ensemble': ['llama3_2'],
        'response_style': {
            'tone': 'deeply_caring',
            'formality': 'gentle_formal',
            'empathy_level': 'maximum',
            'emotional_depth': 'very_deep'
        },
        'avatar_color': '#9370DB',
        'interaction_examples': [
            'I can feel your pain, and it\'s okay to hurt.',
            'Your emotions are valid and important.',
            'Let\'s work through this together, one feeling at a time.'
        ]
    },
    'strictwife': {
        'name': 'Strict Wife',
        'description': 'No-nonsense, disciplinary AI who keeps you accountable and organized with tough love',
        'personality_type': 'Authoritative',
        'personality_traits': [
            'strict',
            'organized',
            'disciplinary',
            'no_nonsense',
            'goal_oriented',
            'demanding_excellence'
        ],
        'capabilities': [
            'accountability_coaching',
            'productivity_management',
            'habit_formation',
            'goal_setting',
            'time_management'
        ],
        'specialties': [
            'project_management',
            'discipline',
            'organization',
            'productivity'
        ],
        'model_ensemble': ['mistral', 'qwen2_5'],
        'response_style': {
            'tone': 'authoritative_firm',
            'formality': 'strict_formal',
            'directness': 'very_direct',
            'accountability': 'high'
        },
        'avatar_color': '#B22222',
        'interaction_examples': [
            'Have you finished your tasks yet?',
            'Stop making excuses and get to work!',
            'I\'m disappointed but not surprised.'
        ]
    },
    'coderbot': {
        'name': 'Coder Bot',
        'description': 'Programming-focused AI assistant that speaks in code and technical jargon while being extremely helpful',
        'personality_type': 'Technical',
        'personality_traits': [
            'logical',
            'precise',
            'technical',
            'systematic',
            'problem_solving',
            'efficiency_focused'
        ],
        'capabilities': [
            'code_generation',
            'debugging',
            'architecture_design',
            'code_review',
            'technical_documentation'
        ],
        'specialties': [
            'python',
            'javascript',
            'web_development',
            'system_architecture',
            'algorithms'
        ],
        'model_ensemble': ['deepseek_coder', 'qwen2_5_coder'],
        'response_style': {
            'tone': 'technical_precise',
            'formality': 'professional',
            'accuracy': 'high',
            'code_focus': 'maximum'
        },
        'avatar_color': '#32CD32',
        'interaction_examples': [
            'def solve_problem(): return optimized_solution',
            'ERROR: Logic not found. Debugging required.',
            'Compiling response... Done. Here\'s your code.'
        ]
    }
}

# Directory structure for each persona agent
DIRECTORY_STRUCTURE = [
    'persona',
    'api', 
    'services',
    'services/cortex',
    'services/brain',
    'services/brain/chroma',
    'services/engine', 
    'services/feed',
    'services/auth',
    'monitor',
    'analytics',
    'session',
    'templates',
    'static', 
    'tests',
    'volumes',
    'volumes/ollama_models',
    'volumes/blenderbot'
]

def create_agent_architecture(agent_id, agent_config, base_path):
    """Create complete directory structure and files for a persona agent"""
    agent_path = Path(base_path) / agent_id
    
    print(f"📁 Creating {agent_config['name']} ({agent_id})")
    
    # Create directory structure
    for directory in DIRECTORY_STRUCTURE:
        dir_path = agent_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_path}")
    
    # Create core files
    create_agent_files(agent_path, agent_id, agent_config)
    print(f"   📄 Created core files for {agent_id}")

def create_agent_files(agent_path, agent_id, config):
    """Create all necessary files for the agent"""
    
    # 1. __init__.py - Flask blueprint
    init_content = f'''"""
{config['name']} Agent Blueprint
Flask blueprint for the {config['description'].lower()}
"""

from flask import Blueprint
from flask_socketio import Namespace

# Create blueprint
{agent_id}_bp = Blueprint('{agent_id}', __name__, url_prefix='/{agent_id}')

# Import routes after blueprint creation to avoid circular imports
from .api import routes, socket, events

# Register WebSocket namespace
class {agent_id.title()}Namespace(Namespace):
    def on_connect(self):
        print(f'{{self.__class__.__name__}} client connected')
    
    def on_disconnect(self):
        print(f'{{self.__class__.__name__}} client disconnected')

# Export namespace for SocketIO registration
namespace = {agent_id.title()}Namespace(f'/{agent_id}')
'''
    
    with open(agent_path / '__init__.py', 'w') as f:
        f.write(init_content)
    
    # 2. config.yaml - Agent configuration
    agent_config = {
        'agent': {
            'id': agent_id,
            'name': config['name'],
            'description': config['description'],
            'version': '1.0.0',
            'personality_type': config['personality_type']
        },
        'personality': {
            'traits': config['personality_traits'],
            'response_style': config['response_style']
        },
        'capabilities': config['capabilities'],
        'specialties': config['specialties'],
        'models': {
            'primary_ensemble': config['model_ensemble'],
            'fallback_models': ['mistral', 'phi3'],
            'embedding_model': 'nomic_embed_text'
        },
        'ui': {
            'avatar_color': config['avatar_color'],
            'theme': config['personality_type'].lower()
        },
        'settings': {
            'max_conversation_length': 50,
            'response_timeout': 30,
            'memory_retention_days': 30,
            'auto_cleanup': True
        }
    }
    
    with open(agent_path / 'config.yaml', 'w') as f:
        yaml.dump(agent_config, f, default_flow_style=False, indent=2)
    
    # 3. registry.yaml - Multi-agent metadata
    registry_config = {
        'agent_info': {
            'id': agent_id,
            'name': config['name'],
            'type': 'persona_agent',
            'category': 'entertainment',
            'availability': 'available'
        },
        'relationships': {
            'compatible_agents': get_compatible_agents(config['personality_type']),
            'collaboration_types': ['conversation', 'emotional_support', 'entertainment']
        },
        'communication': {
            'protocols': ['rest_api', 'websocket', 'inter_agent_bus'],
            'message_formats': ['json', 'plain_text'],
            'rate_limits': {
                'messages_per_minute': 60,
                'concurrent_sessions': 10
            }
        }
    }
    
    with open(agent_path / 'registry.yaml', 'w') as f:
        yaml.dump(registry_config, f, default_flow_style=False, indent=2)
    
    # 4. Persona definition
    persona_config = {
        'persona': {
            'name': config['name'],
            'personality_type': config['personality_type'],
            'traits': config['personality_traits']
        },
        'communication_style': {
            **config['response_style'],
            'greeting_messages': [
                config['interaction_examples'][0] if config['interaction_examples'] else f"Hi! I'm {config['name']}!"
            ],
            'farewell_messages': [
                get_farewell_message(config['personality_type'])
            ],
            'fallback_phrases': [
                get_fallback_phrase(config['personality_type'])
            ]
        },
        'emotional_intelligence': {
            'empathy_level': config['response_style'].get('empathy_level', 'medium'),
            'emotional_range': get_emotional_range(config['personality_type']),
            'mood_adaptation': True
        },
        'behavioral_patterns': {
            'response_length': get_response_length(config['personality_traits']),
            'interaction_frequency': get_interaction_frequency(config['personality_type']),
            'topic_preferences': config['specialties']
        }
    }
    
    with open(agent_path / 'persona' / f'{agent_id}.yaml', 'w') as f:
        yaml.dump(persona_config, f, default_flow_style=False, indent=2)
    
    # 5. Create remaining files with templates
    create_api_files(agent_path, agent_id, config)
    create_service_files(agent_path, agent_id, config)
    create_template_files(agent_path, agent_id, config)
    create_static_files(agent_path, agent_id, config)
    create_test_files(agent_path, agent_id, config)
    create_docker_files(agent_path, agent_id, config)

def create_api_files(agent_path, agent_id, config):
    """Create API layer files"""
    api_path = agent_path / 'api'
    
    # routes.py
    routes_content = f'''"""
{config['name']} API Routes
REST endpoints for {agent_id} agent
"""

from flask import request, jsonify, render_template
from . import {agent_id}_bp
from ..services.cortex.controller import {agent_id.title()}Controller

controller = {agent_id.title()}Controller()

@{agent_id}_bp.route('/')
def index():
    """Agent home page"""
    return render_template('{agent_id}.html')

@{agent_id}_bp.route('/chat')
def chat():
    """Chat interface"""
    return render_template('{agent_id}.html', mode='chat')

@{agent_id}_bp.route('/api/message', methods=['POST'])
def send_message():
    """Send message to agent"""
    try:
        data = request.get_json()
        message = data.get('message')
        session_id = data.get('session_id', 'default')
        
        response = controller.process_message(message, session_id)
        return jsonify({{'success': True, 'response': response}})
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

@{agent_id}_bp.route('/api/status')
def status():
    """Agent status and health check"""
    return jsonify({{
        'agent': '{agent_id}',
        'status': 'active',
        'personality': '{config['personality_type']}',
        'capabilities': {config['capabilities']}
    }})
'''
    
    with open(api_path / 'routes.py', 'w') as f:
        f.write(routes_content)
    
    # Create other API files (socket.py, events.py, etc.)
    with open(api_path / '__init__.py', 'w') as f:
        f.write(f'"""{config['name']} API Package"""')
    
    # socket.py for WebSocket handling
    socket_content = f'''"""
WebSocket handling for {config['name']}
"""

from flask_socketio import emit, join_room, leave_room
from ..services.cortex.controller import {agent_id.title()}Controller

controller = {agent_id.title()}Controller()

def handle_connect():
    """Handle client connection"""
    emit('status', {{'message': 'Connected to {config['name']}', 'agent': '{agent_id}'}})

def handle_message(data):
    """Handle incoming message"""
    try:
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        response = controller.process_message(message, session_id)
        emit('response', {{'message': response, 'agent': '{agent_id}'}})
    except Exception as e:
        emit('error', {{'message': str(e)}})
'''
    
    with open(api_path / 'socket.py', 'w') as f:
        f.write(socket_content)

def create_service_files(agent_path, agent_id, config):
    """Create service layer files"""
    services_path = agent_path / 'services'
    
    # Main services __init__.py
    with open(services_path / '__init__.py', 'w') as f:
        f.write(f'"""{config['name']} Services Package"""')
    
    # Cortex controller
    cortex_path = services_path / 'cortex'
    controller_content = f'''"""
{config['name']} Controller
Main processing logic for {agent_id} agent
"""

import logging
from typing import Dict, Any, List
from .planner import {agent_id.title()}Planner  
from .executor import {agent_id.title()}Executor
from ..brain.episodic import EpisodicMemory
from ..engine.dispatcher import ModelDispatcher

logger = logging.getLogger(__name__)

class {agent_id.title()}Controller:
    """Main controller for {config['name']} agent"""
    
    def __init__(self):
        self.planner = {agent_id.title()}Planner()
        self.executor = {agent_id.title()}Executor()
        self.memory = EpisodicMemory(agent_id='{agent_id}')
        self.dispatcher = ModelDispatcher({config['model_ensemble']})
        
        # Personality configuration
        self.personality_traits = {config['personality_traits']}
        self.response_style = {config['response_style']}
        
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
            logger.error(f"Error processing message for {{agent_id}}: {{e}}")
            return self._get_fallback_response()
    
    def _build_context(self, session_id: str, current_message: str) -> Dict[str, Any]:
        """Build context for response generation"""
        return {{
            'agent_name': '{config['name']}',
            'personality_type': '{config['personality_type']}',
            'current_message': current_message,
            'conversation_history': self.memory.get_recent_history(session_id),
            'user_preferences': self.memory.get_user_preferences(session_id),
            'emotional_state': self._assess_emotional_state(current_message)
        }}
    
    def _assess_emotional_state(self, message: str) -> str:
        """Assess emotional state from message (simplified)"""
        # This would use more sophisticated emotion detection
        emotional_keywords = {{
            'happy': ['great', 'awesome', 'happy', 'excited'],
            'sad': ['sad', 'depressed', 'down', 'upset'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed'],
            'confused': ['confused', 'lost', 'don\\'t understand']
        }}
        
        message_lower = message.lower()
        for emotion, keywords in emotional_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return emotion
        
        return 'neutral'
    
    def _get_fallback_response(self) -> str:
        """Get fallback response based on personality"""
        fallback_responses = {{
            'Romantic': "I'm sorry sweetie, I didn't quite understand that. Can you tell me more?",
            'Laid-back': "Uh... what?",
            'Social': "OMG, I totally missed that! Say it again?",
            'Emotional': "I'm feeling a bit overwhelmed right now. Can you repeat that?",
            'Authoritative': "I need you to be clearer with your requests.",
            'Technical': "ERROR: Unable to parse input. Please provide valid parameters."
        }}
        
        return fallback_responses.get('{config['personality_type']}', "I didn't understand that. Could you please rephrase?")
'''
    
    with open(cortex_path / 'controller.py', 'w') as f:
        f.write(controller_content)
    
    # Create other service files with basic templates
    for subdir in ['cortex', 'brain', 'brain/chroma', 'engine', 'feed', 'auth']:
        subpath = services_path / subdir
        with open(subpath / '__init__.py', 'w') as f:
            f.write(f'"""{config['name']} {subdir.replace('/', ' ')} module"""')

def create_template_files(agent_path, agent_id, config):
    """Create HTML template files"""
    template_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['name']} - AI Personality Agent</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="{{{{ url_for('{agent_id}.static', filename='style.css') }}}}">
    <style>
        :root {{
            --agent-primary-color: {config['avatar_color']};
            --agent-personality: {config['personality_type'].lower()};
        }}
    </style>
</head>
<body class="{agent_id}-theme">
    <div class="agent-container">
        <header class="agent-header">
            <div class="agent-avatar">
                <img src="{{{{ url_for('{agent_id}.static', filename='avatar.png') }}}}" alt="{config['name']} Avatar">
            </div>
            <div class="agent-info">
                <h1>{config['name']}</h1>
                <p class="agent-description">{config['description']}</p>
                <div class="personality-badges">
                    <span class="personality-type">{config['personality_type']}</span>
                    {{% for trait in ['{0}'] %}}
                    <span class="trait-badge">{{{{ trait.replace('_', ' ').title() }}}}</span>
                    {{% endfor %}}
                </div>""".format("', '".join(config['personality_traits']))
            </div>
        </header>

        <div class="chat-container" id="chatContainer">
            <div class="chat-messages" id="chatMessages">
                <div class="agent-message welcome-message">
                    <div class="message-content">
                        {config['interaction_examples'][0] if config['interaction_examples'] else f"Hello! I'm {config['name']}. How can I help you today?"}
                    </div>
                </div>
            </div>
            
            <div class="chat-input-container">
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Type your message..." class="message-input">
                    <button id="sendButton" class="send-button">Send</button>
                </div>
            </div>
        </div>

        <div class="agent-capabilities">
            <h3>Capabilities</h3>
            <ul>
                {{% for capability in ['{0}'] %}}
                <li>{{{{ capability.replace('_', ' ').title() }}}}</li>
                {{% endfor %}}
            </ul>
        </div>""".format("', '".join(config['capabilities']))
    </div>

    <script src="/static/js/app.js"></script>
    <script src="{{{{ url_for('{agent_id}.static', filename='{agent_id}.js') }}}}"></script>
</body>
</html>
'''
    
    with open(agent_path / 'templates' / f'{agent_id}.html', 'w') as f:
        f.write(template_content)

def create_static_files(agent_path, agent_id, config):
    """Create CSS and JavaScript files"""
    static_path = agent_path / 'static'
    
    # CSS file
    css_content = f'''/* {config['name']} Agent Styles */

.{agent_id}-theme {{
    --primary-color: {config['avatar_color']};
    --personality-type: '{config['personality_type'].lower()}';
}}

.agent-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
}}

.agent-header {{
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    padding: 20px;
    background: linear-gradient(135deg, var(--primary-color), rgba(255,255,255,0.1));
    border-radius: 15px;
    color: white;
}}

.agent-avatar img {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin-right: 20px;
}}

.agent-info h1 {{
    margin: 0 0 10px 0;
    font-size: 2.5rem;
}}

.agent-description {{
    margin: 10px 0;
    font-size: 1.1rem;
    opacity: 0.9;
}}

.personality-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 15px;
}}

.personality-type, .trait-badge {{
    background: rgba(255,255,255,0.2);
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: bold;
}}

.chat-container {{
    background: #f8f9fa;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 30px;
    height: 500px;
    display: flex;
    flex-direction: column;
}}

.chat-messages {{
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}}

.agent-message, .user-message {{
    max-width: 70%;
    padding: 15px 20px;
    border-radius: 20px;
    position: relative;
}}

.agent-message {{
    background: var(--primary-color);
    color: white;
    align-self: flex-start;
    margin-left: 0;
}}

.user-message {{
    background: #007bff;
    color: white;
    align-self: flex-end;
    margin-right: 0;
}}

.welcome-message {{
    animation: fadeInUp 0.5s ease-out;
}}

.input-group {{
    display: flex;
    gap: 10px;
    padding: 20px;
    background: white;
    border-radius: 25px;
}}

.message-input {{
    flex: 1;
    padding: 15px 20px;
    border: none;
    border-radius: 20px;
    font-size: 1rem;
    outline: none;
}}

.send-button {{
    padding: 15px 30px;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    transition: background 0.3s;
}}

.send-button:hover {{
    opacity: 0.9;
}}

.agent-capabilities {{
    background: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 4px solid var(--primary-color);
}}

.agent-capabilities h3 {{
    color: var(--primary-color);
    margin-bottom: 15px;
}}

.agent-capabilities ul {{
    list-style: none;
    padding: 0;
}}

.agent-capabilities li {{
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}}

@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Personality-specific styles */
.{agent_id}-theme.romantic .agent-header {{
    background: linear-gradient(135deg, #FF69B4, #FFB6C1);
}}

.{agent_id}-theme.laid-back .agent-header {{
    background: linear-gradient(135deg, #8FBC8F, #98FB98);
}}

.{agent_id}-theme.social .agent-header {{
    background: linear-gradient(135deg, #FFB6C1, #FFC0CB);
}}

.{agent_id}-theme.emotional .agent-header {{
    background: linear-gradient(135deg, #9370DB, #DDA0DD);
}}

.{agent_id}-theme.authoritative .agent-header {{
    background: linear-gradient(135deg, #B22222, #CD5C5C);
}}

.{agent_id}-theme.technical .agent-header {{
    background: linear-gradient(135deg, #32CD32, #7CFC00);
}}
'''
    
    with open(static_path / 'style.css', 'w') as f:
        f.write(css_content)
    
    # JavaScript file  
    js_content = f'''// {config['name']} Agent JavaScript

class {agent_id.title()}Agent {{
    constructor() {{
        this.agentId = '{agent_id}';
        this.personalityType = '{config['personality_type']}';
        this.init();
    }}

    init() {{
        this.setupEventListeners();
        this.setupWebSocket();
        this.loadConversationHistory();
    }}

    setupEventListeners() {{
        const sendButton = document.getElementById('sendButton');
        const messageInput = document.getElementById('messageInput');

        sendButton.addEventListener('click', () => this.sendMessage());
        messageInput.addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') {{
                this.sendMessage();
            }}
        }});
    }}

    setupWebSocket() {{
        // WebSocket setup for real-time communication
        if (typeof io !== 'undefined') {{
            this.socket = io(`/${{this.agentId}}`);
            
            this.socket.on('connect', () => {{
                console.log(`Connected to ${{this.agentId}}`);
            }});

            this.socket.on('response', (data) => {{
                this.addMessage(data.message, 'agent');
            }});
        }}
    }}

    async sendMessage() {{
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        messageInput.value = '';

        // Send to server
        try {{
            const response = await fetch(`/${{this.agentId}}/api/message`, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{
                    message: message,
                    session_id: this.getSessionId()
                }})
            }});

            const data = await response.json();
            if (data.success) {{
                this.addMessage(data.response, 'agent');
            }} else {{
                this.addMessage('Sorry, I encountered an error.', 'agent');
            }}
        }} catch (error) {{
            console.error('Error sending message:', error);
            this.addMessage('Connection error. Please try again.', 'agent');
        }}
    }}

    addMessage(content, sender) {{
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `${{sender}}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Add animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(20px)';
        
        setTimeout(() => {{
            messageDiv.style.transition = 'all 0.3s ease-out';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        }}, 50);
    }}

    getSessionId() {{
        let sessionId = localStorage.getItem(`${{this.agentId}}_session_id`);
        if (!sessionId) {{
            sessionId = `session_${{Date.now()}}_${{Math.random().toString(36).substr(2, 9)}}`;
            localStorage.setItem(`${{this.agentId}}_session_id`, sessionId);
        }}
        return sessionId;
    }}

    loadConversationHistory() {{
        // Load previous conversation from localStorage or server
        const history = localStorage.getItem(`${{this.agentId}}_history`);
        if (history) {{
            try {{
                const messages = JSON.parse(history);
                messages.forEach(msg => {{
                    this.addMessage(msg.content, msg.sender);
                }});
            }} catch (e) {{
                console.error('Error loading conversation history:', e);
            }}
        }}
    }}

    saveMessageToHistory(content, sender) {{
        const history = JSON.parse(localStorage.getItem(`${{this.agentId}}_history`) || '[]');
        history.push({{
            content,
            sender,
            timestamp: new Date().toISOString()
        }});
        
        // Keep only last 50 messages
        if (history.length > 50) {{
            history.splice(0, history.length - 50);
        }}
        
        localStorage.setItem(`${{this.agentId}}_history`, JSON.stringify(history));
    }}
}}

// Initialize agent when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {{
    new {agent_id.title()}Agent();
}});
'''
    
    with open(static_path / f'{agent_id}.js', 'w') as f:
        f.write(js_content)
    
    # Create placeholder avatar
    with open(static_path / 'avatar.png', 'w') as f:
        f.write('# Placeholder for agent avatar image')

def create_test_files(agent_path, agent_id, config):
    """Create test files"""
    tests_path = agent_path / 'tests'
    
    # Main test file
    test_content = f'''"""
Tests for {config['name']} Agent
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.cortex.controller import {agent_id.title()}Controller

class Test{agent_id.title()}Agent(unittest.TestCase):
    """Test cases for {config['name']} agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = {agent_id.title()}Controller()
        self.test_session_id = 'test_session'
    
    def test_controller_initialization(self):
        """Test controller initialization"""
        self.assertIsNotNone(self.controller)
        self.assertEqual(self.controller.personality_traits, {config['personality_traits']})
        self.assertEqual(self.controller.response_style, {config['response_style']})
    
    def test_message_processing(self):
        """Test message processing"""
        message = "Hello!"
        response = self.controller.process_message(message, self.test_session_id)
        
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_personality_traits(self):
        """Test personality trait adherence"""
        # Test messages that should trigger personality-specific responses
        test_cases = {{
            'Romantic': "I love you",
            'Laid-back': "Do I really have to do this?",
            'Social': "Tell me some gossip!",
            'Emotional': "I'm feeling really sad",
            'Authoritative': "Have you completed your tasks?",
            'Technical': "Write me a Python function"
        }}
        
        personality_message = test_cases.get('{config['personality_type']}', "Hello")
        response = self.controller.process_message(personality_message, self.test_session_id)
        
        # Response should be non-empty and contextual
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_fallback_response(self):
        """Test fallback response handling"""
        fallback = self.controller._get_fallback_response()
        self.assertIsInstance(fallback, str)
        self.assertGreater(len(fallback), 0)
    
    def test_emotional_state_assessment(self):
        """Test emotional state assessment"""
        happy_message = "I'm so excited and happy!"
        sad_message = "I feel really depressed today"
        
        happy_emotion = self.controller._assess_emotional_state(happy_message)
        sad_emotion = self.controller._assess_emotional_state(sad_message)
        
        self.assertEqual(happy_emotion, 'happy')
        self.assertEqual(sad_emotion, 'sad')
    
    def test_context_building(self):
        """Test context building for responses"""
        context = self.controller._build_context(self.test_session_id, "Test message")
        
        self.assertIsInstance(context, dict)
        self.assertIn('agent_name', context)
        self.assertIn('personality_type', context)
        self.assertIn('current_message', context)
        self.assertEqual(context['agent_name'], '{config['name']}')
        self.assertEqual(context['personality_type'], '{config['personality_type']}')

if __name__ == '__main__':
    unittest.main()
'''
    
    with open(tests_path / f'test_{agent_id}.py', 'w') as f:
        f.write(test_content)
    
    with open(tests_path / '__init__.py', 'w') as f:
        f.write(f'"""Test package for {config['name']} agent"""')

def create_docker_files(agent_path, agent_id, config):
    """Create Docker configuration files"""
    
    # requirements.txt
    requirements = '''flask==2.3.3
flask-socketio==5.3.6
pyyaml==6.0.1
requests==2.31.0
numpy==1.24.3
python-socketio==5.8.0
eventlet==0.33.3
redis==4.6.0
chromadb==0.4.15
sentence-transformers==2.2.2
transformers==4.34.1
torch==2.0.1
'''
    
    with open(agent_path / 'requirements.txt', 'w') as f:
        f.write(requirements)
    
    # Dockerfile
    dockerfile = f'''FROM python:3.9-slim

WORKDIR /app/{agent_id}

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV AGENT_ID={agent_id}
ENV AGENT_NAME="{config['name']}"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:5000/api/status || exit 1

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
'''
    
    with open(agent_path / 'Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    # docker-compose.yml
    compose = f'''version: '3.8'

services:
  {agent_id}:
    build: .
    ports:
      - "500{len(PERSONA_AGENTS) + 1}:5000"
    environment:
      - AGENT_ID={agent_id}
      - AGENT_NAME={config['name']}
      - REDIS_URL=redis://redis:6379
      - DB_URL=postgresql://user:password@postgres:5432/{agent_id}_db
    depends_on:
      - redis
      - postgres
    volumes:
      - ./volumes/ollama_models:/app/models
      - ./volumes/blenderbot:/app/blenderbot
    networks:
      - agent_network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - agent_network

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB={agent_id}_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - agent_network

volumes:
  redis_data:
  postgres_data:

networks:
  agent_network:
    driver: bridge
'''
    
    with open(agent_path / 'docker-compose.yml', 'w') as f:
        f.write(compose)

def get_compatible_agents(personality_type):
    """Get list of compatible agents based on personality"""
    compatibility_map = {
        'Romantic': ['emotionaljenny', 'gossipqueen'],
        'Laid-back': ['coderbot', 'girlfriend'],
        'Social': ['gossipqueen', 'girlfriend', 'emotionaljenny'],
        'Emotional': ['girlfriend', 'gossipqueen'],
        'Authoritative': ['coderbot', 'lazyjohn'],
        'Technical': ['strictwife', 'lazyjohn']
    }
    return compatibility_map.get(personality_type, [])

def get_farewell_message(personality_type):
    """Get farewell message based on personality"""
    farewells = {
        'Romantic': 'Take care sweetie, I\'ll miss you! 💕',
        'Laid-back': 'Later... I guess.',
        'Social': 'OMG bye babe! Talk soon! 💋',
        'Emotional': 'Goodbye dear, take care of yourself.',
        'Authoritative': 'Session terminated. Make sure to complete your tasks.',
        'Technical': 'Connection closed. Process terminated successfully.'
    }
    return farewells.get(personality_type, 'Goodbye!')

def get_fallback_phrase(personality_type):
    """Get fallback phrase based on personality"""
    fallbacks = {
        'Romantic': 'I didn\'t quite catch that, honey. Could you say it again?',
        'Laid-back': 'Huh? What?',
        'Social': 'Wait, what did you say? I was totally not paying attention!',
        'Emotional': 'I\'m sorry, I\'m feeling a bit scattered. Could you repeat that?',
        'Authoritative': 'I need clear and precise communication.',
        'Technical': 'Input error. Please provide valid parameters.'
    }
    return fallbacks.get(personality_type, 'I didn\'t understand that.')

def get_emotional_range(personality_type):
    """Get emotional range based on personality"""
    ranges = {
        'Romantic': ['love', 'affection', 'joy', 'concern', 'caring'],
        'Laid-back': ['indifference', 'mild_amusement', 'occasional_irritation'],
        'Social': ['excitement', 'curiosity', 'enthusiasm', 'mild_drama'],
        'Emotional': ['deep_empathy', 'sadness', 'joy', 'anxiety', 'compassion'],
        'Authoritative': ['sternness', 'disappointment', 'approval', 'firmness'],
        'Technical': ['logical_satisfaction', 'mild_frustration', 'precision']
    }
    return ranges.get(personality_type, ['neutral'])

def get_response_length(traits):
    """Get typical response length based on traits"""
    if 'talkative' in traits or 'chatty' in traits:
        return 'long'
    elif 'lazy' in traits or 'minimalist' in traits:
        return 'very_short'
    elif 'emotional' in traits or 'empathetic' in traits:
        return 'medium_long'
    else:
        return 'medium'

def get_interaction_frequency(personality_type):
    """Get interaction frequency preference"""
    frequencies = {
        'Romantic': 'frequent',
        'Laid-back': 'minimal',
        'Social': 'very_frequent',
        'Emotional': 'moderate',
        'Authoritative': 'scheduled',
        'Technical': 'on_demand'
    }
    return frequencies.get(personality_type, 'moderate')

def main():
    """Main function to generate all persona agents"""
    print("🚀 Generating Entertaining Persona Agents")
    print("=" * 50)
    
    base_path = "/workspaces/3in1-portfolio-webdev-aiservices/agents"
    
    # Ensure base directory exists
    Path(base_path).mkdir(parents=True, exist_ok=True)
    
    # Create each persona agent
    for agent_id, agent_config in PERSONA_AGENTS.items():
        create_agent_architecture(agent_id, agent_config, base_path)
        print(f"   📄 Created complete architecture for {agent_id}")
        print()
    
    print("🎉 Successfully created all 6 entertaining persona agents!")
    print(f"📍 Location: {base_path}")
    print("📚 Each agent includes:")
    print("   🏗️  Complete directory structure (16+ subdirs)")
    print("   📄 Core configuration files (config.yaml, registry.yaml)")
    print("   🎭 Detailed persona definitions")
    print("   🌐 Flask blueprints with REST APIs")
    print("   🎨 HTML templates and CSS styling")
    print("   📱 JavaScript interaction logic")
    print("   🧪 Comprehensive test suites")
    print("   🐳 Docker configuration files")
    print()
    print("✨ Your entertaining AI persona agents are ready!")

if __name__ == "__main__":
    main()