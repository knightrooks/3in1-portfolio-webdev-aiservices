"""
AI Models Routing System
Manages AI model integration and real-time agent connections
"""

import json
import os
import subprocess
import time
from pathlib import Path

import psutil
from flask import Blueprint, jsonify, render_template, request, send_file

# Create models blueprint
models_bp = Blueprint("models", __name__, template_folder="../templates/models")

# Models directory path
MODELS_DIR = Path("/workspaces/3in1-portfolio-webdev-aiservices/models")

# Supported model types and their configurations
MODEL_TYPES = {
    "codellama": {
        "name": "Code Llama",
        "description": "Advanced code generation and analysis model",
        "category": "code",
        "use_cases": ["code_generation", "code_review", "debugging", "documentation"],
        "agents": ["developer", "coderbot"],
        "icon": "🦙",
        "color": "#2563eb",
    },
    "deepseek-coder": {
        "name": "DeepSeek Coder",
        "description": "Specialized coding assistant model",
        "category": "code",
        "use_cases": [
            "code_completion",
            "bug_fixing",
            "refactoring",
            "code_explanation",
        ],
        "agents": ["developer", "security_expert"],
        "icon": "🔍",
        "color": "#059669",
    },
    "gemma2": {
        "name": "Gemma 2",
        "description": "General purpose language model for conversation",
        "category": "general",
        "use_cases": ["conversation", "content_creation", "analysis", "summarization"],
        "agents": ["content_creator", "marketing_specialist", "girlfriend", "lazyjohn"],
        "icon": "💎",
        "color": "#7c3aed",
    },
    "llama3.2": {
        "name": "Llama 3.2",
        "description": "Advanced reasoning and conversation model",
        "category": "general",
        "use_cases": ["reasoning", "problem_solving", "creative_writing", "analysis"],
        "agents": ["strategist", "research_analyst", "emotionaljenny"],
        "icon": "🦙",
        "color": "#ea580c",
    },
    "mathstral": {
        "name": "Mathstral",
        "description": "Mathematical reasoning and calculation model",
        "category": "math",
        "use_cases": [
            "mathematical_analysis",
            "calculations",
            "data_modeling",
            "statistics",
        ],
        "agents": ["data_scientist", "research_analyst"],
        "icon": "🔢",
        "color": "#0891b2",
    },
    "mistral": {
        "name": "Mistral",
        "description": "Efficient and powerful language model",
        "category": "general",
        "use_cases": [
            "conversation",
            "text_generation",
            "summarization",
            "translation",
        ],
        "agents": ["content_creator", "customer_success", "gossipqueen"],
        "icon": "🌪️",
        "color": "#16a34a",
    },
    "nomic-embed-text": {
        "name": "Nomic Embed Text",
        "description": "Text embedding model for semantic search",
        "category": "embedding",
        "use_cases": [
            "semantic_search",
            "text_similarity",
            "document_analysis",
            "clustering",
        ],
        "agents": ["research_analyst", "content_creator", "data_scientist"],
        "icon": "🔍",
        "color": "#9333ea",
    },
    "phi3": {
        "name": "Phi-3",
        "description": "Compact and efficient reasoning model",
        "category": "reasoning",
        "use_cases": [
            "logical_reasoning",
            "problem_solving",
            "decision_making",
            "analysis",
        ],
        "agents": ["strategist", "product_manager", "strictwife"],
        "icon": "φ",
        "color": "#e11d48",
    },
    "qwen2.5": {
        "name": "Qwen 2.5",
        "description": "Multilingual conversation and analysis model",
        "category": "multilingual",
        "use_cases": [
            "multilingual_conversation",
            "translation",
            "cultural_analysis",
            "global_support",
        ],
        "agents": ["customer_success", "marketing_specialist"],
        "icon": "🌐",
        "color": "#6b7280",
    },
    "qwen2.5-coder": {
        "name": "Qwen 2.5 Coder",
        "description": "Coding-focused version of Qwen model",
        "category": "code",
        "use_cases": [
            "code_generation",
            "code_review",
            "algorithm_design",
            "optimization",
        ],
        "agents": ["developer", "security_expert", "coderbot"],
        "icon": "👨‍💻",
        "color": "#f472b6",
    },
    "snowflake-arctic-embed": {
        "name": "Snowflake Arctic Embed",
        "description": "Advanced embedding model for enterprise use",
        "category": "embedding",
        "use_cases": [
            "enterprise_search",
            "document_retrieval",
            "knowledge_base",
            "analytics",
        ],
        "agents": ["data_scientist", "operations_manager", "research_analyst"],
        "icon": "❄️",
        "color": "#fbbf24",
    },
    "yi": {
        "name": "Yi",
        "description": "High-performance bilingual language model",
        "category": "multilingual",
        "use_cases": [
            "bilingual_support",
            "cross_cultural_communication",
            "translation",
            "localization",
        ],
        "agents": ["customer_success", "content_creator"],
        "icon": "易",
        "color": "#f59e0b",
    },
}


