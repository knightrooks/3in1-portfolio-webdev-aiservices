#!/usr/bin/env python3
"""
AI Agent Architecture Generator
Creates comprehensive directory structure for all 10 AI agents
"""

import os
import yaml
import json
from pathlib import Path

# Define all 10 agents with their configurations
AGENTS_CONFIG = {
    'strategist': {
        'name': 'Business Strategist AI',
        'description': 'Expert in business strategy, market analysis, and strategic planning',
        'primary_model': 'gemma2',
        'personality': 'analytical_advisor',
        'color_theme': '#1f4e79'
    },
    'developer': {
        'name': 'Senior Developer AI',
        'description': 'Expert software developer and architect with advanced capabilities',
        'primary_model': 'deepseek-coder',
        'personality': 'technical_expert',
        'color_theme': '#2d5a27'
    },
    'security_expert': {
        'name': 'Cybersecurity Expert AI',
        'description': 'Expert in cybersecurity with advanced threat analysis',
        'primary_model': 'llama3_2',
        'personality': 'security_specialist',
        'color_theme': '#8b0000'
    },
    'content_creator': {
        'name': 'Content Creator AI',
        'description': 'Expert content strategist with advanced multilingual capabilities',
        'primary_model': 'llama3_2',
        'personality': 'creative_communicator',
        'color_theme': '#663399'
    },
    'research_analyst': {
        'name': 'Research Analyst AI',
        'description': 'Advanced research specialist with long-context analysis',
        'primary_model': 'yi',
        'personality': 'analytical_researcher',
        'color_theme': '#006666'
    },
    'data_scientist': {
        'name': 'Data Scientist AI',
        'description': 'Advanced data science specialist with mathematical modeling',
        'primary_model': 'mathstral',
        'personality': 'quantitative_analyst',
        'color_theme': '#cc6600'
    },
    'customer_success': {
        'name': 'Customer Success AI',
        'description': 'Expert in customer experience with emotional intelligence',
        'primary_model': 'yi',
        'personality': 'empathetic_advisor',
        'color_theme': '#0066cc'
    },
    'product_manager': {
        'name': 'Product Manager AI',
        'description': 'Strategic product management with user research expertise',
        'primary_model': 'gemma2',
        'personality': 'product_strategist',
        'color_theme': '#ff6600'
    },
    'marketing_specialist': {
        'name': 'Marketing Specialist AI',
        'description': 'Digital marketing expert with creative content capabilities',
        'primary_model': 'llama3_2',
        'personality': 'creative_marketer',
        'color_theme': '#e91e63'
    },
    'operations_manager': {
        'name': 'Operations Manager AI',
        'description': 'Business operations specialist with process optimization',
        'primary_model': 'phi3',
        'personality': 'efficiency_optimizer',
        'color_theme': '#4a4a4a'
    }
}

# Directory structure template
DIRECTORY_STRUCTURE = [
    '',
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
    'tests'
]

