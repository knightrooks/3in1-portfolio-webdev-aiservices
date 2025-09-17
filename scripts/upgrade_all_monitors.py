#!/usr/bin/env python3
"""
Monitor Upgrade Script
Systematically upgrades all 16 agents with production-ready monitoring systems
"""

import os
from pathlib import Path

# Define all agents
ALL_AGENTS = [
    'strategist', 'developer', 'security_expert', 'content_creator', 'research_analyst', 
    'data_scientist', 'customer_success', 'product_manager', 'marketing_specialist', 
    'operations_manager', 'girlfriend', 'lazyjohn', 'gossipqueen', 'emotionaljenny', 
    'strictwife', 'coderbot'
]

# Base directory
BASE_DIR = Path("/workspaces/3in1-portfolio-webdev-aiservices/agents")

def get_agent_monitoring_context(agent_name):
    """Get monitoring context specific to each agent"""
    return {
        'class_name': agent_name.replace('_', '').title(),
        'display_name': agent_name.replace('_', ' ').title(),
        'namespace': agent_name
    }

def create_usage_py(agent_name, agent_dir):
    """Create production-ready usage.py for an agent"""
    context = get_agent_monitoring_context(agent_name)
    
    content = f'''"""
{context['display_name']} AI Usage Monitoring
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

class {context['class_name']}UsageMonitor:
    """Production usage monitoring for {context['namespace']} agent"""
    
    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self.usage_history: deque = deque(maxlen=max_history)
        self.session_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.endpoint_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {{
            'total_requests': 0,
            'total_duration': 0.0,
            'success_count': 0,
            'error_count': 0,
            'avg_duration': 0.0,
            'last_request': 0.0
        }})
        self.real_time_stats = {{
            'current_sessions': 0,
            'requests_per_minute': 0,
            'average_response_time': 0.0,
            'success_rate': 100.0,
            'cpu_usage': 0.0,
            'memory_usage': 0.0
        }}
        self._lock = Lock()
    
    def track_request(self, endpoint: str, method: str = 'POST') -> Callable:
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
                        agent='{context['namespace']}',
                        session_id='default',
                        endpoint=endpoint,
                        method=method,
                        timestamp=start_time,
                        duration=duration,
                        status_code=200,
                        cpu_usage=psutil.cpu_percent(),
                        memory_usage=psutil.virtual_memory().percent
                    )
                    
                    self.record_usage(usage_metric)
                    return result
                    
                except Exception as e:
                    duration = time.time() - start_time
                    
                    error_metric = UsageMetric(
                        metric_id=metric_id,
                        agent='{context['namespace']}',
                        session_id='default',
                        endpoint=endpoint,
                        method=method,
                        timestamp=start_time,
                        duration=duration,
                        status_code=500,
                        cpu_usage=psutil.cpu_percent(),
                        memory_usage=psutil.virtual_memory().percent,
                        error_message=str(e)
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
                return {{'total_requests': 0}}
            
            error_count = sum(1 for m in self.usage_history if m.status_code >= 400)
            success_rate = ((total_requests - error_count) / total_requests) * 100
            
            return {{
                'total_requests': total_requests,
                'error_count': error_count,
                'success_rate': success_rate,
                'timestamp': time.time()
            }}

# Global usage monitor instance
usage_monitor = {context['class_name']}UsageMonitor()

# Convenience decorators
def track_usage(func: Callable) -> Callable:
    """Simple usage tracking decorator"""
    return usage_monitor.track_request('api_call')(func)

def track_websocket_usage(func: Callable) -> Callable:
    """WebSocket usage tracking decorator"""
    return usage_monitor.track_request('websocket', method='WEBSOCKET')(func)
'''
    
    with open(agent_dir / "monitor" / "usage.py", 'w') as f:
        f.write(content)

def create_alerts_py(agent_name, agent_dir):
    """Create production-ready alerts.py for an agent"""
    context = get_agent_monitoring_context(agent_name)
    
    content = f'''"""
{context['display_name']} AI Alert System
Production-ready monitoring alerts and notifications
"""

import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from threading import Lock, Thread

class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    """Types of alerts that can be triggered"""
    HIGH_ERROR_RATE = "high_error_rate"
    SLOW_RESPONSE_TIME = "slow_response_time"
    HIGH_CPU_USAGE = "high_cpu_usage"
    HIGH_MEMORY_USAGE = "high_memory_usage"
    SYSTEM_OVERLOAD = "system_overload"

@dataclass
class Alert:
    """Alert data structure"""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    timestamp: float
    agent: str
    metrics: Dict[str, Any]
    resolved: bool = False

class {context['class_name']}AlertManager:
    """Production alert management for {context['namespace']} agent"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self._lock = Lock()
        self.monitoring_active = True
    
    def trigger_alert(self, alert_type: AlertType, severity: AlertSeverity, 
                     title: str, message: str, metrics: Dict[str, Any] = None):
        """Trigger a new alert"""
        alert = Alert(
            alert_id=f"alert_{{int(time.time() * 1000)}}",
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            timestamp=time.time(),
            agent="{context['namespace']}",
            metrics=metrics or {{}}
        )
        
        with self._lock:
            self.alerts.append(alert)
        
        return alert
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all unresolved alerts"""
        with self._lock:
            return [alert for alert in self.alerts if not alert.resolved]
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        with self._lock:
            total_alerts = len(self.alerts)
            if total_alerts == 0:
                return {{'total_alerts': 0, 'active_alerts': 0}}
            
            active_alerts = len([a for a in self.alerts if not a.resolved])
            
            return {{
                'total_alerts': total_alerts,
                'active_alerts': active_alerts
            }}

# Global alert manager instance
alert_manager = {context['class_name']}AlertManager()

def trigger_alert(alert_type: AlertType, severity: AlertSeverity, 
                 title: str, message: str, metrics: Dict[str, Any] = None):
    """Manually trigger an alert"""
    return alert_manager.trigger_alert(alert_type, severity, title, message, metrics)
'''
    
    with open(agent_dir / "monitor" / "alerts.py", 'w') as f:
        f.write(content)

