"""
Girlfriend AI Usage Monitoring
Production-ready usage tracking and analysis system
"""

import time
import json
import uuid
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from functools import wraps
from threading import Lock
from collections import defaultdict, deque
import psutil
import os


@dataclass
class UsageMetric:
    """Individual usage metric data structure"""

    metric_id: str
    agent: str
    session_id: str
    endpoint: str
    method: str
    timestamp: float
    duration: float
    status_code: int
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    request_size: int = 0
    response_size: int = 0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    error_message: Optional[str] = None


class GirlfriendUsageMonitor:
    """Production usage monitoring for girlfriend agent"""

    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self.usage_history: deque = deque(maxlen=max_history)
        self.session_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.endpoint_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "total_requests": 0,
                "total_duration": 0.0,
                "success_count": 0,
                "error_count": 0,
                "avg_duration": 0.0,
                "last_request": 0.0,
            }
        )
        self.real_time_stats = {
            "current_sessions": 0,
            "requests_per_minute": 0,
            "average_response_time": 0.0,
            "success_rate": 100.0,
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
        }
        self._lock = Lock()

    def track_request(self, endpoint: str, method: str = "POST") -> Callable:
        """Decorator to track API request usage"""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                metric_id = str(uuid.uuid4())

                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time

                    usage_metric = UsageMetric(
                        metric_id=metric_id,
                        agent="girlfriend",
                        session_id="default",
                        endpoint=endpoint,
                        method=method,
                        timestamp=start_time,
                        duration=duration,
                        status_code=200,
                        cpu_usage=psutil.cpu_percent(),
                        memory_usage=psutil.virtual_memory().percent,
                    )

                    self.record_usage(usage_metric)
                    return result

                except Exception as e:
                    duration = time.time() - start_time

                    error_metric = UsageMetric(
                        metric_id=metric_id,
                        agent="girlfriend",
                        session_id="default",
                        endpoint=endpoint,
                        method=method,
                        timestamp=start_time,
                        duration=duration,
                        status_code=500,
                        cpu_usage=psutil.cpu_percent(),
                        memory_usage=psutil.virtual_memory().percent,
                        error_message=str(e),
                    )

                    self.record_usage(error_metric)
                    raise

            return wrapper

        return decorator

    def record_usage(self, metric: UsageMetric):
        """Record a usage metric"""
        with self._lock:
            self.usage_history.append(metric)

    def get_usage_summary(self) -> Dict[str, Any]:
        """Get comprehensive usage summary"""
        with self._lock:
            total_requests = len(self.usage_history)
            if total_requests == 0:
                return {"total_requests": 0}

            error_count = sum(1 for m in self.usage_history if m.status_code >= 400)
            success_rate = ((total_requests - error_count) / total_requests) * 100

            return {
                "total_requests": total_requests,
                "error_count": error_count,
                "success_rate": success_rate,
                "timestamp": time.time(),
            }


# Global usage monitor instance
usage_monitor = GirlfriendUsageMonitor()


# Convenience decorators
def track_usage(func: Callable) -> Callable:
    """Simple usage tracking decorator"""
    return usage_monitor.track_request("api_call")(func)


def track_websocket_usage(func: Callable) -> Callable:
    """WebSocket usage tracking decorator"""
    return usage_monitor.track_request("websocket", method="WEBSOCKET")(func)
