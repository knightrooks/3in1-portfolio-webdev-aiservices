"""
Girlfriend AI Event Handler
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

from ..analytics.metrics import GirlfriendMetrics
from ..analytics.logger import GirlfriendAnalyticsLogger

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
class GirlfriendEvent:
    """Standardized event structure for girlfriend agent"""
    event_id: str
    event_type: EventType
    session_id: str
    timestamp: float
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=critical
    source: str = "girlfriend"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        result = asdict(self)
        result['event_type'] = self.event_type.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GirlfriendEvent':
        """Create event from dictionary"""
        data['event_type'] = EventType(data['event_type'])
        return cls(**data)

class GirlfriendEventManager:
    """Production-ready event management for girlfriend agent"""
    
    def __init__(self):
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.event_history: List[GirlfriendEvent] = []
        self.analytics = GirlfriendMetrics()
        self.logger = GirlfriendAnalyticsLogger()
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
            event = GirlfriendEvent(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                session_id=session_id,
                timestamp=time.time(),
                data=data or {},
                metadata=metadata or {},
                priority=priority,
                source="girlfriend"
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
                error=f"Event emission failed: {str(e)}",
                traceback=str(e)
            )
            raise
    
    def _process_event_handlers(self, event: GirlfriendEvent):
        """Process all registered handlers for an event"""
        if event.event_type in self.event_handlers:
            for handler in self.event_handlers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    self.logger.log_error(
                        request_id=str(uuid.uuid4()),
                        error=f"Event handler failed: {str(e)}",
                        traceback=str(e)
                    )
    
    def _update_analytics(self, event: GirlfriendEvent):
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
                error=f"Analytics update failed: {str(e)}",
                traceback=str(e)
            )
    
    def get_events(self, session_id: Optional[str] = None, 
                   event_type: Optional[EventType] = None,
                   limit: int = 100) -> List[GirlfriendEvent]:
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
event_manager = GirlfriendEventManager()

# Convenience functions for common events
def emit_conversation_started(session_id: str, conversation_type: str):
    """Emit conversation started event"""
    return event_manager.emit_event(
        EventType.CONVERSATION_STARTED,
        session_id,
        {
            'conversation_type': conversation_type,
            'start_time': time.time()
        },
        priority=2
    )

def emit_conversation_completed(session_id: str, duration: float, 
                               satisfaction_rating: Optional[int] = None):
    """Emit conversation completed event"""
    return event_manager.emit_event(
        EventType.CONVERSATION_COMPLETED,
        session_id,
        {
            'duration': duration,
            'satisfaction_rating': satisfaction_rating,
            'completion_time': time.time()
        },
        priority=2
    )

def emit_error_occurred(session_id: str, error_type: str, error_message: str, 
                       severity: str = 'medium'):
    """Emit error occurred event"""
    priority_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
    return event_manager.emit_event(
        EventType.ERROR_OCCURRED,
        session_id,
        {
            'error_type': error_type,
            'error_message': error_message,
            'severity': severity,
            'error_time': time.time()
        },
        priority=priority_map.get(severity, 2)
    )
