"""
Health check and metrics endpoint for monitoring
"""

import os
import time
from datetime import datetime, timedelta

import psutil
import redis
import sqlalchemy
from flask import Blueprint, current_app, jsonify

from app.models import db
from app.services.cache import get_redis_client

health_bp = Blueprint("health", __name__)


class HealthChecker:
    """Comprehensive health checking system"""

    def __init__(self):
        self.checks = {
            "database": self._check_database,
            "redis": self._check_redis,
            "disk_space": self._check_disk_space,
            "memory": self._check_memory,
            "services": self._check_services,
        }

    def _check_database(self):
        """Check database connectivity and performance"""
        try:
            start_time = time.time()

            # Test connection
            with db.engine.connect() as conn:
                result = conn.execute(sqlalchemy.text("SELECT 1"))
                result.fetchone()

            response_time = (time.time() - start_time) * 1000  # ms

            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "details": "Database connection successful",
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "details": "Database connection failed",
            }

    def _check_redis(self):
        """Check Redis connectivity and performance"""
        try:
            start_time = time.time()

            redis_client = get_redis_client()
            redis_client.ping()

            # Test set/get operation
            test_key = "health_check_test"
            redis_client.set(test_key, "test_value", ex=60)
            value = redis_client.get(test_key)
            redis_client.delete(test_key)

            response_time = (time.time() - start_time) * 1000  # ms

            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "details": "Redis connection and operations successful",
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "details": "Redis connection failed",
            }

    def _check_disk_space(self):
        """Check disk space availability"""
        try:
            disk_usage = psutil.disk_usage("/")
            free_percent = (disk_usage.free / disk_usage.total) * 100

            if free_percent < 10:
                status = "critical"
                details = "Very low disk space"
            elif free_percent < 20:
                status = "warning"
                details = "Low disk space"
            else:
                status = "healthy"
                details = "Sufficient disk space"

            return {
                "status": status,
                "free_percent": round(free_percent, 2),
                "free_gb": round(disk_usage.free / (1024**3), 2),
                "total_gb": round(disk_usage.total / (1024**3), 2),
                "details": details,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "details": "Could not check disk space",
            }

    def _check_memory(self):
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            used_percent = memory.percent

            if used_percent > 90:
                status = "critical"
                details = "Very high memory usage"
            elif used_percent > 80:
                status = "warning"
                details = "High memory usage"
            else:
                status = "healthy"
                details = "Normal memory usage"

            return {
                "status": status,
                "used_percent": used_percent,
                "available_gb": round(memory.available / (1024**3), 2),
                "total_gb": round(memory.total / (1024**3), 2),
                "details": details,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "details": "Could not check memory usage",
            }

    def _check_services(self):
        """Check external service connectivity"""
        services = {}

        # Check AI service endpoints
        ai_services = [
            ("OpenAI", os.getenv("OPENAI_API_KEY")),
            ("Anthropic", os.getenv("ANTHROPIC_API_KEY")),
        ]

        for service_name, api_key in ai_services:
            if api_key:
                services[service_name.lower()] = {
                    "status": "configured",
                    "details": f"{service_name} API key configured",
                }
            else:
                services[service_name.lower()] = {
                    "status": "not_configured",
                    "details": f"{service_name} API key not configured",
                }

        # Check payment services
        stripe_key = os.getenv("STRIPE_SECRET_KEY")
        paypal_key = os.getenv("PAYPAL_CLIENT_SECRET")

        services["stripe"] = {
            "status": "configured" if stripe_key else "not_configured",
            "details": "Stripe configured" if stripe_key else "Stripe not configured",
        }

        services["paypal"] = {
            "status": "configured" if paypal_key else "not_configured",
            "details": "PayPal configured" if paypal_key else "PayPal not configured",
        }

        return {
            "status": "healthy",
            "services": services,
            "details": "Service configuration checked",
        }

    def run_all_checks(self):
        """Run all health checks and return results"""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "healthy",
            "checks": {},
            "summary": {},
        }

        healthy_count = 0
        warning_count = 0
        critical_count = 0
        unhealthy_count = 0

        for check_name, check_func in self.checks.items():
            try:
                check_result = check_func()
                results["checks"][check_name] = check_result

                status = check_result.get("status", "unknown")
                if status == "healthy":
                    healthy_count += 1
                elif status == "warning":
                    warning_count += 1
                elif status == "critical":
                    critical_count += 1
                else:
                    unhealthy_count += 1

            except Exception as e:
                results["checks"][check_name] = {
                    "status": "error",
                    "error": str(e),
                    "details": f"Health check {check_name} failed",
                }
                unhealthy_count += 1

        # Determine overall status
        if critical_count > 0 or unhealthy_count > 0:
            results["status"] = "unhealthy"
        elif warning_count > 0:
            results["status"] = "degraded"
        else:
            results["status"] = "healthy"

        results["summary"] = {
            "total_checks": len(self.checks),
            "healthy": healthy_count,
            "warning": warning_count,
            "critical": critical_count,
            "unhealthy": unhealthy_count,
        }

        return results


