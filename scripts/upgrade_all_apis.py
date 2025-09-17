#!/usr/bin/env python3
"""
API Upgrade Script
Systematically upgrades all 16 agents with production-ready API modules
"""

import os
import shutil
from pathlib import Path

# Define all agents
PROFESSIONAL_AGENTS = [
    'developer', 'security_expert', 'content_creator', 'research_analyst', 
    'data_scientist', 'customer_success', 'product_manager', 'marketing_specialist', 
    'operations_manager'
]

ENTERTAINMENT_AGENTS = [
    'girlfriend', 'lazyjohn', 'gossipqueen', 'emotionaljenny', 'strictwife', 'coderbot'
]

ALL_AGENTS = PROFESSIONAL_AGENTS + ENTERTAINMENT_AGENTS

# Base directory
BASE_DIR = Path("/workspaces/3in1-portfolio-webdev-aiservices/agents")
TEMPLATE_AGENT = "strategist"

def get_agent_capabilities(agent_name):
    """Get capabilities specific to each agent"""
    capabilities_map = {
        'developer': ['code_development', 'architecture_design', 'code_review', 'debugging', 'testing', 'deployment'],
        'security_expert': ['security_analysis', 'vulnerability_assessment', 'penetration_testing', 'compliance', 'threat_modeling'],
        'content_creator': ['content_strategy', 'copywriting', 'seo_optimization', 'social_media', 'brand_messaging'],
        'research_analyst': ['market_research', 'data_analysis', 'trend_analysis', 'competitive_intelligence', 'reporting'],
        'data_scientist': ['data_analysis', 'machine_learning', 'statistical_modeling', 'predictive_analytics', 'data_visualization'],
        'customer_success': ['customer_support', 'relationship_management', 'retention_strategies', 'feedback_analysis'],
        'product_manager': ['product_strategy', 'roadmap_planning', 'feature_prioritization', 'user_research', 'stakeholder_management'],
        'marketing_specialist': ['marketing_strategy', 'campaign_management', 'brand_development', 'digital_marketing', 'analytics'],
        'operations_manager': ['process_optimization', 'resource_management', 'quality_assurance', 'workflow_design', 'performance_monitoring'],
        'girlfriend': ['emotional_support', 'relationship_advice', 'casual_conversation', 'companionship'],
        'lazyjohn': ['casual_chat', 'humor', 'relaxed_conversation', 'entertainment'],
        'gossipqueen': ['social_updates', 'trending_topics', 'celebrity_news', 'entertainment_gossip'],
        'emotionaljenny': ['emotional_intelligence', 'empathy', 'mood_support', 'personal_guidance'],
        'strictwife': ['discipline', 'organization', 'accountability', 'structured_guidance'],
        'coderbot': ['coding_assistance', 'programming_tutorials', 'code_debugging', 'technical_support']
    }
    return capabilities_map.get(agent_name, ['general_assistance', 'conversation', 'support'])