# Core files to create for each agent
CORE_FILES = {
    '__init__.py': 'blueprint_init',
    'config.yaml': 'agent_config',
    'registry.yaml': 'registry_metadata',
    'persona/{agent_id}.yaml': 'persona_config',
    'api/__init__.py': 'api_init',
    'api/routes.py': 'api_routes',
    'api/socket.py': 'api_socket',
    'api/events.py': 'api_events',
    'services/__init__.py': 'services_init',
    'services/cortex/__init__.py': 'cortex_init',
    'services/cortex/controller.py': 'cortex_controller',
    'services/cortex/planner.py': 'cortex_planner',
    'services/cortex/executor.py': 'cortex_executor',
    'services/cortex/hooks.py': 'cortex_hooks',
    'services/brain/__init__.py': 'brain_init',
    'services/brain/chroma/__init__.py': 'chroma_init',
    'services/brain/chroma/embedder.py': 'chroma_embedder',
    'services/brain/chroma/vector_store.py': 'chroma_vector_store',
    'services/brain/chroma/recall.py': 'chroma_recall',
    'services/brain/episodic.py': 'brain_episodic',
    'services/brain/feedback.py': 'brain_feedback',
    'services/brain/memory_sync.py': 'brain_memory_sync',
    'services/engine/__init__.py': 'engine_init',
    'services/engine/local_runner.py': 'engine_local_runner',
    'services/engine/api_runner.py': 'engine_api_runner',
    'services/engine/dispatcher.py': 'engine_dispatcher',
    'services/feed/__init__.py': 'feed_init',
    'services/feed/fetch.py': 'feed_fetch',
    'services/feed/preprocess.py': 'feed_preprocess',
    'services/auth/__init__.py': 'auth_init',
    'services/auth/token.py': 'auth_token',
    'services/auth/roles.py': 'auth_roles',
    'monitor/__init__.py': 'monitor_init',
    'monitor/latency.py': 'monitor_latency',
    'monitor/usage.py': 'monitor_usage',
    'monitor/alerts.py': 'monitor_alerts',
    'analytics/__init__.py': 'analytics_init',
    'analytics/logger.py': 'analytics_logger',
    'analytics/metrics.py': 'analytics_metrics',
    'session/__init__.py': 'session_init',
    'session/store.py': 'session_store',
    'session/cleanup.py': 'session_cleanup',
    'templates/{agent_id}.html': 'chat_template',
    'static/style.css': 'agent_css',
    'static/{agent_id}.js': 'agent_js',
    'static/utils.js': 'utils_js',
    'tests/__init__.py': 'tests_init',
    'tests/test_routes.py': 'test_routes',
    'tests/test_controller.py': 'test_controller',
    'tests/test_memory.py': 'test_memory',
    'tests/simulator.py': 'test_simulator'
}

def create_agent_directories(base_path: str):
    """Create directory structure for all agents"""
    print("🏗️  Creating AI Agent Architecture...")
    
    for agent_id, agent_config in AGENTS_CONFIG.items():
        print(f"\n📁 Creating {agent_config['name']} ({agent_id})")
        
        # Create main agent directory
        agent_path = Path(base_path) / agent_id
        
        # Create all subdirectories
        for subdir in DIRECTORY_STRUCTURE:
            dir_path = agent_path / subdir
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {dir_path}")
        
        print(f"   📂 Created {len(DIRECTORY_STRUCTURE)} directories for {agent_id}")

