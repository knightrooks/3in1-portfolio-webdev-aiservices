"""
Base Agent Class
Foundation for all specialized AI agents
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import yaml
import os

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all AI agents"""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.model_ensemble = config.get("model_ensemble", {})
        self.capabilities = config.get("capabilities", [])
        self.persona = config.get("persona", {})
        self.tools = config.get("tools", [])
        self.status = config.get("status", "inactive")

        # Agent state
        self.session_data = {}
        self.conversation_history = []
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 0.0,
            "average_response_time": 0.0,
            "user_satisfaction": 0.0,
        }

        logger.info(f"Initialized {self.__class__.__name__}: {self.name}")

    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request and return response"""
        pass

    @abstractmethod
    async def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        pass

    async def initialize_models(self):
        """Initialize the model ensemble for this agent"""
        try:
            # Load model configurations
            initialized_models = {}

            for model_role, model_name in self.model_ensemble.items():
                # Here we would initialize actual model connections
                # For now, we'll simulate with configuration loading
                initialized_models[model_role] = {
                    "name": model_name,
                    "status": "ready",
                    "initialized_at": datetime.now().isoformat(),
                }

            self.initialized_models = initialized_models
            logger.info(f"Initialized {len(initialized_models)} models for {self.name}")

            return True

        except Exception as e:
            logger.error(f"Error initializing models for {self.name}: {e}")
            return False

    async def select_model(self, task_type: str) -> str:
        """Select appropriate model for task"""
        model_selection_map = {
            "coding": "primary_model",
            "analysis": "reasoning_model",
            "mathematics": "math_model",
            "translation": "multilingual_model",
            "search": "embedding_model",
            "strategy": "strategy_model",
            "content": "content_model",
            "research": "research_model",
        }

        model_role = model_selection_map.get(task_type, "primary_model")
        return self.model_ensemble.get(
            model_role, self.model_ensemble.get("primary_model")
        )

    async def execute_with_model(
        self, model_name: str, prompt: str, context: Dict = None
    ) -> Dict[str, Any]:
        """Execute task with specific model"""
        try:
            # Simulate model execution
            # In production, this would call the actual model runner

            response = {
                "model_used": model_name,
                "response": f"Response from {model_name} for: {prompt[:100]}...",
                "confidence": 0.85,
                "processing_time": 1.2,
                "context_used": context is not None,
            }

            return response

        except Exception as e:
            logger.error(f"Error executing with model {model_name}: {e}")
            return {"error": str(e), "model_used": model_name, "fallback_used": True}

    async def collaborate_with_agent(
        self, other_agent: str, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Collaborate with another agent"""
        try:
            # Simulate agent collaboration
            # In production, this would route to the actual agent

            collaboration_result = {
                "collaborating_agent": other_agent,
                "request_sent": request,
                "collaboration_successful": True,
                "timestamp": datetime.now().isoformat(),
            }

            return collaboration_result

        except Exception as e:
            logger.error(f"Error collaborating with {other_agent}: {e}")
            return {
                "error": str(e),
                "collaborating_agent": other_agent,
                "collaboration_successful": False,
            }

    def update_performance_metrics(self, task_result: Dict[str, Any]):
        """Update agent performance metrics"""
        try:
            self.performance_metrics["tasks_completed"] += 1

            if task_result.get("success", True):
                current_success = self.performance_metrics["success_rate"]
                total_tasks = self.performance_metrics["tasks_completed"]
                self.performance_metrics["success_rate"] = (
                    current_success * (total_tasks - 1) + 1.0
                ) / total_tasks

            if "processing_time" in task_result:
                current_avg = self.performance_metrics["average_response_time"]
                total_tasks = self.performance_metrics["tasks_completed"]
                new_time = task_result["processing_time"]
                self.performance_metrics["average_response_time"] = (
                    current_avg * (total_tasks - 1) + new_time
                ) / total_tasks

        except Exception as e:
            logger.error(f"Error updating performance metrics: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """Perform agent health check"""
        try:
            health_status = {
                "agent_name": self.name,
                "status": self.status,
                "models_initialized": len(getattr(self, "initialized_models", {})),
                "capabilities_count": len(self.capabilities),
                "performance_metrics": self.performance_metrics,
                "last_check": datetime.now().isoformat(),
                "healthy": True,
            }

            # Check model health
            if hasattr(self, "initialized_models"):
                model_health = {}
                for role, model_info in self.initialized_models.items():
                    model_health[role] = model_info.get("status") == "ready"

                health_status["model_health"] = model_health
                health_status["all_models_healthy"] = all(model_health.values())

            return health_status

        except Exception as e:
            logger.error(f"Error in health check for {self.name}: {e}")
            return {
                "agent_name": self.name,
                "healthy": False,
                "error": str(e),
                "last_check": datetime.now().isoformat(),
            }

    def get_agent_info(self) -> Dict[str, Any]:
        """Get comprehensive agent information"""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "model_ensemble": self.model_ensemble,
            "capabilities": self.capabilities,
            "persona": self.persona,
            "tools": self.tools,
            "status": self.status,
            "performance_metrics": self.performance_metrics,
            "session_active": len(self.session_data) > 0,
            "conversation_turns": len(self.conversation_history),
        }
