"""
AI Agents Module
This module contains all specialized AI agents for the 3-in-1 platform
"""

from .strategist import StrategistAgent
from .developer import DeveloperAgent
from .security_expert import SecurityExpertAgent
from .content_creator import ContentCreatorAgent
from .research_analyst import ResearchAnalystAgent
from .data_scientist import DataScientistAgent
from .customer_success import CustomerSuccessAgent
from .product_manager import ProductManagerAgent
from .marketing_specialist import MarketingSpecialistAgent
from .operations_manager import OperationsManagerAgent

__all__ = [
    "StrategistAgent",
    "DeveloperAgent",
    "SecurityExpertAgent",
    "ContentCreatorAgent",
    "ResearchAnalystAgent",
    "DataScientistAgent",
    "CustomerSuccessAgent",
    "ProductManagerAgent",
    "MarketingSpecialistAgent",
    "OperationsManagerAgent",
]

# Agent Registry for Dynamic Loading
AGENT_REGISTRY = {
    "strategist": StrategistAgent,
    "developer": DeveloperAgent,
    "security_expert": SecurityExpertAgent,
    "content_creator": ContentCreatorAgent,
    "research_analyst": ResearchAnalystAgent,
    "data_scientist": DataScientistAgent,
    "customer_success": CustomerSuccessAgent,
    "product_manager": ProductManagerAgent,
    "marketing_specialist": MarketingSpecialistAgent,
    "operations_manager": OperationsManagerAgent,
}


def get_agent_class(agent_name: str):
    """Get agent class by name"""
    return AGENT_REGISTRY.get(agent_name)


def list_available_agents():
    """List all available agents"""
    return list(AGENT_REGISTRY.keys())