def generate_file_content(template_type: str, agent_id: str, agent_config: dict) -> str:
    """Generate content for different file types"""
    
    if template_type == 'blueprint_init':
        return f'''"""
{agent_config['name']} Blueprint Registration
Flask blueprint for {agent_config['name']}
"""

from flask import Blueprint
from .api.routes import {agent_id}_routes
from .api.socket import {agent_id}_socket

def create_{agent_id}_blueprint():
    """Create and configure the {agent_config['name']} blueprint"""
    
    bp = Blueprint('{agent_id}', __name__, 
                   url_prefix='/ai/agents/{agent_id}',
                   template_folder='templates',
                   static_folder='static')
    
    # Register routes
    bp.register_blueprint({agent_id}_routes)
    
    # Register WebSocket handlers
    {agent_id}_socket.init_app(bp)
    
    return bp

# Export the blueprint
{agent_id}_bp = create_{agent_id}_blueprint()'''

    elif template_type == 'api_routes':
        return f'''"""
{agent_config['name']} REST API Routes
Handles HTTP requests for {agent_id} agent
"""

from flask import Blueprint, request, jsonify
from ..services.cortex.controller import {agent_id.title()}Controller
from ..monitor.usage import track_usage
from ..analytics.logger import log_interaction

{agent_id}_routes = Blueprint('{agent_id}_routes', __name__)
controller = {agent_id.title()}Controller()

@{agent_id}_routes.route('/chat', methods=['POST'])
@track_usage
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Process request through controller
        response = await controller.process_message(message, session_id)
        
        # Log interaction
        log_interaction('{agent_id}', 'chat', message, response)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

@{agent_id}_routes.route('/health', methods=['GET'])
def health_check():
    """Agent health check endpoint"""
    return jsonify(controller.get_health_status())

@{agent_id}_routes.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get agent capabilities"""
    return jsonify(controller.get_capabilities())

@{agent_id}_routes.route('/metrics', methods=['GET'])
def get_metrics():
    """Get agent performance metrics"""
    return jsonify(controller.get_performance_metrics())'''

    elif template_type == 'cortex_controller':
        return f'''"""
{agent_config['name']} Controller
Main orchestration controller for {agent_id} agent
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from .planner import {agent_id.title()}Planner
from .executor import {agent_id.title()}Executor
from ..brain.episodic import EpisodicMemory
from ..engine.dispatcher import ModelDispatcher

logger = logging.getLogger(__name__)

class {agent_id.title()}Controller:
    """Main controller for {agent_config['name']}"""
    
    def __init__(self):
        self.planner = {agent_id.title()}Planner()
        self.executor = {agent_id.title()}Executor()
        self.memory = EpisodicMemory('{agent_id}')
        self.dispatcher = ModelDispatcher('{agent_id}')
        
        self.session_data = {{}}
        self.performance_metrics = {{
            'requests_processed': 0,
            'average_response_time': 0.0,
            'success_rate': 0.0,
            'user_satisfaction': 0.0
        }}
        
        logger.info(f"Initialized {{self.__class__.__name__}}")
    
    async def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """Process incoming message and generate response"""
        start_time = datetime.now()
        
        try:
            # Initialize session if new
            if session_id not in self.session_data:
                self.session_data[session_id] = {{
                    'created_at': start_time,
                    'conversation_history': [],
                    'user_profile': {{}},
                    'context': {{}}
                }}
            
            session = self.session_data[session_id]
            
            # Plan the response approach
            plan = await self.planner.create_plan(message, session)
            
            # Execute the plan
            response = await self.executor.execute_plan(plan, session)
            
            # Store in memory
            await self.memory.store_interaction(session_id, message, response)
            
            # Update session
            session['conversation_history'].append({{
                'timestamp': start_time.isoformat(),
                'user_message': message,
                'agent_response': response.get('content', ''),
                'confidence': response.get('confidence', 0.0)
            }})
            
            # Update metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(processing_time, response.get('success', True))
            
            return {{
                'response': response.get('content', ''),
                'confidence': response.get('confidence', 0.0),
                'session_id': session_id,
                'processing_time': processing_time,
                'agent': '{agent_id}',
                'timestamp': datetime.now().isoformat()
            }}
            
        except Exception as e:
            logger.error(f"Error processing message: {{e}}")
            return {{
                'error': str(e),
                'agent': '{agent_id}',
                'timestamp': datetime.now().isoformat()
            }}
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health status"""
        return {{
            'agent': '{agent_id}',
            'status': 'healthy',
            'uptime': datetime.now().isoformat(),
            'active_sessions': len(self.session_data),
            'performance_metrics': self.performance_metrics
        }}
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            '{agent_config["description"]}',
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
            )'''

    elif template_type == 'chat_template':
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{agent_config['name']} - AI Assistant</title>
    <link rel="stylesheet" href="{{{{ url_for('{agent_id}.static', filename='style.css') }}}}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="chat-container">
        <!-- Header -->
        <div class="chat-header">
            <div class="agent-info">
                <div class="agent-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="agent-details">
                    <h1>{agent_config['name']}</h1>
                    <p class="agent-description">{agent_config['description']}</p>
                    <span class="agent-status" id="status">Online</span>
                </div>
            </div>
            <div class="chat-controls">
                <button id="clearChat" class="btn btn-secondary">
                    <i class="fas fa-trash"></i> Clear
                </button>
                <button id="exportChat" class="btn btn-secondary">
                    <i class="fas fa-download"></i> Export
                </button>
            </div>
        </div>

        <!-- Messages Container -->
        <div class="messages-container" id="messagesContainer">
            <div class="welcome-message">
                <div class="agent-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <h3>Hello! I'm your {agent_config['name']}</h3>
                    <p>{agent_config['description']}. How can I help you today?</p>
                    
                    <div class="quick-actions">
                        <button class="quick-action" data-message="What are your main capabilities?">
                            <i class="fas fa-list"></i> Capabilities
                        </button>
                        <button class="quick-action" data-message="Can you help me get started?">
                            <i class="fas fa-play"></i> Get Started
                        </button>
                        <button class="quick-action" data-message="Show me some examples of what you can do">
                            <i class="fas fa-lightbulb"></i> Examples
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
            <div class="input-container">
                <textarea 
                    id="messageInput" 
                    placeholder="Type your message here..." 
                    rows="1"
                ></textarea>
                <button id="sendButton" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
            
            <!-- Typing Indicator -->
            <div class="typing-indicator" id="typingIndicator" style="display: none;">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <span class="typing-text">{agent_config['name']} is thinking...</span>
            </div>
        </div>

        <!-- Performance Metrics -->
        <div class="metrics-bar">
            <div class="metric">
                <span class="metric-label">Response Time:</span>
                <span class="metric-value" id="responseTime">0ms</span>
            </div>
            <div class="metric">
                <span class="metric-label">Confidence:</span>
                <span class="metric-value" id="confidence">0%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Model:</span>
                <span class="metric-value" id="modelUsed">{agent_config['primary_model']}</span>
            </div>
        </div>
    </div>

    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loadingOverlay" style="display: none;">
        <div class="loading-spinner">
            <i class="fas fa-cog fa-spin"></i>
        </div>
        <p>Processing your request...</p>
    </div>

    <script src="{{{{ url_for('{agent_id}.static', filename='utils.js') }}}}"></script>
    <script src="{{{{ url_for('{agent_id}.static', filename='{agent_id}.js') }}}}"></script>
