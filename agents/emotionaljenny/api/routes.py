"""
Emotionaljenny AI REST API Routes
Production-ready HTTP endpoints for emotionaljenny agent
"""

from flask import Blueprint, request, jsonify, session, current_app
from functools import wraps
import asyncio
import traceback
import time
import uuid
from typing import Dict, Any, Optional

from ..services.cortex.controller import EmotionaljennyController
from ..monitor.usage import track_usage
from ..analytics.metrics import EmotionaljennyMetrics
from ..analytics.logger import EmotionaljennyAnalyticsLogger

# Initialize blueprint and services
emotionaljenny_api = Blueprint(
    "emotionaljenny_api", __name__, url_prefix="/api/emotionaljenny"
)
controller = EmotionaljennyController()
metrics = EmotionaljennyMetrics()
analytics_logger = EmotionaljennyAnalyticsLogger()

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


@emotionaljenny_api.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "agent": "emotionaljenny",
            "version": "1.0.0",
            "timestamp": time.time(),
            "uptime": time.time() - current_app.config.get("START_TIME", time.time()),
        }
    )


@emotionaljenny_api.route("/chat", methods=["POST"])
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
                "agent": "emotionaljenny",
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


@emotionaljenny_api.route("/speak", methods=["POST"])
@rate_limit
@validate_request(["text"])
@track_usage
def text_to_speech():
    """Convert text to speech with personality-matched voice"""
    start_time = time.time()
    request_id = str(uuid.uuid4())

    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        include_audio = data.get("include_audio", True)
        audio_format = data.get("format", "audio/mp3")

        # Validate text length
        if len(text) > 1000:
            return (
                jsonify({
                    "error": "Text too long. Maximum 1000 characters.",
                    "code": "TEXT_TOO_LONG"
                }),
                400,
            )

        if not text:
            return (
                jsonify({
                    "error": "Text cannot be empty",
                    "code": "EMPTY_TEXT"
                }),
                400,
            )

        # Generate speech using agent's personality
        speech_response = asyncio.run(
            controller.agent.speak_response(text, include_audio=include_audio)
        )

        processing_time = time.time() - start_time

        # Log analytics
        analytics_logger.log_interaction(
            request_id=request_id,
            session_id=data.get("session_id", "anonymous"),
            interaction_type="voice_synthesis",
            success=True,
            processing_time=processing_time,
            metadata={
                "text_length": len(text),
                "audio_format": audio_format,
                "voice_enabled": speech_response.get("voice_enabled", False),
                "audio_size": speech_response.get("audio_size", 0)
            }
        )

        response = {
            "success": True,
            "request_id": request_id,
            "data": speech_response,
            "metadata": {
                "processing_time": processing_time,
                "timestamp": time.time(),
                "agent": "emotionaljenny",
                "voice_personality": "warm_empathetic"
            }
        }

        return jsonify(response)

    except Exception as e:
        error_time = time.time() - start_time
        analytics_logger.log_error(
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
            processing_time=error_time,
        )

        return (
            jsonify({
                "success": False,
                "error": "Voice synthesis failed",
                "code": "VOICE_ERROR",
                "request_id": request_id,
                "metadata": {
                    "processing_time": error_time,
                    "timestamp": time.time(),
                }
            }),
            500,
        )


@emotionaljenny_api.route("/voice/capabilities", methods=["GET"])
def get_voice_capabilities():
    """Get voice capabilities and configuration"""
    try:
        voice_caps = asyncio.run(controller.agent.get_voice_capabilities())
        
        return jsonify({
            "success": True,
            "data": {
                **voice_caps,
                "agent_personality": "warm_empathetic",
                "voice_description": "Warm, soothing voice with empathetic tone",
                "supported_features": [
                    "text_to_speech",
                    "personality_matched_voice",
                    "emotional_inflection",
                    "multiple_formats"
                ]
            }
        })

    except Exception as e:
        return (
            jsonify({
                "success": False,
                "error": "Failed to get voice capabilities",
                "code": "VOICE_CAPABILITIES_ERROR",
                "details": str(e)
            }),
            500,
        )


@emotionaljenny_api.route("/chat/speak", methods=["POST"])
@rate_limit
@validate_request(["message"])
@track_usage
def chat_with_voice():
    """Chat with voice response included"""
    start_time = time.time()
    request_id = str(uuid.uuid4())

    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", str(uuid.uuid4()))
        context = data.get("context", {})
        include_audio = data.get("include_audio", True)

        # Validate message length
        if len(message) > 2000:
            return (
                jsonify({
                    "error": "Message too long. Maximum 2000 characters.",
                    "code": "MESSAGE_TOO_LONG"
                }),
                400,
            )

        # Process chat request
        chat_request = {
            "message": message,
            "session_id": session_id,
            "context": context,
            "request_id": request_id,
            "include_voice": include_audio
        }

        # Get response from controller
        response_data = asyncio.run(controller.process_request(chat_request))
        
        # Add voice to response if requested
        if include_audio and response_data.get("response"):
            voice_response = asyncio.run(
                controller.agent.speak_response(
                    response_data["response"], 
                    include_audio=True
                )
            )
            response_data.update(voice_response)

        processing_time = time.time() - start_time

        # Log analytics
        analytics_logger.log_interaction(
            request_id=request_id,
            session_id=session_id,
            interaction_type="chat_with_voice",
            success=True,
            processing_time=processing_time,
            metadata={
                "message_length": len(message),
                "response_length": len(response_data.get("response", "")),
                "voice_included": include_audio,
                "audio_generated": "audio" in response_data
            }
        )

        response = {
            "success": True,
            "request_id": request_id,
            "data": response_data,
            "metadata": {
                "processing_time": processing_time,
                "timestamp": time.time(),
                "agent": "emotionaljenny",
                "interaction_type": "chat_with_voice"
            }
        }

        return jsonify(response)

    except Exception as e:
        error_time = time.time() - start_time
        analytics_logger.log_error(
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
            processing_time=error_time,
        )

        return (
            jsonify({
                "success": False,
                "error": "Chat with voice failed",
                "code": "CHAT_VOICE_ERROR",
                "request_id": request_id,
                "metadata": {
                    "processing_time": error_time,
                    "timestamp": time.time(),
                }
            }),
            500,
        )


@emotionaljenny_api.route("/analytics", methods=["GET"])
def get_analytics():
    """Get agent analytics and metrics"""
    try:
        analytics_data = {
            "agent": "emotionaljenny",
            "metrics": metrics.get_summary(),
            "performance": {
                "total_conversations": metrics.conversation_count,
                "average_duration": metrics.average_duration,
                "success_rate": metrics.success_rate,
                "satisfaction_score": metrics.average_satisfaction,
            },
            "capabilities": [
                "emotional_intelligence",
                "empathy",
                "mood_support",
                "personal_guidance",
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