def create_routes_py(agent_name, agent_dir):
    """Create production-ready routes.py for an agent"""
    capabilities = get_agent_capabilities(agent_name)
    
    content = f'''"""
{agent_name.replace('_', ' ').title()} AI REST API Routes
Production-ready HTTP endpoints for {agent_name} agent
"""

from flask import Blueprint, request, jsonify, session, current_app
from functools import wraps
import asyncio
import traceback
import time
import uuid
from typing import Dict, Any, Optional

from ..services.cortex.controller import {agent_name.replace('_', '').title()}Controller
from ..monitor.usage import track_usage
from ..analytics.metrics import {agent_name.replace('_', '').title()}Metrics
from ..analytics.logger import {agent_name.replace('_', '').title()}AnalyticsLogger

# Initialize blueprint and services
{agent_name}_api = Blueprint('{agent_name}_api', __name__, url_prefix='/api/{agent_name}')
controller = {agent_name.replace('_', '').title()}Controller()
metrics = {agent_name.replace('_', '').title()}Metrics()
analytics_logger = {agent_name.replace('_', '').title()}AnalyticsLogger()

# Rate limiting configuration
RATE_LIMIT = 100  # requests per minute
rate_limit_store = {{}}

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        current_time = time.time()
        
        if client_ip not in rate_limit_store:
            rate_limit_store[client_ip] = []
        
        # Clean old requests
        rate_limit_store[client_ip] = [req_time for req_time in rate_limit_store[client_ip] if current_time - req_time < 60]
        
        if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
            return jsonify({{'error': 'Rate limit exceeded', 'code': 'RATE_LIMIT_EXCEEDED'}}), 429
        
        rate_limit_store[client_ip].append(current_time)
        return f(*args, **kwargs)
    return decorated_function

def validate_request(required_fields=None):
    """Request validation decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({{'error': 'Content-Type must be application/json', 'code': 'INVALID_CONTENT_TYPE'}}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({{'error': 'Request body cannot be empty', 'code': 'EMPTY_REQUEST'}}), 400
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data or not data[field]]
                if missing_fields:
                    return jsonify({{
                        'error': f'Missing required fields: {{", ".join(missing_fields)}}',
                        'code': 'MISSING_FIELDS',
                        'missing_fields': missing_fields
                    }}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@{agent_name}_api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({{
        'status': 'healthy',
        'agent': '{agent_name}',
        'version': '1.0.0',
        'timestamp': time.time(),
        'uptime': time.time() - current_app.config.get('START_TIME', time.time())
    }})

@{agent_name}_api.route('/chat', methods=['POST'])
@rate_limit
@validate_request(['message'])
@track_usage
def chat():
    """Handle chat requests with full error handling and analytics"""
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        context = data.get('context', {{}})
        
        # Validate message length
        if len(message) > 2000:
            return jsonify({{
                'error': 'Message too long (max 2000 characters)',
                'code': 'MESSAGE_TOO_LONG',
                'request_id': request_id
            }}), 400
        
        # Log request
        analytics_logger.log_request(
            request_id=request_id,
            message=message[:100] + '...' if len(message) > 100 else message,
            session_id=session_id,
            context=context
        )
        
        # Process request through controller
        response_data = controller.process_message(message, session_id, context)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Track metrics
        metrics.track_conversation(
            conversation_type='chat',
            duration=processing_time,
            satisfaction_score=None
        )
        
        # Prepare response
        response = {{
            'success': True,
            'data': response_data,
            'metadata': {{
                'request_id': request_id,
                'processing_time': processing_time,
                'session_id': session_id,
                'agent': '{agent_name}',
                'timestamp': time.time()
            }}
        }}
        
        # Log successful response
        analytics_logger.log_response(
            request_id=request_id,
            response=response_data,
            processing_time=processing_time,
            success=True
        )
        
        return jsonify(response)
        
    except Exception as e:
        # Calculate error time
        error_time = time.time() - start_time
        
        # Log error
        analytics_logger.log_error(
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
            processing_time=error_time
        )
        
        return jsonify({{
            'success': False,
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'request_id': request_id,
            'metadata': {{
                'processing_time': error_time,
                'timestamp': time.time()
            }}
        }}), 500

@{agent_name}_api.route('/analytics', methods=['GET'])
def get_analytics():
    """Get agent analytics and metrics"""
    try:
        analytics_data = {{
            'agent': '{agent_name}',
            'metrics': metrics.get_summary(),
            'performance': {{
                'total_conversations': metrics.conversation_count,
                'average_duration': metrics.average_duration,
                'success_rate': metrics.success_rate,
                'satisfaction_score': metrics.average_satisfaction
            }},
            'capabilities': {capabilities},
            'timestamp': time.time()
        }}
        
        return jsonify({{
            'success': True,
            'data': analytics_data
        }})
        
    except Exception as e:
        analytics_logger.log_error(
            request_id=str(uuid.uuid4()),
            error=str(e),
            traceback=traceback.format_exc()
        )
        
        return jsonify({{
            'success': False,
            'error': 'Failed to retrieve analytics',
            'code': 'ANALYTICS_ERROR'
        }}), 500
'''
    
    with open(agent_dir / "api" / "routes.py", 'w') as f:
        f.write(content)