</body>
</html>'''

    elif template_type == 'agent_css':
        return f'''/* {agent_config['name']} Styles */

:root {{
    --primary-color: {agent_config['color_theme']};
    --primary-light: {agent_config['color_theme']}20;
    --text-primary: #333;
    --text-secondary: #666;
    --background: #f8f9fa;
    --surface: #ffffff;
    --border: #e1e5e9;
    --shadow: 0 2px 10px rgba(0,0,0,0.1);
    --border-radius: 12px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: var(--background);
    color: var(--text-primary);
    line-height: 1.6;
}}

.chat-container {{
    max-width: 1200px;
    margin: 0 auto;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--surface);
    box-shadow: var(--shadow);
}}

/* Header Styles */
.chat-header {{
    background: var(--primary-color);
    color: white;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--shadow);
}}

.agent-info {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.agent-avatar {{
    width: 60px;
    height: 60px;
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}}

.agent-details h1 {{
    font-size: 1.5rem;
    margin-bottom: 0.25rem;
}}

.agent-description {{
    opacity: 0.9;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}}

.agent-status {{
    background: #28a745;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
}}

.chat-controls {{
    display: flex;
    gap: 0.5rem;
}}

.btn {{
    padding: 0.5rem 1rem;
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.3s ease;
}}

.btn-primary {{
    background: var(--primary-color);
    color: white;
}}

.btn-secondary {{
    background: rgba(255,255,255,0.2);
    color: white;
    border: 1px solid rgba(255,255,255,0.3);
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}}

/* Messages Container */
.messages-container {{
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
    background: var(--background);
}}

.welcome-message {{
    display: flex;
    gap: 1rem;
    background: var(--surface);
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    margin-bottom: 2rem;
}}

.welcome-message .agent-avatar {{
    background: var(--primary-light);
    color: var(--primary-color);
}}

.message-content h3 {{
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}}

.quick-actions {{
    display: flex;
    gap: 0.75rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}}

.quick-action {{
    background: var(--primary-light);
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}}

.quick-action:hover {{
    background: var(--primary-color);
    color: white;
}}

.message {{
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    animation: slideIn 0.3s ease;
}}

.message.user {{
    flex-direction: row-reverse;
}}

.message.user .message-bubble {{
    background: var(--primary-color);
    color: white;
}}

.message-bubble {{
    background: var(--surface);
    padding: 1rem 1.5rem;
    border-radius: var(--border-radius);
    max-width: 70%;
    box-shadow: var(--shadow);
    position: relative;
}}

.message-meta {{
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

/* Input Area */
.input-area {{
    background: var(--surface);
    padding: 1.5rem 2rem;
    border-top: 1px solid var(--border);
}}

.input-container {{
    display: flex;
    gap: 1rem;
    align-items: flex-end;
}}

#messageInput {{
    flex: 1;
    border: 2px solid var(--border);
    border-radius: var(--border-radius);
    padding: 1rem;
    font-size: 1rem;
    resize: none;
    min-height: 50px;
    max-height: 120px;
    transition: all 0.3s ease;
}}

#messageInput:focus {{
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px var(--primary-light);
}}

