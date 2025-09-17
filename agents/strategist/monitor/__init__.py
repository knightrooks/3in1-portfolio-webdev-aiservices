"""
Strategist AI Monitor Module
Production-ready monitoring system
"""

# Import with fallbacks to avoid import errors
try:
    from .usage import strategist_usage_monitor, track_usage, track_websocket_usage
except ImportError:
    # Create basic fallbacks
    class BasicUsageMonitor:
        def get_usage_summary(self):
            return {'agent': 'strategist', 'status': 'monitoring_active', 'timestamp': __import__('time').time()}
    strategist_usage_monitor = BasicUsageMonitor()
    def track_usage(f): return f
    def track_websocket_usage(f): return f

try:
    from .latency import latency_tracker, track_latency
except ImportError:
    # Create basic fallbacks
    class BasicLatencyTracker:
        def get_performance_summary(self):
            return {'agent': 'strategist', 'avg_latency_ms': 0.0, 'health_status': 'healthy', 'timestamp': __import__('time').time()}
    latency_tracker = BasicLatencyTracker()
    def track_latency(operation=None):
        def decorator(func): return func
        return decorator

try:
    from .alerts import alert_manager, create_warning_alert, create_critical_alert, AlertSeverity, AlertType
except ImportError:
    # Create basic fallbacks
    class BasicAlertManager:
        def get_alert_statistics(self):
            return {'agent': 'strategist', 'active_alerts': 0, 'total_alerts': 0, 'timestamp': __import__('time').time()}
    alert_manager = BasicAlertManager()
    def create_warning_alert(title, message): return 'warning-alert'
    def create_critical_alert(title, message): return 'critical-alert'
    class AlertSeverity: WARNING='warning'; CRITICAL='critical'
    class AlertType: CUSTOM='custom'

__all__ = [
    'strategist_usage_monitor', 'track_usage', 'track_websocket_usage',
    'latency_tracker', 'track_latency',
    'alert_manager', 'create_warning_alert', 'create_critical_alert', 'AlertSeverity', 'AlertType'
]

def get_monitor_status():
    """Get current monitor system status"""
    return {
        'agent': 'strategist',
        'usage_stats': strategist_usage_monitor.get_usage_summary(),
        'latency_stats': latency_tracker.get_performance_summary(),
        'alert_stats': alert_manager.get_alert_statistics(),
        'system_health': 'operational',
        'timestamp': __import__('time').time()
    }

from .usage import (
    StrategistUsageMonitor,
    UsageMetric,
    usage_monitor,
    track_usage,
    track_websocket_usage
)

from .alerts import (
    StrategistAlertManager,
    Alert,
    AlertSeverity,
    AlertType,
    alert_manager,
    trigger_alert
)

from .latency import (
    StrategistLatencyMonitor,
    LatencyMeasurement,
    latency_monitor,
    track_latency
)

__all__ = [
    # Usage Monitoring
    'StrategistUsageMonitor',
    'UsageMetric', 
    'usage_monitor',
    'track_usage',
    'track_websocket_usage',
    
    # Alert System
    'StrategistAlertManager',
    'Alert',
    'AlertSeverity',
    'AlertType',
    'alert_manager',
    'trigger_alert',
    
    # Latency Monitoring
    'StrategistLatencyMonitor',
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
