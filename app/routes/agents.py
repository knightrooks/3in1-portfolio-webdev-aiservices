"""
AI Agents Routing System
Comprehensive routing for all 16 AI agents with API endpoints
"""

import importlib
import json
import time

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

# Create agents blueprint (no template folder - uses individual agent templates)
agents_bp = Blueprint("agents", __name__)

# Define all 16 agents with their metadata
ALL_AGENTS = {
    # Professional Agents (10)
    "strategist": {
        "name": "Business Strategist",
        "description": "Strategic planning, business analysis, market research",
        "category": "professional",
        "capabilities": [
            "strategic_planning",
            "business_analysis",
            "market_research",
            "competitive_analysis",
        ],
        "icon": "📊",
        "color": "#2563eb",
    },
    "developer": {
        "name": "Software Developer",
        "description": "Code development, architecture design, debugging, testing",
        "category": "professional",
        "capabilities": [
            "code_development",
            "architecture_design",
            "debugging",
            "testing",
        ],
        "icon": "💻",
        "color": "#059669",
    },
    "security_expert": {
        "name": "Security Expert",
        "description": "Security analysis, vulnerability assessment, penetration testing",
        "category": "professional",
        "capabilities": [
            "security_analysis",
            "vulnerability_assessment",
            "penetration_testing",
            "compliance",
        ],
        "icon": "🔐",
        "color": "#dc2626",
    },
    "content_creator": {
        "name": "Content Creator",
        "description": "Content strategy, copywriting, SEO optimization, social media",
        "category": "professional",
        "capabilities": [
            "content_strategy",
            "copywriting",
            "seo_optimization",
            "social_media",
        ],
        "icon": "✍️",
        "color": "#7c3aed",
    },
    "research_analyst": {
        "name": "Research Analyst",
        "description": "Market research, data analysis, trend analysis, reporting",
        "category": "professional",
        "capabilities": [
            "market_research",
            "data_analysis",
            "trend_analysis",
            "reporting",
        ],
        "icon": "🔍",
        "color": "#ea580c",
    },
    "data_scientist": {
        "name": "Data Scientist",
        "description": "Data analysis, machine learning, statistical modeling, predictive analytics",
        "category": "professional",
        "capabilities": [
            "data_analysis",
            "machine_learning",
            "statistical_modeling",
            "predictive_analytics",
        ],
        "icon": "📈",
        "color": "#0891b2",
    },
    "customer_success": {
        "name": "Customer Success",
        "description": "Customer support, relationship management, retention strategies",
        "category": "professional",
        "capabilities": [
            "customer_support",
            "relationship_management",
            "retention_strategies",
            "feedback_analysis",
        ],
        "icon": "🤝",
        "color": "#16a34a",
    },
    "product_manager": {
        "name": "Product Manager",
        "description": "Product strategy, roadmap planning, feature prioritization, user research",
        "category": "professional",
        "capabilities": [
            "product_strategy",
            "roadmap_planning",
            "feature_prioritization",
            "user_research",
        ],
        "icon": "📋",
        "color": "#9333ea",
    },
    "marketing_specialist": {
        "name": "Marketing Specialist",
        "description": "Marketing strategy, campaign management, brand development, digital marketing",
        "category": "professional",
        "capabilities": [
            "marketing_strategy",
            "campaign_management",
            "brand_development",
            "digital_marketing",
        ],
        "icon": "📢",
        "color": "#e11d48",
    },
    "operations_manager": {
        "name": "Operations Manager",
        "description": "Process optimization, resource management, quality assurance, workflow design",
        "category": "professional",
        "capabilities": [
            "process_optimization",
            "resource_management",
            "quality_assurance",
            "workflow_design",
        ],
        "icon": "⚙️",
        "color": "#6b7280",
    },
    # Entertainment Agents (6)
    "girlfriend": {
        "name": "Virtual Girlfriend",
        "description": "Emotional support, relationship advice, casual conversation, companionship",
        "category": "entertainment",
        "capabilities": [
            "emotional_support",
            "relationship_advice",
            "casual_conversation",
            "companionship",
        ],
        "icon": "💕",
        "color": "#f472b6",
    },
    "lazyjohn": {
        "name": "Lazy John",
        "description": "Casual chat, humor, relaxed conversation, entertainment",
        "category": "entertainment",
        "capabilities": [
            "casual_chat",
            "humor",
            "relaxed_conversation",
            "entertainment",
        ],
        "icon": "😴",
        "color": "#fbbf24",
    },
    "gossipqueen": {
        "name": "Gossip Queen",
        "description": "Social updates, trending topics, celebrity news, entertainment gossip",
        "category": "entertainment",
        "capabilities": [
            "social_updates",
            "trending_topics",
            "celebrity_news",
            "entertainment_gossip",
        ],
        "icon": "👑",
        "color": "#f59e0b",
    },
    "emotionaljenny": {
        "name": "Emotional Jenny",
        "description": "Emotional intelligence, empathy, mood support, personal guidance",
        "category": "entertainment",
        "capabilities": [
            "emotional_intelligence",
            "empathy",
            "mood_support",
            "personal_guidance",
        ],
        "icon": "😊",
        "color": "#06b6d4",
    },
    "strictwife": {
        "name": "Strict Wife",
        "description": "Discipline, organization, accountability, structured guidance",
        "category": "entertainment",
        "capabilities": [
            "discipline",
            "organization",
            "accountability",
            "structured_guidance",
        ],
        "icon": "👩‍💼",
        "color": "#7c2d12",
    },
    "coderbot": {
        "name": "Coder Bot",
        "description": "Coding assistance, programming tutorials, code debugging, technical support",
        "category": "entertainment",
        "capabilities": [
            "coding_assistance",
            "programming_tutorials",
            "code_debugging",
            "technical_support",
        ],
        "icon": "🤖",
        "color": "#374151",
    },
}


