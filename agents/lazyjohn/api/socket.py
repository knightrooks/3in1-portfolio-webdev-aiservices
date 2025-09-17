"""
Lazyjohn AI WebSocket Handler
Production-ready real-time communication system
"""

import json
import asyncio
import uuid
import time
from typing import Dict, Any, Set, Optional
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask import request

from ..services.cortex.controller import LazyjohnController
from ..analytics.metrics import LazyjohnMetrics
from ..analytics.logger import LazyjohnAnalyticsLogger
from ..monitor.usage import track_websocket_usage

# Initialize services
controller = LazyjohnController()
metrics = LazyjohnMetrics()
analytics_logger = LazyjohnAnalyticsLogger()

# Connection management
active_sessions: Dict[str, Dict[str, Any]] = {}
session_rooms: Dict[str, str] = {}
connection_limits = {"max_connections": 100, "current": 0}


class LazyjohnSocketHandler:
    """Production WebSocket handler for Lazyjohn agent"""

    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all WebSocket event handlers"""

        @self.socketio.on("connect", namespace="/lazyjohn")
        def handle_connect():
            """Handle client connection with validation and rate limiting"""
            try:
                # Check connection limits
                if connection_limits["current"] >= connection_limits["max_connections"]:
                    emit(
                        "error",
                        {
                            "message": "Maximum connections reached",
                            "code": "CONNECTION_LIMIT",
                        },
                    )
                    disconnect()
                    return False

                # Generate session
                session_id = str(uuid.uuid4())
                client_id = request.sid

                # Initialize session
                active_sessions[client_id] = {
                    "session_id": session_id,
                    "connected_at": time.time(),
                    "last_activity": time.time(),
                    "message_count": 0,
                    "room": f"lazyjohn_{session_id}",
                    "authenticated": False,
                }

                # Join room
                room = active_sessions[client_id]["room"]
                join_room(room)
                session_rooms[session_id] = room

                # Update connection count
                connection_limits["current"] += 1

                # Log connection
                analytics_logger.log_websocket_event(
                    event_type="connect",
                    session_id=session_id,
                    client_id=client_id,
                    metadata={"room": room},
                )

                # Send welcome message
                emit(
                    "connected",
                    {
                        "status": "connected",
                        "session_id": session_id,
                        "agent": "lazyjohn",
                        "capabilities": [
                            "casual_chat",
                            "humor",
                            "relaxed_conversation",
                            "entertainment",
                        ],
                        "timestamp": time.time(),
                    },
                )

                return True

            except Exception as e:
                analytics_logger.log_error(
                    request_id=str(uuid.uuid4()),
                    error=f"Connection error: {str(e)}",
                    traceback=str(e),
                )
                emit(
                    "error",
                    {"message": "Connection failed", "code": "CONNECTION_ERROR"},
                )
                return False

        @self.socketio.on("disconnect", namespace="/lazyjohn")
        def handle_disconnect():
            """Handle client disconnection"""
            try:
                client_id = request.sid

                if client_id in active_sessions:
                    session_data = active_sessions[client_id]
                    session_id = session_data["session_id"]
                    room = session_data["room"]

                    # Calculate session duration
                    duration = time.time() - session_data["connected_at"]

                    # Leave room
                    leave_room(room)

                    # Clean up
                    del active_sessions[client_id]
                    if session_id in session_rooms:
                        del session_rooms[session_id]

                    # Update connection count
                    connection_limits["current"] = max(
                        0, connection_limits["current"] - 1
                    )

                    # Log disconnection
                    analytics_logger.log_websocket_event(
                        event_type="disconnect",
                        session_id=session_id,
                        client_id=client_id,
                        metadata={
                            "duration": duration,
                            "message_count": session_data["message_count"],
                        },
                    )

            except Exception as e:
                analytics_logger.log_error(
                    request_id=str(uuid.uuid4()),
                    error=f"Disconnection error: {str(e)}",
                    traceback=str(e),
                )

        @self.socketio.on("message", namespace="/lazyjohn")
        @track_websocket_usage
        def handle_message(data):
            """Handle incoming messages with full validation and processing"""
            start_time = time.time()
            client_id = request.sid
            request_id = str(uuid.uuid4())

            try:
                # Validate session
                if client_id not in active_sessions:
                    emit(
                        "error",
                        {
                            "message": "Invalid session",
                            "code": "INVALID_SESSION",
                            "request_id": request_id,
                        },
                    )
                    return

                session_data = active_sessions[client_id]
                session_id = session_data["session_id"]

                # Update activity
                session_data["last_activity"] = time.time()
                session_data["message_count"] += 1

                # Rate limiting check
                if session_data["message_count"] > 50:  # per session
                    emit(
                        "error",
                        {
                            "message": "Message limit exceeded for session",
                            "code": "MESSAGE_LIMIT",
                            "request_id": request_id,
                        },
                    )
                    return

                # Validate message data
                if not isinstance(data, dict) or "message" not in data:
                    emit(
                        "error",
                        {
                            "message": "Invalid message format",
                            "code": "INVALID_FORMAT",
                            "request_id": request_id,
                        },
                    )
                    return

                message = data.get("message", "").strip()
                if not message or len(message) > 2000:
                    emit(
                        "error",
                        {
                            "message": "Invalid message length",
                            "code": "INVALID_LENGTH",
                            "request_id": request_id,
                        },
                    )
                    return

                # Log incoming message
                analytics_logger.log_websocket_message(
                    session_id=session_id,
                    message_type="incoming",
                    message=message[:100] + "..." if len(message) > 100 else message,
                    request_id=request_id,
                )

                # Process message
                context = data.get("context", {})
                response_data = controller.process_message(message, session_id, context)

                # Calculate processing time
                processing_time = time.time() - start_time

                # Track metrics
                metrics.track_conversation(
                    conversation_type="websocket_chat",
                    duration=processing_time,
                    satisfaction_score=None,
                )

                # Send response
                response = {
                    "type": "response",
                    "data": response_data,
                    "metadata": {
                        "request_id": request_id,
                        "processing_time": processing_time,
                        "session_id": session_id,
                        "agent": "lazyjohn",
                        "timestamp": time.time(),
                    },
                }

                emit("response", response)

                # Log outgoing response
                analytics_logger.log_websocket_message(
                    session_id=session_id,
                    message_type="outgoing",
                    message=(
                        str(response_data)[:100] + "..."
                        if len(str(response_data)) > 100
                        else str(response_data)
                    ),
                    request_id=request_id,
                    processing_time=processing_time,
                )

            except Exception as e:
                processing_time = time.time() - start_time

                analytics_logger.log_error(
                    request_id=request_id,
                    error=f"Message processing error: {str(e)}",
                    traceback=str(e),
                    processing_time=processing_time,
                )

                emit(
                    "error",
                    {
                        "message": "Failed to process message",
                        "code": "PROCESSING_ERROR",
                        "request_id": request_id,
                        "metadata": {
                            "processing_time": processing_time,
                            "timestamp": time.time(),
                        },
                    },
                )

        @self.socketio.on("ping", namespace="/lazyjohn")
        def handle_ping():
            """Handle ping for connection health"""
            try:
                client_id = request.sid
                if client_id in active_sessions:
                    active_sessions[client_id]["last_activity"] = time.time()
                    emit("pong", {"timestamp": time.time()})
                else:
                    emit(
                        "error",
                        {"message": "Invalid session", "code": "INVALID_SESSION"},
                    )
            except Exception as e:
                emit("error", {"message": "Ping failed", "code": "PING_ERROR"})


def get_connection_stats() -> Dict[str, Any]:
    """Get current WebSocket connection statistics"""
    return {
        "active_connections": connection_limits["current"],
        "max_connections": connection_limits["max_connections"],
        "active_sessions": len(active_sessions),
        "session_details": {
            session_id: {
                "connected_duration": time.time() - data["connected_at"],
                "message_count": data["message_count"],
                "last_activity": time.time() - data["last_activity"],
            }
            for session_id, data in active_sessions.items()
        },
    }