#sendButton {{
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Typing Indicator */
.typing-indicator {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.75rem;
    color: var(--text-secondary);
}}

.typing-dots {{
    display: flex;
    gap: 0.25rem;
}}

.typing-dots span {{
    width: 6px;
    height: 6px;
    background: var(--primary-color);
    border-radius: 50%;
    animation: typing 1.4s infinite;
}}

.typing-dots span:nth-child(2) {{
    animation-delay: 0.2s;
}}

.typing-dots span:nth-child(3) {{
    animation-delay: 0.4s;
}}

/* Metrics Bar */
.metrics-bar {{
    background: var(--surface);
    border-top: 1px solid var(--border);
    padding: 0.75rem 2rem;
    display: flex;
    gap: 2rem;
    justify-content: center;
    font-size: 0.85rem;
}}

.metric {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.metric-label {{
    color: var(--text-secondary);
}}

.metric-value {{
    color: var(--primary-color);
    font-weight: 600;
}}

/* Loading Overlay */
.loading-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    z-index: 1000;
}}

.loading-spinner {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

/* Animations */
@keyframes slideIn {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes typing {{
    0%, 60%, 100% {{
        transform: translateY(0);
    }}
    30% {{
        transform: translateY(-10px);
    }}
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .chat-header {{
        padding: 1rem;
        flex-direction: column;
        text-align: center;
        gap: 1rem;
    }}
    
    .messages-container {{
        padding: 1rem;
    }}
    
    .input-area {{
        padding: 1rem;
    }}
    
    .metrics-bar {{
        flex-direction: column;
        gap: 0.5rem;
        text-align: center;
    }}
    
    .message-bubble {{
        max-width: 85%;
    }}
}}'''

    else:
        return f'# {template_type} for {agent_id}\n# TODO: Implement {template_type}'

def create_agent_files(base_path: str):
    """Create all core files for each agent"""
    print("\n📄 Creating Agent Files...")
    
    for agent_id, agent_config in AGENTS_CONFIG.items():
        print(f"\n📝 Creating files for {agent_config['name']} ({agent_id})")
        
        agent_path = Path(base_path) / agent_id
        file_count = 0
        
        for file_template, template_type in CORE_FILES.items():
            # Replace placeholders in file paths
            file_path = file_template.format(agent_id=agent_id)
            full_path = agent_path / file_path
            
            # Generate content
            content = generate_file_content(template_type, agent_id, agent_config)
            
            # Write file
            full_path.write_text(content, encoding='utf-8')
            file_count += 1
            
            print(f"   ✅ {file_path}")
        
        print(f"   📄 Created {file_count} files for {agent_id}")

def generate_master_index():
    """Generate master index file for all agents"""
    print("\n📋 Generating Master Index...")
    
    index_content = '''# AI Agents Architecture Index

This directory contains the complete architecture for all 10 AI agents in the system.

## Agent Directory Structure

Each agent follows this comprehensive architecture:

```
agent_name/
├── __init__.py                    # Flask blueprint registration  
├── config.yaml                    # Agent configuration
├── registry.yaml                  # Multi-agent metadata
├── persona/                       # Persona definitions
│   └── agent_name.yaml
├── api/                           # REST + WebSocket endpoints
│   ├── routes.py                  # HTTP routes
│   ├── socket.py                  # WebSocket setup
│   └── events.py                  # WebSocket events
├── services/                      # Core business logic
│   ├── cortex/                    # Reasoning & orchestration
│   │   ├── controller.py          # Main controller
│   │   ├── planner.py             # Task planning
│   │   ├── executor.py            # Task execution
│   │   └── hooks.py               # Event hooks
│   ├── brain/                     # Memory & cognition
│   │   ├── chroma/                # Vector database
│   │   │   ├── embedder.py        # Text embeddings
│   │   │   ├── vector_store.py    # Vector storage
│   │   │   └── recall.py          # Memory recall
│   │   ├── episodic.py            # Episode memory
│   │   ├── feedback.py            # Learning feedback
│   │   └── memory_sync.py         # Memory synchronization
│   ├── engine/                    # AI model inference
│   │   ├── local_runner.py        # Local model execution
│   │   ├── api_runner.py          # API model execution  
│   │   └── dispatcher.py          # Model routing
│   ├── feed/                      # External data
│   │   ├── fetch.py               # Data fetching
│   │   └── preprocess.py          # Data preprocessing
│   └── auth/                      # Authentication
│       ├── token.py               # Token management
│       └── roles.py               # Role management
├── monitor/                       # Performance monitoring
│   ├── latency.py                 # Response time tracking
│   ├── usage.py                   # Usage analytics
│   └── alerts.py                  # Alert system
├── analytics/                     # User analytics
│   ├── logger.py                  # Interaction logging
│   └── metrics.py                 # Metrics collection
├── session/                       # Session management
│   ├── store.py                   # Session storage
│   └── cleanup.py                 # Session cleanup
├── templates/                     # Frontend templates
│   └── agent_name.html            # Chat interface
├── static/                        # Static assets
│   ├── style.css                  # Agent styling
│   ├── agent_name.js              # JavaScript logic
│   └── utils.js                   # Utility functions
└── tests/                         # Test suite
    ├── test_routes.py             # Route testing
    ├── test_controller.py         # Controller testing
    ├── test_memory.py             # Memory testing
    └── simulator.py               # Agent simulation
```

## Available Agents

'''
    
    for agent_id, agent_config in AGENTS_CONFIG.items():
        index_content += f'''### {agent_config['name']} (`{agent_id}`)
- **Description**: {agent_config['description']}
- **Primary Model**: {agent_config['primary_model']}
- **Personality**: {agent_config['personality']}
- **Color Theme**: {agent_config['color_theme']}
- **Endpoint**: `/ai/agents/{agent_id}/`

'''
    
    index_content += '''
## Usage

Each agent can be accessed via:
- **REST API**: `/ai/agents/{agent_id}/chat`
- **WebSocket**: `/ai/agents/{agent_id}/ws`
- **Web Interface**: `/ai/agents/{agent_id}/`

## Development

To extend an agent:
1. Modify the `config.yaml` for configuration changes
2. Update `persona/{agent_id}.yaml` for personality changes
3. Extend `services/cortex/controller.py` for new capabilities
4. Add routes in `api/routes.py` for new endpoints
5. Update tests in `tests/` directory

## Architecture Benefits

- **Modular**: Each agent is completely self-contained
- **Scalable**: Individual agents can be scaled independently
- **Maintainable**: Clear separation of concerns
- **Testable**: Comprehensive test coverage for each component
- **Extensible**: Easy to add new capabilities or agents
'''
    
    return index_content

def main():
    """Main execution function"""
    base_path = "/workspaces/3in1-portfolio-webdev-aiservices/app/ai/agents"
    
    print("🚀 AI Agent Architecture Generator")
    print("=" * 50)
    
    # Create directories
    create_agent_directories(base_path)
    
    # Create files
    create_agent_files(base_path)
    
    # Create master index
    index_content = generate_master_index()
    index_path = Path(base_path) / "README.md"
    index_path.write_text(index_content, encoding='utf-8')
    
    print(f"\n🎉 Successfully created complete architecture for all {len(AGENTS_CONFIG)} agents!")
    print(f"📍 Location: {base_path}")
    print(f"📚 Documentation: {index_path}")
    
    # Summary
    total_dirs = len(AGENTS_CONFIG) * len(DIRECTORY_STRUCTURE)
    total_files = len(AGENTS_CONFIG) * len(CORE_FILES)
    
    print(f"\n📊 Summary:")
    print(f"   🏗️  Total Directories Created: {total_dirs}")
    print(f"   📄 Total Files Created: {total_files}")
    print(f"   🤖 Agents Configured: {len(AGENTS_CONFIG)}")
    
    print(f"\n✨ Your 10-agent AI system is now ready for development!")

if __name__ == "__main__":
    main()