@agents_bp.route("/")
def agents_dashboard():
    """Main agents dashboard showing all 16 agents"""
    professional_agents = {
        k: v for k, v in ALL_AGENTS.items() if v["category"] == "professional"
    }
    entertainment_agents = {
        k: v for k, v in ALL_AGENTS.items() if v["category"] == "entertainment"
    }

    return render_template(
        "agents/dashboard.html",
        professional_agents=professional_agents,
        entertainment_agents=entertainment_agents,
        total_agents=len(ALL_AGENTS),
    )


@agents_bp.route("/api")
def api_overview():
    """API overview showing all available agent endpoints"""
    agent_apis = {}

    for agent_id, agent_info in ALL_AGENTS.items():
        agent_apis[agent_id] = {
            "info": agent_info,
            "endpoints": {
                "chat": f"/agents/api/{agent_id}/chat",
                "health": f"/agents/api/{agent_id}/health",
                "analytics": f"/agents/api/{agent_id}/analytics",
                "websocket": f"/agents/ws/{agent_id}",
            },
        }

    return jsonify(
        {
            "success": True,
            "data": {
                "total_agents": len(ALL_AGENTS),
                "professional_count": len(
                    [a for a in ALL_AGENTS.values() if a["category"] == "professional"]
                ),
                "entertainment_count": len(
                    [a for a in ALL_AGENTS.values() if a["category"] == "entertainment"]
                ),
                "agents": agent_apis,
            },
        }
    )


@agents_bp.route("/<agent_id>")
def agent_detail(agent_id):
    """Agent detail page - redirect to individual agent interface"""
    if agent_id not in ALL_AGENTS:
        return render_template("errors/404.html"), 404

    # Redirect to the agent's individual template/interface
    # For now, redirect to chat interface - can be changed to individual agent routes later
    return redirect(url_for("agents.agent_chat", agent_id=agent_id))


@agents_bp.route("/<agent_id>/chat")
def agent_chat(agent_id):
    """Agent chat interface - serve individual agent template"""
    if agent_id not in ALL_AGENTS:
        return render_template("errors/404.html"), 404

    agent = ALL_AGENTS[agent_id]

    # For now, create a simple chat interface.
    # TODO: Later this should redirect to individual agent blueprints
    # or serve the individual agent templates directly

    # Try to serve individual agent template if it exists
    template_path = f"../../agents/{agent_id}/templates/{agent_id}.html"
    try:
        # This is a workaround - ideally each agent should have its own blueprint
        return render_template(template_path, agent=agent)
    except:
        # Fallback to a simple chat interface
        return (
            f"""
        <!DOCTYPE html>
        <html>
        <head><title>{agent['name']} Chat</title></head>
        <body>
            <h1>{agent['name']}</h1>
            <p>{agent['description']}</p>
            <p>Individual agent template not found. Please implement agent blueprint.</p>
            <a href="/agents">Back to Dashboard</a>
        </body>
        </html>
        """,
            200,
        )