# Initialize health checker
health_checker = HealthChecker()


@health_bp.route("/health")
def health_check():
    """Basic health check endpoint"""
    try:
        # Quick database check
        with db.engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))

        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "portfolio-platform",
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "timestamp": datetime.utcnow().isoformat(),
                    "service": "portfolio-platform",
                    "error": str(e),
                }
            ),
            503,
        )


@health_bp.route("/health/detailed")
def detailed_health_check():
    """Detailed health check with all systems"""
    results = health_checker.run_all_checks()

    status_code = 200
    if results["status"] == "unhealthy":
        status_code = 503
    elif results["status"] == "degraded":
        status_code = 200  # Still serving but with warnings

    return jsonify(results), status_code


@health_bp.route("/metrics")
def metrics():
    """Prometheus-compatible metrics endpoint"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # Database metrics
        db_response_time = 0
        try:
            start_time = time.time()
            with db.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            db_response_time = (time.time() - start_time) * 1000
        except:
            db_response_time = -1

        # Redis metrics
        redis_response_time = 0
        try:
            start_time = time.time()
            redis_client = get_redis_client()
            redis_client.ping()
            redis_response_time = (time.time() - start_time) * 1000
        except:
            redis_response_time = -1

        # Generate Prometheus format metrics
        metrics_output = f"""# HELP portfolio_cpu_usage_percent CPU usage percentage
# TYPE portfolio_cpu_usage_percent gauge
portfolio_cpu_usage_percent {cpu_percent}

# HELP portfolio_memory_usage_percent Memory usage percentage
# TYPE portfolio_memory_usage_percent gauge
portfolio_memory_usage_percent {memory.percent}

# HELP portfolio_memory_available_bytes Available memory in bytes
# TYPE portfolio_memory_available_bytes gauge
portfolio_memory_available_bytes {memory.available}

# HELP portfolio_disk_usage_percent Disk usage percentage
# TYPE portfolio_disk_usage_percent gauge
portfolio_disk_usage_percent {(disk.used / disk.total) * 100}

# HELP portfolio_disk_free_bytes Free disk space in bytes
# TYPE portfolio_disk_free_bytes gauge
portfolio_disk_free_bytes {disk.free}

# HELP portfolio_database_response_time_ms Database response time in milliseconds
# TYPE portfolio_database_response_time_ms gauge
portfolio_database_response_time_ms {db_response_time}

# HELP portfolio_redis_response_time_ms Redis response time in milliseconds
# TYPE portfolio_redis_response_time_ms gauge
portfolio_redis_response_time_ms {redis_response_time}

# HELP portfolio_uptime_seconds Application uptime in seconds
# TYPE portfolio_uptime_seconds counter
portfolio_uptime_seconds {time.time() - psutil.boot_time()}
"""

        return metrics_output, 200, {"Content-Type": "text/plain; charset=utf-8"}

    except Exception as e:
        current_app.logger.error(f"Metrics endpoint error: {str(e)}")
        return (
            f"# Error generating metrics: {str(e)}",
            500,
            {"Content-Type": "text/plain"},
        )


@health_bp.route("/health/ready")
def readiness_check():
    """Kubernetes readiness probe endpoint"""
    try:
        # Check critical dependencies
        with db.engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))

        redis_client = get_redis_client()
        redis_client.ping()

        return jsonify({"status": "ready", "timestamp": datetime.utcnow().isoformat()})
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "not_ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": str(e),
                }
            ),
            503,
        )


@health_bp.route("/health/live")
def liveness_check():
    """Kubernetes liveness probe endpoint"""
    return jsonify({"status": "alive", "timestamp": datetime.utcnow().isoformat()})