def create_socket_py(agent_name, agent_dir):
    """Create production-ready socket.py for an agent"""
    capabilities = get_agent_capabilities(agent_name)
    
    content = f'''"""
{agent_name.replace('_', ' ').title()} AI WebSocket Handler
Production-ready real-time communication system
"""

import json
import asyncio
import uuid
import time
from typing import Dict, Any, Set, Optional
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask import request

from ..services.cortex.controller import {agent_name.replace('_', '').title()}Controller
from ..analytics.metrics import {agent_name.replace('_', '').title()}Metrics
from ..analytics.logger import {agent_name.replace('_', '').title()}AnalyticsLogger
from ..monitor.usage import track_websocket_usage

# Initialize services
controller = {agent_name.replace('_', '').title()}Controller()
metrics = {agent_name.replace('_', '').title()}Metrics()
analytics_logger = {agent_name.replace('_', '').title()}AnalyticsLogger()

# Connection management
active_sessions: Dict[str, Dict[str, Any]] = {{}}
session_rooms: Dict[str, str] = {{}}
connection_limits = {{'max_connections': 100, 'current': 0}}

class {agent_name.replace('_', '').title()}SocketHandler:
    """Production WebSocket handler for {agent_name.title()} agent"""
    
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup all WebSocket event handlers"""
        
        @self.socketio.on('connect', namespace='/{agent_name}')
        def handle_connect():
            """Handle client connection with validation and rate limiting"""
            try:
                # Check connection limits
                if connection_limits['current'] >= connection_limits['max_connections']:
                    emit('error', {{
                        'message': 'Maximum connections reached',
                        'code': 'CONNECTION_LIMIT'
                    }})
                    disconnect()
                    return False
                
                # Generate session
                session_id = str(uuid.uuid4())
                client_id = request.sid
                
                # Initialize session
                active_sessions[client_id] = {{
                    'session_id': session_id,
                    'connected_at': time.time(),
                    'last_activity': time.time(),
                    'message_count': 0,
                    'room': f'{agent_name}_{{session_id}}',
                    'authenticated': False
                }}
                
                # Join room
                room = active_sessions[client_id]['room']
                join_room(room)
                session_rooms[session_id] = room
                
                # Update connection count
                connection_limits['current'] += 1
                
                # Log connection
                analytics_logger.log_websocket_event(
                    event_type='connect',
                    session_id=session_id,
                    client_id=client_id,
                    metadata={{'room': room}}
                )
                
                # Send welcome message
                emit('connected', {{
                    'status': 'connected',
                    'session_id': session_id,
                    'agent': '{agent_name}',
                    'capabilities': {capabilities},
                    'timestamp': time.time()
                }})
                
                return True
                
            except Exception as e:
                analytics_logger.log_error(
                    request_id=str(uuid.uuid4()),
                    error=f"Connection error: {{str(e)}}",
                    traceback=str(e)
                )
                emit('error', {{'message': 'Connection failed', 'code': 'CONNECTION_ERROR'}})
                return False
        
        @self.socketio.on('disconnect', namespace='/{agent_name}')
        def handle_disconnect():
            """Handle client disconnection"""
            try:
                client_id = request.sid
                
                if client_id in active_sessions:
                    session_data = active_sessions[client_id]
                    session_id = session_data['session_id']
                    room = session_data['room']
                    
                    # Calculate session duration
                    duration = time.time() - session_data['connected_at']
                    
                    # Leave room
                    leave_room(room)
                    
                    # Clean up
                    del active_sessions[client_id]
                    if session_id in session_rooms:
                        del session_rooms[session_id]
                    
                    # Update connection count
                    connection_limits['current'] = max(0, connection_limits['current'] - 1)
                    
                    # Log disconnection
                    analytics_logger.log_websocket_event(
                        event_type='disconnect',
                        session_id=session_id,
                        client_id=client_id,
                        metadata={{
                            'duration': duration,
                            'message_count': session_data['message_count']
                        }}
                    )
                    
            except Exception as e:
                analytics_logger.log_error(
                    request_id=str(uuid.uuid4()),
                    error=f"Disconnection error: {{str(e)}}",
                    traceback=str(e)
                )
        
        @self.socketio.on('message', namespace='/{agent_name}')
        @track_websocket_usage
        def handle_message(data):
            """Handle incoming messages with full validation and processing"""
            start_time = time.time()
            client_id = request.sid
            request_id = str(uuid.uuid4())
            
            try:
                # Validate session
                if client_id not in active_sessions:
                    emit('error', {{
                        'message': 'Invalid session',
                        'code': 'INVALID_SESSION',
                        'request_id': request_id
                    }})
                    return
                
                session_data = active_sessions[client_id]
                session_id = session_data['session_id']
                
                # Update activity
                session_data['last_activity'] = time.time()
                session_data['message_count'] += 1
                
                # Rate limiting check
                if session_data['message_count'] > 50:  # per session
                    emit('error', {{
                        'message': 'Message limit exceeded for session',
                        'code': 'MESSAGE_LIMIT',
                        'request_id': request_id
                    }})
                    return
                
                # Validate message data
                if not isinstance(data, dict) or 'message' not in data:
                    emit('error', {{
                        'message': 'Invalid message format',
                        'code': 'INVALID_FORMAT',
                        'request_id': request_id
                    }})
                    return
                
                message = data.get('message', '').strip()
                if not message or len(message) > 2000:
                    emit('error', {{
                        'message': 'Invalid message length',
                        'code': 'INVALID_LENGTH',
                        'request_id': request_id
                    }})
                    return
                
                # Log incoming message
                analytics_logger.log_websocket_message(
                    session_id=session_id,
                    message_type='incoming',
                    message=message[:100] + '...' if len(message) > 100 else message,
                    request_id=request_id
                )
                
                # Process message
                context = data.get('context', {{}})
                response_data = controller.process_message(message, session_id, context)
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Track metrics
                metrics.track_conversation(
                    conversation_type='websocket_chat',
                    duration=processing_time,
                    satisfaction_score=None
                )
                
                # Send response
                response = {{
                    'type': 'response',
                    'data': response_data,
                    'metadata': {{
                        'request_id': request_id,
                        'processing_time': processing_time,
                        'session_id': session_id,
                        'agent': '{agent_name}',
                        'timestamp': time.time()
                    }}
                }}
                
                emit('response', response)
                
                # Log outgoing response
                analytics_logger.log_websocket_message(
                    session_id=session_id,
                    message_type='outgoing',
                    message=str(response_data)[:100] + '...' if len(str(response_data)) > 100 else str(response_data),
                    request_id=request_id,
                    processing_time=processing_time
                )
                
            except Exception as e:
                processing_time = time.time() - start_time
                
                analytics_logger.log_error(
                    request_id=request_id,
                    error=f"Message processing error: {{str(e)}}",
                    traceback=str(e),
                    processing_time=processing_time
                )
                
                emit('error', {{
                    'message': 'Failed to process message',
                    'code': 'PROCESSING_ERROR',
                    'request_id': request_id,
                    'metadata': {{
                        'processing_time': processing_time,
                        'timestamp': time.time()
                    }}
                }})
        
        @self.socketio.on('ping', namespace='/{agent_name}')
        def handle_ping():
            """Handle ping for connection health"""
            try:
                client_id = request.sid
                if client_id in active_sessions:
                    active_sessions[client_id]['last_activity'] = time.time()
                    emit('pong', {{'timestamp': time.time()}})
                else:
                    emit('error', {{'message': 'Invalid session', 'code': 'INVALID_SESSION'}})
            except Exception as e:
                emit('error', {{'message': 'Ping failed', 'code': 'PING_ERROR'}})

def get_connection_stats() -> Dict[str, Any]:
    """Get current WebSocket connection statistics"""
    return {{
        'active_connections': connection_limits['current'],
        'max_connections': connection_limits['max_connections'],
        'active_sessions': len(active_sessions),
        'session_details': {{
            session_id: {{
                'connected_duration': time.time() - data['connected_at'],
                'message_count': data['message_count'],
                'last_activity': time.time() - data['last_activity']
            }}
            for session_id, data in active_sessions.items()
        }}
    }}
'''
    
    with open(agent_dir / "api" / "socket.py", 'w') as f:
        f.write(content)

