"""
Product Manager AI REST API Routes
Handles HTTP requests for product_manager agent
"""

from flask import Blueprint, request, jsonify
from ..services.cortex.controller import Product_ManagerController
from ..monitor.usage import track_usage
from ..analytics.logger import log_interaction

product_manager_routes = Blueprint('product_manager_routes', __name__)
controller = Product_ManagerController()

@product_manager_routes.route('/chat', methods=['POST'])
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
        log_interaction('product_manager', 'chat', message, response)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_manager_routes.route('/health', methods=['GET'])
def health_check():
    """Agent health check endpoint"""
    return jsonify(controller.get_health_status())

@product_manager_routes.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get agent capabilities"""
    return jsonify(controller.get_capabilities())

@product_manager_routes.route('/metrics', methods=['GET'])
def get_metrics():
    """Get agent performance metrics"""
    return jsonify(controller.get_performance_metrics())