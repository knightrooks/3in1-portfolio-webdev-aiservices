"""
Research Analyst AI REST API Routes
Handles HTTP requests for research_analyst agent
"""

from flask import Blueprint, request, jsonify
from ..services.cortex.controller import Research_AnalystController
from ..monitor.usage import track_usage
from ..analytics.logger import log_interaction

research_analyst_routes = Blueprint('research_analyst_routes', __name__)
controller = Research_AnalystController()

@research_analyst_routes.route('/chat', methods=['POST'])
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
        log_interaction('research_analyst', 'chat', message, response)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@research_analyst_routes.route('/health', methods=['GET'])
def health_check():
    """Agent health check endpoint"""
    return jsonify(controller.get_health_status())

@research_analyst_routes.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get agent capabilities"""
    return jsonify(controller.get_capabilities())

@research_analyst_routes.route('/metrics', methods=['GET'])
def get_metrics():
    """Get agent performance metrics"""
    return jsonify(controller.get_performance_metrics())