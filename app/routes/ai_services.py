"""
AI Services Routes - Flask Blueprint for AI Services Section
This module handles routes for the AI Services hub including agent interactions,
chat interfaces, pricing, and agent profiles.
"""

import logging
import os

import yaml
from flask import Blueprint, jsonify, render_template, request, session

from app.ai.controller import AIController
from app.ai.executor import AIExecutor
from app.ai.memory import AIMemory
from app.ai.planner import AIPlanner

# Initialize blueprint
ai_services_bp = Blueprint("ai_services", __name__, url_prefix="/ai")

# Initialize AI components
ai_controller = AIController()
ai_planner = AIPlanner()
ai_executor = AIExecutor()
ai_memory = AIMemory()

logger = logging.getLogger(__name__)


# Load agent registry
def load_agent_registry():
    """Load agent registry configuration"""
    try:
        registry_path = os.path.join(
            os.path.dirname(__file__), "..", "ai", "registry.yaml"
        )
        with open(registry_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load agent registry: {e}")
        return {}


@ai_services_bp.route("/")
def index():
    """AI Services home page - showcase AI capabilities"""
    registry = load_agent_registry()
    agents = registry.get("agents", {})
    featured_agents = []

    # Get featured agents for showcase
    for agent_id, agent_data in list(agents.items())[:6]:  # Show top 6 agents
        featured_agents.append(
            {
                "id": agent_id,
                "name": agent_data.get("name", agent_id.title()),
                "description": agent_data.get("description", ""),
                "avatar": f"/static/img/avatars/{agent_id}.png",
                "personality": agent_data.get("personality_traits", []),
                "capabilities": agent_data.get("capabilities", []),
            }
        )

    return render_template(
        "ai_services/index.html",
        featured_agents=featured_agents,
        total_agents=len(agents),
    )


@ai_services_bp.route("/showcase")
def showcase():
    """AI capabilities showcase and demos"""
    registry = load_agent_registry()
    models = registry.get("models", {})

    # Prepare model showcase data
    model_showcase = []
    for model_id, model_data in models.items():
        model_showcase.append(
            {
                "name": model_id,
                "description": model_data.get("description", ""),
                "capabilities": model_data.get("capabilities", []),
                "specialties": model_data.get("specialties", []),
                "status": model_data.get("status", "unknown"),
            }
        )

    return render_template("ai_services/showcase.html", models=model_showcase)


@ai_services_bp.route("/agents")
def agents():
    """Browse all available AI agents"""
    registry = load_agent_registry()
    agents = registry.get("agents", {})

    # Prepare agent data for display
    agent_list = []
    for agent_id, agent_data in agents.items():
        agent_list.append(
            {
                "id": agent_id,
                "name": agent_data.get("name", agent_id.title()),
                "description": agent_data.get("description", ""),
                "avatar": f"/static/img/avatars/{agent_id}.png",
                "personality_type": agent_data.get("personality_type", "Professional"),
                "specialties": agent_data.get("specialties", []),
                "model_ensemble": agent_data.get("model_ensemble", []),
                "availability": agent_data.get("availability", "available"),
            }
        )

    return render_template("ai_services/agents.html", agents=agent_list)


@ai_services_bp.route("/agent/<agent_id>")
def agent_profile(agent_id):
    """Individual agent profile page"""
    registry = load_agent_registry()
    agents = registry.get("agents", {})

    if agent_id not in agents:
        return render_template("404.html"), 404

    agent_data = agents[agent_id]

    # Get related agents (same personality type or similar capabilities)
    related_agents = []
    agent_personality = agent_data.get("personality_type", "")
    agent_capabilities = set(agent_data.get("capabilities", []))

    for other_id, other_data in agents.items():
        if other_id != agent_id:
            other_capabilities = set(other_data.get("capabilities", []))
            if (
                other_data.get("personality_type") == agent_personality
                or len(agent_capabilities.intersection(other_capabilities)) >= 2
            ):
                related_agents.append(
                    {
                        "id": other_id,
                        "name": other_data.get("name", other_id.title()),
                        "avatar": f"/static/img/avatars/{other_id}.png",
                    }
                )
                if len(related_agents) >= 3:  # Limit to 3 related agents
                    break

    agent_profile_data = {
        "id": agent_id,
        "name": agent_data.get("name", agent_id.title()),
        "description": agent_data.get("description", ""),
        "avatar": f"/static/img/avatars/{agent_id}.png",
        "personality_type": agent_data.get("personality_type", "Professional"),
        "personality_traits": agent_data.get("personality_traits", []),
        "capabilities": agent_data.get("capabilities", []),
        "specialties": agent_data.get("specialties", []),
        "model_ensemble": agent_data.get("model_ensemble", []),
        "response_style": agent_data.get("response_style", {}),
        "interaction_examples": agent_data.get("interaction_examples", []),
        "availability": agent_data.get("availability", "available"),
    }

    return render_template(
        "ai_services/agent_profile.html",
        agent=agent_profile_data,
        related_agents=related_agents,
    )


@ai_services_bp.route("/chat")
@ai_services_bp.route("/chat/<agent_id>")
def chat(agent_id=None):
    """Universal chat interface for AI agents"""
    registry = load_agent_registry()
    agents = registry.get("agents", {})

    # If no specific agent, show agent selection
    if not agent_id:
        available_agents = []
        for aid, adata in agents.items():
            if adata.get("availability") == "available":
                available_agents.append(
                    {
                        "id": aid,
                        "name": adata.get("name", aid.title()),
                        "avatar": f"/static/img/avatars/{aid}.png",
                        "description": adata.get("description", ""),
                    }
                )
        return render_template(
            "ai_services/chat.html", agents=available_agents, selected_agent=None
        )

    # Specific agent chat
    if agent_id not in agents:
        return render_template("404.html"), 404

    agent_data = agents[agent_id]
    selected_agent = {
        "id": agent_id,
        "name": agent_data.get("name", agent_id.title()),
        "avatar": f"/static/img/avatars/{agent_id}.png",
        "description": agent_data.get("description", ""),
        "personality_type": agent_data.get("personality_type", "Professional"),
    }

    return render_template(
        "ai_services/chat.html", agents=[], selected_agent=selected_agent
    )


@ai_services_bp.route("/pricing")
def pricing():
    """AI service pricing and subscription plans"""
    # Define pricing tiers
    pricing_tiers = [
        {
            "name": "Free Tier",
            "price": 0,
            "period": "month",
            "features": [
                "10 messages per day",
                "Access to 2 basic agents",
                "Standard response time",
                "Basic chat interface",
            ],
            "limitations": [
                "Limited conversation history",
                "No premium agents",
                "No priority support",
            ],
            "color": "basic",
        },
        {
            "name": "Pro Plan",
            "price": 19.99,
            "period": "month",
            "features": [
                "Unlimited messages",
                "Access to all 10 agents",
                "Fast response time",
                "Advanced chat features",
                "Conversation history",
                "Export conversations",
                "Email support",
            ],
            "limitations": [],
            "color": "primary",
            "popular": True,
        },
        {
            "name": "Enterprise",
            "price": 99.99,
            "period": "month",
            "features": [
                "Everything in Pro",
                "Custom agent development",
                "API access",
                "Priority support",
                "Custom integrations",
                "Analytics dashboard",
                "Dedicated account manager",
            ],
            "limitations": [],
            "color": "premium",
        },
    ]

    return render_template("ai_services/pricing.html", pricing_tiers=pricing_tiers)


# API Endpoints for AJAX/WebSocket communication


@ai_services_bp.route("/api/message", methods=["POST"])
def send_message():
    """Handle incoming chat messages"""
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        message = data.get("message")
        session_id = session.get("session_id", "anonymous")

        if not agent_id or not message:
            return jsonify({"error": "Missing agent_id or message"}), 400

        # Process message through AI controller
        response = ai_controller.process_message(
            agent_id=agent_id,
            message=message,
            session_id=session_id,
            user_context=session.get("user_context", {}),
        )

        return jsonify(
            {
                "success": True,
                "response": response.get("content", ""),
                "agent_id": agent_id,
                "timestamp": response.get("timestamp"),
                "metadata": response.get("metadata", {}),
            }
        )

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return jsonify({"error": "Failed to process message"}), 500


@ai_services_bp.route("/api/agents", methods=["GET"])
def get_agents():
    """API endpoint to get available agents"""
    try:
        registry = load_agent_registry()
        agents = registry.get("agents", {})

        agent_list = []
        for agent_id, agent_data in agents.items():
            if agent_data.get("availability") == "available":
                agent_list.append(
                    {
                        "id": agent_id,
                        "name": agent_data.get("name", agent_id.title()),
                        "description": agent_data.get("description", ""),
                        "avatar": f"/static/img/avatars/{agent_id}.png",
                        "personality_type": agent_data.get(
                            "personality_type", "Professional"
                        ),
                    }
                )

        return jsonify({"agents": agent_list})

    except Exception as e:
        logger.error(f"Error fetching agents: {e}")
        return jsonify({"error": "Failed to fetch agents"}), 500


@ai_services_bp.route("/api/session/history", methods=["GET"])
def get_session_history():
    """Get conversation history for current session"""
    try:
        session_id = session.get("session_id", "anonymous")
        agent_id = request.args.get("agent_id")

        if not agent_id:
            return jsonify({"error": "Missing agent_id"}), 400

        # Get conversation history from memory
        history = ai_memory.get_conversation_history(session_id, agent_id)

        return jsonify(
            {"history": history, "session_id": session_id, "agent_id": agent_id}
        )

    except Exception as e:
        logger.error(f"Error fetching conversation history: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500


# Error handlers specific to AI services
@ai_services_bp.errorhandler(404)
def ai_not_found(error):
    """Custom 404 handler for AI services"""
    return render_template("ai_services/404.html"), 404


@ai_services_bp.errorhandler(500)
def ai_internal_error(error):
    """Custom 500 handler for AI services"""
    return render_template("ai_services/500.html"), 500
