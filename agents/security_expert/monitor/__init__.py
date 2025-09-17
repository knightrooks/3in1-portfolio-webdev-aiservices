"""
Security Expert AI Monitoring Module
Production-ready monitoring system
"""

from .usage import (
    SecurityexpertUsageMonitor,
    UsageMetric,
    usage_monitor,
    track_usage,
    track_websocket_usage
)

from .alerts import (
    SecurityexpertAlertManager,
    Alert,
    AlertSeverity,
    AlertType,
    alert_manager,
    trigger_alert
)

from .latency import (
    SecurityexpertLatencyMonitor,
    LatencyMeasurement,
    latency_monitor,
    track_latency
)

__all__ = [
    # Usage Monitoring
    'SecurityexpertUsageMonitor',
    'UsageMetric', 
    'usage_monitor',
    'track_usage',
    'track_websocket_usage',
    
    # Alert System
    'SecurityexpertAlertManager',
    'Alert',
    'AlertSeverity',
    'AlertType',
    'alert_manager',
    'trigger_alert',
    
    # Latency Monitoring
    'SecurityexpertLatencyMonitor',
    'LatencyMeasurement',
    'latency_monitor',
    'track_latency'
]

def get_monitoring_status():
    """Get current monitoring system status"""
    return {
        'usage_monitoring': {
            'active': True,
            'total_requests_tracked': len(usage_monitor.usage_history)
        },
        'alert_system': {
            'active': alert_manager.monitoring_active,
            'total_alerts': len(alert_manager.alerts),
            'active_alerts': len(alert_manager.get_active_alerts())
        },
        'latency_monitoring': {
            'active': True,
            'measurements_tracked': len(latency_monitor.measurements),
            'current_performance': latency_monitor.get_current_performance()
        }
    }
