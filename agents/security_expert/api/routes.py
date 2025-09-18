"""
Security Expert AI REST API Routes
Production-ready HTTP endpoints for security_expert agent
"""

from flask import Blueprint, request, jsonify, session, current_app
from functools import wraps
import asyncio
import traceback
import time
import uuid
from typing import Dict, Any, Optional

from ..services.cortex.controller import SecurityexpertController
from ..monitor.usage import track_usage
from ..analytics.metrics import SecurityexpertMetrics
from ..analytics.logger import SecurityexpertAnalyticsLogger

# Initialize blueprint and services
security_expert_api = Blueprint(
    "security_expert_api", __name__, url_prefix="/api/security_expert"
)
controller = SecurityexpertController()
metrics = SecurityexpertMetrics()
analytics_logger = SecurityexpertAnalyticsLogger()

# Rate limiting configuration
RATE_LIMIT = 100  # requests per minute
rate_limit_store = {}


def rate_limit(f):
    """Rate limiting decorator"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.environ.get(
            "HTTP_X_FORWARDED_FOR", request.environ.get("REMOTE_ADDR", "unknown")
        )
        current_time = time.time()

        if client_ip not in rate_limit_store:
            rate_limit_store[client_ip] = []

        # Clean old requests
        rate_limit_store[client_ip] = [
            req_time
            for req_time in rate_limit_store[client_ip]
            if current_time - req_time < 60
        ]

        if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
            return (
                jsonify(
                    {"error": "Rate limit exceeded", "code": "RATE_LIMIT_EXCEEDED"}
                ),
                429,
            )

        rate_limit_store[client_ip].append(current_time)
        return f(*args, **kwargs)

    return decorated_function


def validate_request(required_fields=None):
    """Request validation decorator"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return (
                    jsonify(
                        {
                            "error": "Content-Type must be application/json",
                            "code": "INVALID_CONTENT_TYPE",
                        }
                    ),
                    400,
                )

            data = request.get_json()
            if not data:
                return (
                    jsonify(
                        {
                            "error": "Request body cannot be empty",
                            "code": "EMPTY_REQUEST",
                        }
                    ),
                    400,
                )

            if required_fields:
                missing_fields = [
                    field
                    for field in required_fields
                    if field not in data or not data[field]
                ]
                if missing_fields:
                    return (
                        jsonify(
                            {
                                "error": f'Missing required fields: {", ".join(missing_fields)}',
                                "code": "MISSING_FIELDS",
                                "missing_fields": missing_fields,
                            }
                        ),
                        400,
                    )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


@security_expert_api.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "agent": "security_expert",
            "version": "1.0.0",
            "timestamp": time.time(),
            "uptime": time.time() - current_app.config.get("START_TIME", time.time()),
        }
    )


@security_expert_api.route("/chat", methods=["POST"])
@rate_limit
@validate_request(["message"])
@track_usage
def chat():
    """Handle chat requests with full error handling and analytics"""
    start_time = time.time()
    request_id = str(uuid.uuid4())

    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", str(uuid.uuid4()))
        context = data.get("context", {})

        # Validate message length
        if len(message) > 2000:
            return (
                jsonify(
                    {
                        "error": "Message too long (max 2000 characters)",
                        "code": "MESSAGE_TOO_LONG",
                        "request_id": request_id,
                    }
                ),
                400,
            )

        # Log request
        analytics_logger.log_request(
            request_id=request_id,
            message=message[:100] + "..." if len(message) > 100 else message,
            session_id=session_id,
            context=context,
        )

        # Process request through controller
        response_data = controller.process_message(message, session_id, context)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Track metrics
        metrics.track_conversation(
            conversation_type="chat", duration=processing_time, satisfaction_score=None
        )

        # Prepare response
        response = {
            "success": True,
            "data": response_data,
            "metadata": {
                "request_id": request_id,
                "processing_time": processing_time,
                "session_id": session_id,
                "agent": "security_expert",
                "timestamp": time.time(),
            },
        }

        # Log successful response
        analytics_logger.log_response(
            request_id=request_id,
            response=response_data,
            processing_time=processing_time,
            success=True,
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
            processing_time=error_time,
        )

        return (
            jsonify(
                {
                    "success": False,
                    "error": "Internal server error",
                    "code": "INTERNAL_ERROR",
                    "request_id": request_id,
                    "metadata": {
                        "processing_time": error_time,
                        "timestamp": time.time(),
                    },
                }
            ),
            500,
        )


@security_expert_api.route("/analytics", methods=["GET"])
def get_analytics():
    """Get agent analytics and metrics"""
    try:
        analytics_data = {
            "agent": "security_expert",
            "metrics": metrics.get_summary(),
            "performance": {
                "total_conversations": metrics.conversation_count,
                "average_duration": metrics.average_duration,
                "success_rate": metrics.success_rate,
                "satisfaction_score": metrics.average_satisfaction,
            },
            "capabilities": [
                "security_analysis",
                "vulnerability_assessment",
                "penetration_testing",
                "compliance",
                "threat_modeling",
            ],
            "timestamp": time.time(),
        }

        return jsonify({"success": True, "data": analytics_data})

    except Exception as e:
        analytics_logger.log_error(
            request_id=str(uuid.uuid4()), error=str(e), traceback=traceback.format_exc()
        )

        return (
            jsonify(
                {
                    "success": False,
                    "error": "Failed to retrieve analytics",
                    "code": "ANALYTICS_ERROR",
                }
            ),
            500,
        )


