"""
Developer AI Alert System
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

class DeveloperAlertManager:
    """Production alert management for developer agent"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self._lock = Lock()
        self.monitoring_active = True
    
    def trigger_alert(self, alert_type: AlertType, severity: AlertSeverity, 
                     title: str, message: str, metrics: Dict[str, Any] = None):
        """Trigger a new alert"""
        alert = Alert(
            alert_id=f"alert_{int(time.time() * 1000)}",
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            timestamp=time.time(),
            agent="developer",
            metrics=metrics or {}
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
                return {'total_alerts': 0, 'active_alerts': 0}
            
            active_alerts = len([a for a in self.alerts if not a.resolved])
            
            return {
                'total_alerts': total_alerts,
                'active_alerts': active_alerts
            }

# Global alert manager instance
alert_manager = DeveloperAlertManager()

def trigger_alert(alert_type: AlertType, severity: AlertSeverity, 
                 title: str, message: str, metrics: Dict[str, Any] = None):
    """Manually trigger an alert"""
    return alert_manager.trigger_alert(alert_type, severity, title, message, metrics)