def create_events_py(agent_name, agent_dir):
    """Create production-ready events.py for an agent"""
    content = f'''"""
{agent_name.replace('_', ' ').title()} AI Event Handler
Production-ready event management system
"""

import json
import time
import uuid
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
from threading import Lock

from ..analytics.metrics import {agent_name.replace('_', '').title()}Metrics
from ..analytics.logger import {agent_name.replace('_', '').title()}AnalyticsLogger

class EventType(Enum):
    """Enumeration of all possible event types"""
    CONVERSATION_STARTED = "conversation_started"
    CONVERSATION_COMPLETED = "conversation_completed"
    REQUEST_PROCESSED = "request_processed"
    ERROR_OCCURRED = "error_occurred"
    SESSION_STARTED = "session_started"
    SESSION_ENDED = "session_ended"
    USER_FEEDBACK = "user_feedback"
    SYSTEM_STATUS = "system_status"
    PERFORMANCE_METRIC = "performance_metric"

@dataclass
class {agent_name.replace('_', '').title()}Event:
    """Standardized event structure for {agent_name} agent"""
    event_id: str
    event_type: EventType
    session_id: str
    timestamp: float
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=critical
    source: str = "{agent_name}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        result = asdict(self)
        result['event_type'] = self.event_type.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> '{agent_name.replace('_', '').title()}Event':
        """Create event from dictionary"""
        data['event_type'] = EventType(data['event_type'])
        return cls(**data)

class {agent_name.replace('_', '').title()}EventManager:
    """Production-ready event management for {agent_name} agent"""
    
    def __init__(self):
        self.event_handlers: Dict[EventType, List[Callable]] = {{}}
        self.event_history: List[{agent_name.replace('_', '').title()}Event] = []
        self.analytics = {agent_name.replace('_', '').title()}Metrics()
        self.logger = {agent_name.replace('_', '').title()}AnalyticsLogger()
        self._lock = Lock()
        self.max_history_size = 1000
        
    def register_handler(self, event_type: EventType, handler: Callable):
        """Register an event handler for specific event type"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        
    def unregister_handler(self, event_type: EventType, handler: Callable):
        """Unregister an event handler"""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
            except ValueError:
                pass
    
    def emit_event(self, event_type: EventType, session_id: str, data: Dict[str, Any], 
                   metadata: Optional[Dict[str, Any]] = None, priority: int = 1) -> str:
        """Emit a new event with validation and processing"""
        try:
            # Create event
            event = {agent_name.replace('_', '').title()}Event(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                session_id=session_id,
                timestamp=time.time(),
                data=data or {{}},
                metadata=metadata or {{}},
                priority=priority,
                source="{agent_name}"
            )
            
            # Store event
            with self._lock:
                self.event_history.append(event)
                
                # Limit history size
                if len(self.event_history) > self.max_history_size:
                    self.event_history = self.event_history[-self.max_history_size:]
            
            # Process event handlers
            self._process_event_handlers(event)
            
            # Log event
            self.logger.log_event(
                event_type=event_type.value,
                session_id=session_id,
                data=data,
                metadata=metadata,
                priority=priority
            )
            
            # Update analytics
            self._update_analytics(event)
            
            return event.event_id
            
        except Exception as e:
            self.logger.log_error(
                request_id=str(uuid.uuid4()),
                error=f"Event emission failed: {{str(e)}}",
                traceback=str(e)
            )
            raise
    
    def _process_event_handlers(self, event: {agent_name.replace('_', '').title()}Event):
        """Process all registered handlers for an event"""
        if event.event_type in self.event_handlers:
            for handler in self.event_handlers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    self.logger.log_error(
                        request_id=str(uuid.uuid4()),
                        error=f"Event handler failed: {{str(e)}}",
                        traceback=str(e)
                    )
    
    def _update_analytics(self, event: {agent_name.replace('_', '').title()}Event):
        """Update analytics based on event"""
        try:
            if event.event_type == EventType.CONVERSATION_COMPLETED:
                duration = event.data.get('duration', 0)
                satisfaction = event.data.get('satisfaction_score')
                
                self.analytics.track_conversation(
                    conversation_type=event.data.get('type', 'general'),
                    duration=duration,
                    satisfaction_score=satisfaction
                )
                    
        except Exception as e:
            self.logger.log_error(
                request_id=str(uuid.uuid4()),
                error=f"Analytics update failed: {{str(e)}}",
                traceback=str(e)
            )
    
    def get_events(self, session_id: Optional[str] = None, 
                   event_type: Optional[EventType] = None,
                   limit: int = 100) -> List[{agent_name.replace('_', '').title()}Event]:
        """Retrieve events with filtering"""
        with self._lock:
            events = self.event_history.copy()
        
        # Apply filters
        if session_id:
            events = [e for e in events if e.session_id == session_id]
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # Sort by timestamp (newest first) and limit
        events.sort(key=lambda x: x.timestamp, reverse=True)
        return events[:limit]

# Global event manager instance
event_manager = {agent_name.replace('_', '').title()}EventManager()

# Convenience functions for common events
def emit_conversation_started(session_id: str, conversation_type: str):
    """Emit conversation started event"""
    return event_manager.emit_event(
        EventType.CONVERSATION_STARTED,
        session_id,
        {{
            'conversation_type': conversation_type,
            'start_time': time.time()
        }},
        priority=2
    )

def emit_conversation_completed(session_id: str, duration: float, 
                               satisfaction_rating: Optional[int] = None):
    """Emit conversation completed event"""
    return event_manager.emit_event(
        EventType.CONVERSATION_COMPLETED,
        session_id,
        {{
            'duration': duration,
            'satisfaction_rating': satisfaction_rating,
            'completion_time': time.time()
        }},
        priority=2
    )

def emit_error_occurred(session_id: str, error_type: str, error_message: str, 
                       severity: str = 'medium'):
    """Emit error occurred event"""
    priority_map = {{'low': 1, 'medium': 2, 'high': 3, 'critical': 4}}
    return event_manager.emit_event(
        EventType.ERROR_OCCURRED,
        session_id,
        {{
            'error_type': error_type,
            'error_message': error_message,
            'severity': severity,
            'error_time': time.time()
        }},
        priority=priority_map.get(severity, 2)
    )
'''
    
    with open(agent_dir / "api" / "events.py", 'w') as f:
        f.write(content)