def create_latency_py(agent_name, agent_dir):
    """Create production-ready latency.py for an agent"""
    context = get_agent_monitoring_context(agent_name)
    
    content = f'''"""
{context['display_name']} AI Latency Monitoring
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

class {context['class_name']}LatencyMonitor:
    """Production latency monitoring for {context['namespace']} agent"""
    
    def __init__(self, max_measurements: int = 1000):
        self.max_measurements = max_measurements
        self.measurements: deque = deque(maxlen=max_measurements)
        self._lock = Lock()
        
        # Performance thresholds (in seconds)
        self.thresholds = {{
            'excellent': 0.1,
            'good': 0.5,
            'acceptable': 1.0,
            'poor': 2.0,
            'unacceptable': 5.0
        }}
    
    def measure_latency(self, operation: str = 'api_call') -> Callable:
        """Decorator to measure function latency"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                measurement_id = f"{{operation}}_{{int(start_time * 1000)}}"
                
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
                        success=True
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
                        error_message=str(e)
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
                return {{'performance_grade': 'excellent', 'avg_latency': 0}}
            
            recent_measurements = list(self.measurements)[-100:]  # Last 100
            durations = [m.duration for m in recent_measurements]
            avg_latency = statistics.mean(durations)
            
            return {{
                'avg_latency': avg_latency,
                'performance_grade': self._grade_performance(avg_latency),
                'recent_requests': len(recent_measurements)
            }}
    
    def _grade_performance(self, avg_latency: float) -> str:
        """Grade performance based on average latency"""
        if avg_latency <= self.thresholds['excellent']:
            return 'excellent'
        elif avg_latency <= self.thresholds['good']:
            return 'good'
        elif avg_latency <= self.thresholds['acceptable']:
            return 'acceptable'
        elif avg_latency <= self.thresholds['poor']:
            return 'poor'
        else:
            return 'unacceptable'

# Global latency monitor instance
latency_monitor = {context['class_name']}LatencyMonitor()

def track_latency(operation: str = 'api_call'):
    """Simple latency tracking decorator"""
    return latency_monitor.measure_latency(operation)
'''
    
    with open(agent_dir / "monitor" / "latency.py", 'w') as f:
        f.write(content)

def create_init_py(agent_name, agent_dir):
    """Create production-ready __init__.py for an agent"""
    context = get_agent_monitoring_context(agent_name)
    
    content = f'''"""
{context['display_name']} AI Monitoring Module
Production-ready monitoring system
"""

from .usage import (
    {context['class_name']}UsageMonitor,
    UsageMetric,
    usage_monitor,
    track_usage,
    track_websocket_usage
)

from .alerts import (
    {context['class_name']}AlertManager,
    Alert,
    AlertSeverity,
    AlertType,
    alert_manager,
    trigger_alert
)

from .latency import (
    {context['class_name']}LatencyMonitor,
    LatencyMeasurement,
    latency_monitor,
    track_latency
)

__all__ = [
    # Usage Monitoring
    '{context['class_name']}UsageMonitor',
    'UsageMetric', 
    'usage_monitor',
    'track_usage',
    'track_websocket_usage',
    
    # Alert System
    '{context['class_name']}AlertManager',
    'Alert',
    'AlertSeverity',
    'AlertType',
    'alert_manager',
    'trigger_alert',
    
    # Latency Monitoring
    '{context['class_name']}LatencyMonitor',
    'LatencyMeasurement',
    'latency_monitor',
    'track_latency'
]

def get_monitoring_status():
    """Get current monitoring system status"""
    return {{
        'usage_monitoring': {{
            'active': True,
            'total_requests_tracked': len(usage_monitor.usage_history)
        }},
        'alert_system': {{
            'active': alert_manager.monitoring_active,
            'total_alerts': len(alert_manager.alerts),
            'active_alerts': len(alert_manager.get_active_alerts())
        }},
        'latency_monitoring': {{
            'active': True,
            'measurements_tracked': len(latency_monitor.measurements),
            'current_performance': latency_monitor.get_current_performance()
        }}
    }}
'''
    
    with open(agent_dir / "monitor" / "__init__.py", 'w') as f:
        f.write(content)

def upgrade_agent_monitor(agent_name):
    """Upgrade a single agent's monitor to production-ready status"""
    print(f"Upgrading {agent_name} monitor...")
    
    agent_dir = BASE_DIR / agent_name
    monitor_dir = agent_dir / "monitor"
    
    # Ensure monitor directory exists
    monitor_dir.mkdir(exist_ok=True)
    
    # Create all monitor files
    create_usage_py(agent_name, agent_dir)
    create_alerts_py(agent_name, agent_dir)
    create_latency_py(agent_name, agent_dir)
    create_init_py(agent_name, agent_dir)
    
    print(f"✅ {agent_name} monitor upgraded successfully")

def main():
    """Main upgrade function"""
    print("Starting monitor upgrade for all 16 agents...")
    
    success_count = 0
    error_count = 0
    
    for agent in ALL_AGENTS:
        try:
            upgrade_agent_monitor(agent)
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to upgrade {agent}: {e}")
            error_count += 1
    
    print(f"\n🎉 Monitor upgrade completed!")
    print(f"✅ Successfully upgraded: {success_count} agents")
    if error_count > 0:
        print(f"❌ Failed to upgrade: {error_count} agents")
    
    print(f"\nTotal agents with production-ready monitors: {success_count}")

if __name__ == "__main__":
    main()
