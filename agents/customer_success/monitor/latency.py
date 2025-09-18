"""
Customer Success AI Latency Monitoring
Production-ready latency tracking and performance analysis
"""

import time
import statistics
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from functools import wraps
from threading import Lock
from collections import deque


@dataclass
class LatencyMeasurement:
    """Individual latency measurement"""

    measurement_id: str
    operation: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    error_message: Optional[str] = None


class CustomersuccessLatencyMonitor:
    """Production latency monitoring for customer_success agent"""

    def __init__(self, max_measurements: int = 1000):
        self.max_measurements = max_measurements
        self.measurements: deque = deque(maxlen=max_measurements)
        self._lock = Lock()

        # Performance thresholds (in seconds)
        self.thresholds = {
            "excellent": 0.1,
            "good": 0.5,
            "acceptable": 1.0,
            "poor": 2.0,
            "unacceptable": 5.0,
        }

    def measure_latency(self, operation: str = "api_call") -> Callable:
        """Decorator to measure function latency"""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                measurement_id = f"{operation}_{int(start_time * 1000)}"

                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    duration = end_time - start_time

                    measurement = LatencyMeasurement(
                        measurement_id=measurement_id,
                        operation=operation,
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        success=True,
                    )

                    self.record_measurement(measurement)
                    return result

                except Exception as e:
                    end_time = time.time()
                    duration = end_time - start_time

                    measurement = LatencyMeasurement(
                        measurement_id=measurement_id,
                        operation=operation,
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        success=False,
                        error_message=str(e),
                    )

                    self.record_measurement(measurement)
                    raise

            return wrapper

        return decorator

    def record_measurement(self, measurement: LatencyMeasurement):
        """Record a latency measurement"""
        with self._lock:
            self.measurements.append(measurement)

    def get_current_performance(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        with self._lock:
            if not self.measurements:
                return {"performance_grade": "excellent", "avg_latency": 0}

            recent_measurements = list(self.measurements)[-100:]  # Last 100
            durations = [m.duration for m in recent_measurements]
            avg_latency = statistics.mean(durations)

            return {
                "avg_latency": avg_latency,
                "performance_grade": self._grade_performance(avg_latency),
                "recent_requests": len(recent_measurements),
            }

    def _grade_performance(self, avg_latency: float) -> str:
        """Grade performance based on average latency"""
        if avg_latency <= self.thresholds["excellent"]:
            return "excellent"
        elif avg_latency <= self.thresholds["good"]:
            return "good"
        elif avg_latency <= self.thresholds["acceptable"]:
            return "acceptable"
        elif avg_latency <= self.thresholds["poor"]:
            return "poor"
        else:
            return "unacceptable"


# Global latency monitor instance
latency_monitor = CustomersuccessLatencyMonitor()


def track_latency(operation: str = "api_call"):
    """Simple latency tracking decorator"""
    return latency_monitor.measure_latency(operation)