def create_init_py(agent_name, agent_dir):
    """Create production-ready __init__.py for an agent"""
    capabilities = get_agent_capabilities(agent_name)
    
    content = f'''"""
{agent_name.replace('_', ' ').title()} AI API Module
Production-ready API interface with REST endpoints, WebSocket support, and event management
"""

from .routes import {agent_name}_api
from .socket import {agent_name.replace('_', '').title()}SocketHandler, get_connection_stats
from .events import (
    event_manager,
    {agent_name.replace('_', '').title()}EventManager,
    EventType,
    {agent_name.replace('_', '').title()}Event,
    emit_conversation_started,
    emit_conversation_completed,
    emit_error_occurred
)

__all__ = [
    # REST API
    '{agent_name}_api',
    
    # WebSocket Handler
    '{agent_name.replace('_', '').title()}SocketHandler',
    'get_connection_stats',
    
    # Event Management
    'event_manager',
    '{agent_name.replace('_', '').title()}EventManager',
    'EventType',
    '{agent_name.replace('_', '').title()}Event',
    'emit_conversation_started',
    'emit_conversation_completed', 
    'emit_error_occurred'
]

# API version and metadata
API_VERSION = "1.0.0"
API_NAME = "{agent_name.replace('_', ' ').title()} AI API"
API_DESCRIPTION = "Production-ready API for {agent_name.replace('_', ' ').title()} AI Agent"

def get_api_info():
    """Get API information and status"""
    return {{
        'name': API_NAME,
        'version': API_VERSION,
        'description': API_DESCRIPTION,
        'agent': '{agent_name}',
        'capabilities': {capabilities},
        'endpoints': {{
            'rest': '/api/{agent_name}',
            'websocket': '/{agent_name}',
            'health': '/api/{agent_name}/health',
            'analytics': '/api/{agent_name}/analytics'
        }},
        'features': [
            'rate_limiting',
            'request_validation',
            'error_handling',
            'analytics_tracking',
            'websocket_support',
            'event_management',
            'session_management'
        ]
    }}
'''
    
    with open(agent_dir / "api" / "__init__.py", 'w') as f:
        f.write(content)

