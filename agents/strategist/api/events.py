"""
Business Strategist AI Event Handler
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

from ..analytics.metrics import StrategistMetrics
from ..analytics.logger import StrategistAnalyticsLogger


class EventType(Enum):
    """Enumeration of all possible event types"""

    CONSULTATION_STARTED = "consultation_started"
    CONSULTATION_COMPLETED = "consultation_completed"
    STRATEGY_GENERATED = "strategy_generated"
    MARKET_ANALYSIS = "market_analysis"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    BUSINESS_PLAN = "business_plan"
    GROWTH_STRATEGY = "growth_strategy"
    PERFORMANCE_METRIC = "performance_metric"
    ERROR_OCCURRED = "error_occurred"
    SESSION_STARTED = "session_started"
    SESSION_ENDED = "session_ended"
    USER_FEEDBACK = "user_feedback"
    SYSTEM_STATUS = "system_status"


@dataclass
class StrategistEvent:
    """Standardized event structure for strategist agent"""

    event_id: str
    event_type: EventType
    session_id: str
    timestamp: float
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=critical
    source: str = "strategist"

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        result = asdict(self)
        result["event_type"] = self.event_type.value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StrategistEvent":
        """Create event from dictionary"""
        data["event_type"] = EventType(data["event_type"])
        return cls(**data)


class StrategistEventManager:
    """Production-ready event management for strategist agent"""

    def __init__(self):
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.event_history: List[StrategistEvent] = []
        self.analytics = StrategistMetrics()
        self.logger = StrategistAnalyticsLogger()
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

    def emit_event(
        self,
        event_type: EventType,
        session_id: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        priority: int = 1,
    ) -> str:
        """Emit a new event with validation and processing"""
        try:
            # Create event
            event = StrategistEvent(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                session_id=session_id,
                timestamp=time.time(),
                data=data or {},
                metadata=metadata or {},
                priority=priority,
                source="strategist",
            )

            # Store event
            with self._lock:
                self.event_history.append(event)

                # Limit history size
                if len(self.event_history) > self.max_history_size:
                    self.event_history = self.event_history[-self.max_history_size :]

            # Process event handlers
            self._process_event_handlers(event)

            # Log event
            self.logger.log_event(
                event_type=event_type.value,
                session_id=session_id,
                data=data,
                metadata=metadata,
                priority=priority,
            )

            # Update analytics
            self._update_analytics(event)

            return event.event_id

        except Exception as e:
            self.logger.log_error(
                request_id=str(uuid.uuid4()),
                error=f"Event emission failed: {str(e)}",
                traceback=str(e),
            )
            raise

    def _process_event_handlers(self, event: StrategistEvent):
        """Process all registered handlers for an event"""
        if event.event_type in self.event_handlers:
            for handler in self.event_handlers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    self.logger.log_error(
                        request_id=str(uuid.uuid4()),
                        error=f"Event handler failed: {str(e)}",
                        traceback=str(e),
                    )

    def _update_analytics(self, event: StrategistEvent):
        """Update analytics based on event"""
        try:
            if event.event_type == EventType.CONSULTATION_COMPLETED:
                duration = event.data.get("duration", 0)
                consultation_type = event.data.get("type", "general")
                complexity = event.data.get("complexity", "moderate")
                deliverable = event.data.get("deliverable_type", "advice")

                self.analytics.track_consultation(
                    consultation_type=consultation_type,
                    complexity=complexity,
                    deliverable_type=deliverable,
                    execution_time=duration,
                )

            elif event.event_type == EventType.USER_FEEDBACK:
                rating = event.data.get("rating")
                if rating:
                    self.analytics.track_satisfaction(rating)

        except Exception as e:
            self.logger.log_error(
                request_id=str(uuid.uuid4()),
                error=f"Analytics update failed: {str(e)}",
                traceback=str(e),
            )

    def get_events(
        self,
        session_id: Optional[str] = None,
        event_type: Optional[EventType] = None,
        limit: int = 100,
    ) -> List[StrategistEvent]:
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

    def get_event_statistics(self) -> Dict[str, Any]:
        """Get comprehensive event statistics"""
        with self._lock:
            events = self.event_history.copy()

        if not events:
            return {"total_events": 0}

        # Calculate statistics
        event_counts = {}
        session_counts = {}
        priority_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for event in events:
            # Count by event type
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

            # Count by session
            session_counts[event.session_id] = (
                session_counts.get(event.session_id, 0) + 1
            )

            # Count by priority
            priority_counts[event.priority] += 1

        # Calculate time ranges
        timestamps = [e.timestamp for e in events]
        time_range = max(timestamps) - min(timestamps) if timestamps else 0

        return {
            "total_events": len(events),
            "event_types": event_counts,
            "active_sessions": len(session_counts),
            "session_distribution": session_counts,
            "priority_distribution": priority_counts,
            "time_range_seconds": time_range,
            "events_per_hour": (
                len(events) / (time_range / 3600) if time_range > 0 else 0
            ),
            "most_common_event": (
                max(event_counts.items(), key=lambda x: x[1])[0]
                if event_counts
                else None
            ),
            "recent_activity": len(
                [e for e in events if time.time() - e.timestamp < 3600]
            ),  # Last hour
        }

    def clear_old_events(self, max_age_hours: int = 24):
        """Clear events older than specified hours"""
        cutoff_time = time.time() - (max_age_hours * 3600)

        with self._lock:
            self.event_history = [
                event for event in self.event_history if event.timestamp > cutoff_time
            ]

    def export_events(
        self, session_id: Optional[str] = None, format: str = "json"
    ) -> str:
        """Export events to specified format"""
        events = self.get_events(session_id=session_id)
        event_dicts = [event.to_dict() for event in events]

        if format.lower() == "json":
            return json.dumps(event_dicts, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported export format: {format}")


# Global event manager instance
event_manager = StrategistEventManager()


# Convenience functions for common events
def emit_consultation_started(
    session_id: str, consultation_type: str, client_info: Dict[str, Any]
):
    """Emit consultation started event"""
    return event_manager.emit_event(
        EventType.CONSULTATION_STARTED,
        session_id,
        {
            "consultation_type": consultation_type,
            "client_info": client_info,
            "start_time": time.time(),
        },
        priority=2,
    )


def emit_consultation_completed(
    session_id: str,
    duration: float,
    deliverables: List[str],
    satisfaction_rating: Optional[int] = None,
):
    """Emit consultation completed event"""
    return event_manager.emit_event(
        EventType.CONSULTATION_COMPLETED,
        session_id,
        {
            "duration": duration,
            "deliverables": deliverables,
            "satisfaction_rating": satisfaction_rating,
            "completion_time": time.time(),
        },
        priority=2,
    )


def emit_strategy_generated(
    session_id: str,
    strategy_type: str,
    components: List[str],
    complexity: str = "moderate",
):
    """Emit strategy generated event"""
    return event_manager.emit_event(
        EventType.STRATEGY_GENERATED,
        session_id,
        {
            "strategy_type": strategy_type,
            "components": components,
            "complexity": complexity,
            "generation_time": time.time(),
        },
        priority=3,
    )


def emit_error_occurred(
    session_id: str, error_type: str, error_message: str, severity: str = "medium"
):
    """Emit error occurred event"""
    priority_map = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    return event_manager.emit_event(
        EventType.ERROR_OCCURRED,
        session_id,
        {
            "error_type": error_type,
            "error_message": error_message,
            "severity": severity,
            "error_time": time.time(),
        },
        priority=priority_map.get(severity, 2),
    )
