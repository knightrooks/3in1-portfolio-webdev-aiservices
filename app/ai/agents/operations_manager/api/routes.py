"""
Operations Manager AI REST API Routes
Handles HTTP requests for operations_manager agent
"""

from flask import Blueprint, request, jsonify
from ..services.cortex.controller import Operations_ManagerController
from ..monitor.usage import track_usage
from ..analytics.logger import log_interaction

operations_manager_routes = Blueprint('operations_manager_routes', __name__)
controller = Operations_ManagerController()

@operations_manager_routes.route('/chat', methods=['POST'])
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
        log_interaction('operations_manager', 'chat', message, response)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@operations_manager_routes.route('/health', methods=['GET'])
def health_check():
    """Agent health check endpoint"""
    return jsonify(controller.get_health_status())

@operations_manager_routes.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get agent capabilities"""
    return jsonify(controller.get_capabilities())

@operations_manager_routes.route('/metrics', methods=['GET'])
def get_metrics():
    """Get agent performance metrics"""
    return jsonify(controller.get_performance_metrics())