"""
Content Creator AI REST API Routes
Handles HTTP requests for content_creator agent
"""

from flask import Blueprint, request, jsonify
from ..services.cortex.controller import Content_CreatorController
from ..monitor.usage import track_usage
from ..analytics.logger import log_interaction

content_creator_routes = Blueprint('content_creator_routes', __name__)
controller = Content_CreatorController()

@content_creator_routes.route('/chat', methods=['POST'])
@track_usage
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Process request through controller
        response = await controller.process_message(message, session_id)
        
        # Log interaction
        log_interaction('content_creator', 'chat', message, response)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_creator_routes.route('/health', methods=['GET'])
def health_check():
    """Agent health check endpoint"""
    return jsonify(controller.get_health_status())

@content_creator_routes.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get agent capabilities"""
    return jsonify(controller.get_capabilities())

@content_creator_routes.route('/metrics', methods=['GET'])
def get_metrics():
    """Get agent performance metrics"""
    return jsonify(controller.get_performance_metrics())