def get_model_status(model_name):
    """Check if a model is currently running via Ollama or other service"""
    try:
        # Check if Ollama is running and has the model
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and model_name in result.stdout:
            return {"status": "available", "service": "ollama"}
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Check if model files exist locally
    model_dir = MODELS_DIR / model_name
    if model_dir.exists():
        return {"status": "local", "path": str(model_dir)}

    return {"status": "not_available"}


def get_system_resources():
    """Get current system resource usage"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "gpu_available": False,  # Would need GPU-specific library to check
    }


@models_bp.route("/")
def models_dashboard():
    """Main models dashboard"""
    model_statuses = {}

    for model_id, model_info in MODEL_TYPES.items():
        status = get_model_status(model_id)
        model_statuses[model_id] = {
            **model_info,
            **status,
            "connected_agents": len(model_info["agents"]),
        }

    # Categorize models
    categories = {}
    for model_id, model_data in model_statuses.items():
        category = model_data["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((model_id, model_data))

    system_resources = get_system_resources()

    return render_template(
        "models/dashboard.html",
        models=model_statuses,
        categories=categories,
        total_models=len(MODEL_TYPES),
        system_resources=system_resources,
    )


@models_bp.route("/api")
def models_api_overview():
    """API overview for model management"""
    model_apis = {}

    for model_id, model_info in MODEL_TYPES.items():
        status = get_model_status(model_id)
        model_apis[model_id] = {
            "info": model_info,
            "status": status,
            "endpoints": {
                "status": f"/models/api/{model_id}/status",
                "start": f"/models/api/{model_id}/start",
                "stop": f"/models/api/{model_id}/stop",
                "health": f"/models/api/{model_id}/health",
            },
        }

    return jsonify(
        {
            "success": True,
            "data": {
                "total_models": len(MODEL_TYPES),
                "categories": list(
                    set(model["category"] for model in MODEL_TYPES.values())
                ),
                "models": model_apis,
                "system_resources": get_system_resources(),
            },
        }
    )


@models_bp.route("/<model_id>")
def model_detail(model_id):
    """Individual model detail page"""
    if model_id not in MODEL_TYPES:
        return render_template("errors/404.html"), 404

    model = MODEL_TYPES[model_id]
    status = get_model_status(model_id)

    # Get connected agents information
    connected_agents = []
    for agent_id in model["agents"]:
        try:
            # Import agent info
            agent_module = __import__(f"app.routes.agents", fromlist=["ALL_AGENTS"])
            if (
                hasattr(agent_module, "ALL_AGENTS")
                and agent_id in agent_module.ALL_AGENTS
            ):
                connected_agents.append(
                    {"id": agent_id, "info": agent_module.ALL_AGENTS[agent_id]}
                )
        except ImportError:
            pass

    return render_template(
        "models/detail.html",
        model_id=model_id,
        model=model,
        status=status,
        connected_agents=connected_agents,
    )


@models_bp.route("/api/<model_id>/status")
def model_status(model_id):
    """Get model status"""
    if model_id not in MODEL_TYPES:
        return jsonify({"error": "Model not found"}), 404

    status = get_model_status(model_id)
    model_info = MODEL_TYPES[model_id]

    return jsonify(
        {
            "success": True,
            "data": {
                "model_id": model_id,
                "model_info": model_info,
                "status": status,
                "timestamp": time.time(),
            },
        }
    )


@models_bp.route("/api/<model_id>/start", methods=["POST"])
def start_model(model_id):
    """Start a model service"""
    if model_id not in MODEL_TYPES:
        return jsonify({"error": "Model not found"}), 404

    try:
        # Try to start model with Ollama
        result = subprocess.run(
            ["ollama", "run", model_id], capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0:
            return jsonify(
                {
                    "success": True,
                    "message": f"Model {model_id} started successfully",
                    "model_id": model_id,
                }
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Failed to start model",
                        "details": result.stderr,
                    }
                ),
                500,
            )

    except subprocess.TimeoutExpired:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Model start timeout",
                    "details": "Model took too long to start",
                }
            ),
            500,
        )
    except FileNotFoundError:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Ollama not found",
                    "details": "Ollama service is not installed or not in PATH",
                }
            ),
            500,
        )


@models_bp.route("/api/<model_id>/stop", methods=["POST"])
def stop_model(model_id):
    """Stop a model service"""
    if model_id not in MODEL_TYPES:
        return jsonify({"error": "Model not found"}), 404

    try:
        # This would depend on how models are managed
        # For now, return success (would need actual implementation)
        return jsonify(
            {
                "success": True,
                "message": f"Model {model_id} stop requested",
                "model_id": model_id,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"success": False, "error": "Failed to stop model", "details": str(e)}
            ),
            500,
        )


@models_bp.route("/api/<model_id>/health")
def model_health(model_id):
    """Get detailed model health information"""
    if model_id not in MODEL_TYPES:
        return jsonify({"error": "Model not found"}), 404

    status = get_model_status(model_id)
    model_info = MODEL_TYPES[model_id]

    # Detailed health check
    health_data = {
        "model_id": model_id,
        "basic_info": model_info,
        "status": status,
        "health_score": 0,
        "checks": {
            "model_available": status["status"] != "not_available",
            "system_resources": get_system_resources(),
            "connected_agents": len(model_info["agents"]),
        },
        "timestamp": time.time(),
    }

    # Calculate health score
    checks_passed = sum(
        [
            health_data["checks"]["model_available"],
            health_data["checks"]["system_resources"]["cpu_percent"] < 80,
            health_data["checks"]["system_resources"]["memory_percent"] < 80,
            health_data["checks"]["connected_agents"] > 0,
        ]
    )

    health_data["health_score"] = (checks_passed / 4) * 100
    health_data["overall_health"] = (
        "healthy"
        if health_data["health_score"] > 75
        else "degraded" if health_data["health_score"] > 50 else "unhealthy"
    )

    return jsonify({"success": True, "data": health_data})


@models_bp.route("/analytics")
def models_analytics():
    """Models analytics and usage statistics"""
    analytics_data = {
        "total_models": len(MODEL_TYPES),
        "categories": {},
        "agent_connections": {},
        "system_resources": get_system_resources(),
        "model_statuses": {},
    }

    # Count by category
    for model_info in MODEL_TYPES.values():
        category = model_info["category"]
        analytics_data["categories"][category] = (
            analytics_data["categories"].get(category, 0) + 1
        )

    # Count agent connections
    for model_id, model_info in MODEL_TYPES.items():
        for agent in model_info["agents"]:
            analytics_data["agent_connections"][agent] = (
                analytics_data["agent_connections"].get(agent, 0) + 1
            )

        # Get model status
        analytics_data["model_statuses"][model_id] = get_model_status(model_id)

    return jsonify({"success": True, "data": analytics_data, "timestamp": time.time()})


@models_bp.route("/health")
def models_health():
    """Overall models system health"""
    health_status = {}
    healthy_count = 0

    for model_id in MODEL_TYPES.keys():
        status = get_model_status(model_id)
        is_healthy = status["status"] != "not_available"

        health_status[model_id] = {
            "status": "healthy" if is_healthy else "unavailable",
            "details": status,
            "last_check": time.time(),
        }

        if is_healthy:
            healthy_count += 1

    system_resources = get_system_resources()
    system_healthy = all(
        [
            system_resources["cpu_percent"] < 90,
            system_resources["memory_percent"] < 90,
            system_resources["disk_percent"] < 90,
        ]
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "overall_status": (
                    "healthy" if healthy_count > 0 and system_healthy else "degraded"
                ),
                "available_models": healthy_count,
                "total_models": len(MODEL_TYPES),
                "availability_percentage": (healthy_count / len(MODEL_TYPES)) * 100,
                "system_resources": system_resources,
                "system_healthy": system_healthy,
                "models": health_status,
                "timestamp": time.time(),
            },
        }
    )