@security_expert_api.route("/speak", methods=["POST"])
@rate_limit
@validate_request(["text"])
def speak_text():
    """Convert text to speech with secure, vigilant expert voice"""
    start_time = time.time()
    request_id = str(uuid.uuid4())

    try:
        data = request.get_json()
        text = data["text"]
        include_audio = data.get("include_audio", True)
        
        # Validate text length
        if len(text) > 5000:
            return (
                jsonify({
                    "success": False,
                    "error": "Text too long (max 5000 characters)",
                    "code": "TEXT_TOO_LONG"
                }),
                400,
            )

        # Log request start
        analytics_logger.log_request(
            request_id=request_id,
            endpoint="/speak",
            request_data={"text_length": len(text), "include_audio": include_audio}
        )

        # Generate speech with security expert personality
        speech_response = asyncio.run(
            controller.agent.speak_response(text, include_audio=include_audio)
        )

        # Calculate processing time
        processing_time = time.time() - start_time

        # Log successful response
        analytics_logger.log_response(
            request_id=request_id,
            response_data=speech_response,
            processing_time=processing_time,
            interaction_type="voice_synthesis",
            status="success"
        )

        response = {
            "success": True,
            "data": {
                "voice_enabled": speech_response.get("voice_enabled", False),
                "message": speech_response.get("message", ""),
                "audio_file": speech_response.get("audio_file"),
                "metadata": {
                    "processing_time": processing_time,
                    "request_id": request_id,
                    "timestamp": time.time(),
                    "voice_personality": "secure_vigilant"
                }
            }
        }

        return jsonify(response)

    except ValueError as e:
        processing_time = time.time() - start_time
        analytics_logger.log_error(
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
            processing_time=processing_time
        )

        return (
            jsonify({
                "success": False,
                "error": "Voice synthesis failed",
                "code": "VOICE_ERROR",
                "request_id": request_id,
                "metadata": {
                    "processing_time": processing_time,
                    "timestamp": time.time()
                }
            }),
            500,
        )

    except Exception as e:
        processing_time = time.time() - start_time
        analytics_logger.log_error(
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
            processing_time=processing_time
        )

        return (
            jsonify({
                "success": False,
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "request_id": request_id,
                "metadata": {
                    "processing_time": processing_time,
                    "timestamp": time.time()
                }
            }),
            500,
        )


@security_expert_api.route("/voice/capabilities", methods=["GET"])
def get_voice_capabilities():
    """Get voice capabilities and configuration"""
    try:
        voice_caps = asyncio.run(controller.agent.get_voice_capabilities())
        
        response = {
            "success": True,
            "data": {
                **voice_caps,
                "agent": "security_expert",
                "voice_description": "Vigilant, authoritative voice with security expertise tone",
                "personality_traits": [
                    "vigilant",
                    "authoritative", 
                    "security_focused",
                    "cautious",
                    "protective",
                    "personality_matched_voice",
                ]
            }
        }

        return jsonify(response)

    except Exception as e:
        analytics_logger.log_error(
            request_id=str(uuid.uuid4()),
            error=str(e),
            traceback=traceback.format_exc()
        )

        return (
            jsonify({
                "success": False,
                "error": "Failed to get voice capabilities",
                "code": "VOICE_CAPABILITIES_ERROR",
                "metadata": {"timestamp": time.time()}
            }),
            500,
        )


@security_expert_api.route("/chat/speak", methods=["POST"])
@rate_limit
@validate_request(["message"])
def chat_with_voice():
    """Chat with security expert voice response"""
    start_time = time.time()
    request_id = str(uuid.uuid4())

    try:
        data = request.get_json()
        user_message = data["message"]
        include_audio = data.get("include_audio", True)
        session_id = data.get("session_id", str(uuid.uuid4()))
        
        # Validate message length
        if len(user_message) > 2000:
            return (
                jsonify({
                    "success": False,
                    "error": "Message too long (max 2000 characters)",
                    "code": "MESSAGE_TOO_LONG"
                }),
                400,
            )

        # Log request start
        analytics_logger.log_request(
            request_id=request_id,
            endpoint="/chat/speak",
            request_data={
                "message_length": len(user_message), 
                "session_id": session_id,
                "include_audio": include_audio
            }
        )

        # Generate chat response with voice
        chat_response = asyncio.run(controller.agent.process_message({
            "message": user_message,
            "session_id": session_id,
            "include_voice": include_audio
        }))

        # Calculate processing time
        processing_time = time.time() - start_time

        # Log successful response
        analytics_logger.log_response(
            request_id=request_id,
            response_data=chat_response,
            processing_time=processing_time,
            interaction_type="chat_with_voice",
            status="success"
        )

        response = {
            "success": True,
            "data": {
                **chat_response,
                "metadata": {
                    "processing_time": processing_time,
                    "request_id": request_id,
                    "timestamp": time.time(),
                    "voice_personality": "secure_vigilant",
                    "session_id": session_id
                }
            }
        }

        return jsonify(response)

    except ValueError as e:
        processing_time = time.time() - start_time
        analytics_logger.log_error(
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
            processing_time=processing_time
        )

        return (
            jsonify({
                "success": False,
                "error": "Chat processing failed",
                "code": "CHAT_ERROR",
                "request_id": request_id,
                "metadata": {
                    "processing_time": processing_time,
                    "timestamp": time.time()
                }
            }),
            500,
        )

    except Exception as e:
        processing_time = time.time() - start_time
        analytics_logger.log_error(
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
            processing_time=processing_time
        )

        return (
            jsonify({
                "success": False,
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "request_id": request_id,
                "metadata": {
                    "processing_time": processing_time,
                    "timestamp": time.time()
                }
            }),
            500,
        )
