"""
Cybersecurity Expert AI REST API Routes
Handles HTTP requests for security_expert agent
"""

from flask import Blueprint, request, jsonify
from ..services.cortex.controller import Security_ExpertController
from ..monitor.usage import track_usage
from ..analytics.logger import log_interaction

security_expert_routes = Blueprint('security_expert_routes', __name__)
controller = Security_ExpertController()

@security_expert_routes.route('/chat', methods=['POST'])
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
        log_interaction('security_expert', 'chat', message, response)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@security_expert_routes.route('/health', methods=['GET'])
def health_check():
    """Agent health check endpoint"""
    return jsonify(controller.get_health_status())

@security_expert_routes.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get agent capabilities"""
    return jsonify(controller.get_capabilities())

@security_expert_routes.route('/metrics', methods=['GET'])
def get_metrics():
    """Get agent performance metrics"""
    return jsonify(controller.get_performance_metrics())