# Dynamic API routing to individual agents
@agents_bp.route(
    "/api/<agent_id>/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"]
)
def proxy_to_agent_api(agent_id, endpoint):
    """Proxy requests to individual agent APIs"""
    if agent_id not in ALL_AGENTS:
        return jsonify({"error": "Agent not found", "code": "AGENT_NOT_FOUND"}), 404

    try:
        # Import the specific agent's API blueprint
        agent_api_module = importlib.import_module(f"agents.{agent_id}.api.routes")
        agent_blueprint = getattr(agent_api_module, f"{agent_id}_api")

        # Forward the request to the agent's API
        # This is a simplified proxy - in production, you might want more sophisticated routing
        return redirect(url_for(f"{agent_blueprint.name}.{endpoint}", **request.args))

    except (ImportError, AttributeError) as e:
        return (
            jsonify(
                {
                    "error": "Agent API not available",
                    "code": "API_NOT_AVAILABLE",
                    "details": str(e),
                }
            ),
            503,
        )


@agents_bp.route("/health")
def agents_health():
    """Health check for all agents"""
    health_status = {}

    for agent_id in ALL_AGENTS.keys():
        try:
            # Try to import agent's API to check if it's available
            importlib.import_module(f"agents.{agent_id}.api")
            health_status[agent_id] = {
                "status": "healthy",
                "api_available": True,
                "last_check": time.time(),
            }
        except ImportError:
            health_status[agent_id] = {
                "status": "unavailable",
                "api_available": False,
                "last_check": time.time(),
                "error": "API module not found",
            }

    # Overall system health
    healthy_count = sum(
        1 for status in health_status.values() if status["status"] == "healthy"
    )
    total_count = len(ALL_AGENTS)

    return jsonify(
        {
            "success": True,
            "data": {
                "overall_status": (
                    "healthy" if healthy_count == total_count else "partial"
                ),
                "healthy_agents": healthy_count,
                "total_agents": total_count,
                "health_percentage": (healthy_count / total_count) * 100,
                "agents": health_status,
                "timestamp": time.time(),
            },
        }
    )


@agents_bp.route("/analytics")
def agents_analytics():
    """Combined analytics for all agents"""
    analytics_data = {
        "total_agents": len(ALL_AGENTS),
        "categories": {
            "professional": len(
                [a for a in ALL_AGENTS.values() if a["category"] == "professional"]
            ),
            "entertainment": len(
                [a for a in ALL_AGENTS.values() if a["category"] == "entertainment"]
            ),
        },
        "capabilities": {},
        "agents": {},
    }

    # Aggregate capabilities
    all_capabilities = []
    for agent_info in ALL_AGENTS.values():
        all_capabilities.extend(agent_info["capabilities"])

    from collections import Counter

    capability_counts = Counter(all_capabilities)
    analytics_data["capabilities"] = dict(capability_counts)

    # Get individual agent analytics
    for agent_id in ALL_AGENTS.keys():
        try:
            agent_api = importlib.import_module(f"agents.{agent_id}.api")
            if hasattr(agent_api, "get_api_info"):
                analytics_data["agents"][agent_id] = agent_api.get_api_info()
        except ImportError:
            analytics_data["agents"][agent_id] = {"status": "unavailable"}

    return jsonify({"success": True, "data": analytics_data, "timestamp": time.time()})


# WebSocket namespace registration will be handled by the main app
def register_agent_websockets(socketio):
    """Register WebSocket handlers for all agents"""
    for agent_id in ALL_AGENTS.keys():
        try:
            agent_socket_module = importlib.import_module(
                f"agents.{agent_id}.api.socket"
            )
            if hasattr(
                agent_socket_module, f'{agent_id.replace("_", "").title()}SocketHandler'
            ):
                handler_class = getattr(
                    agent_socket_module,
                    f'{agent_id.replace("_", "").title()}SocketHandler',
                )
                handler_class(socketio)
        except ImportError:
            pass  # Agent doesn't have WebSocket support yet