def upgrade_agent_api(agent_name):
    """Upgrade a single agent's API to production-ready status"""
    print(f"Upgrading {agent_name} API...")
    
    agent_dir = BASE_DIR / agent_name
    api_dir = agent_dir / "api"
    
    # Ensure API directory exists
    api_dir.mkdir(exist_ok=True)
    
    # Create all API files
    create_routes_py(agent_name, agent_dir)
    create_socket_py(agent_name, agent_dir)
    create_events_py(agent_name, agent_dir)
    create_init_py(agent_name, agent_dir)
    
    print(f"✅ {agent_name} API upgraded successfully")

def main():
    """Main upgrade function"""
    print("Starting API upgrade for all 15 agents (excluding strategist)...")
    
    success_count = 0
    error_count = 0
    
    for agent in ALL_AGENTS:
        try:
            upgrade_agent_api(agent)
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to upgrade {agent}: {e}")
            error_count += 1
    
    print(f"\n🎉 API upgrade completed!")
    print(f"✅ Successfully upgraded: {success_count} agents")
    if error_count > 0:
        print(f"❌ Failed to upgrade: {error_count} agents")
    
    # Summary
    print(f"\nTotal agents with production-ready APIs: {success_count + 1} (including strategist)")

if __name__ == "__main__":
    main()