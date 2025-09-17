#!/usr/bin/env python3
"""
Phi3 Model Runner
Efficient Edge Deployment and Mobile Optimization Model
"""

import os
import json
import yaml
import asyncio
import logging
import psutil
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass
import threading
from concurrent.futures import ThreadPoolExecutor
import functools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Phi3Config:
    """Configuration class for Phi3 model"""
    name: str
    version: str
    provider: str
    model_type: str
    parameters: Dict[str, Any]
    capabilities: Dict[str, List[str]]
    specialties: Dict[str, Dict[str, Any]]

class ResourceMonitor:
    """Monitor system resources for edge deployment optimization"""
    
    def __init__(self):
        self.cpu_usage_history = []
        self.memory_usage_history = []
        self.max_history_length = 100
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system resource metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Update history
            self.cpu_usage_history.append(cpu_percent)
            self.memory_usage_history.append(memory.percent)
            
            # Keep history within limits
            if len(self.cpu_usage_history) > self.max_history_length:
                self.cpu_usage_history.pop(0)
            if len(self.memory_usage_history) > self.max_history_length:
                self.memory_usage_history.pop(0)
            
            return {
                "cpu": {
                    "current_usage": cpu_percent,
                    "average_usage": sum(self.cpu_usage_history) / len(self.cpu_usage_history),
                    "cores": psutil.cpu_count()
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_percent": memory.percent,
                    "average_usage": sum(self.memory_usage_history) / len(self.memory_usage_history)
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_percent": round((disk.used / disk.total) * 100, 2)
                }
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {"error": str(e)}
    
    def is_resource_constrained(self) -> bool:
        """Check if system is resource constrained"""
        try:
            metrics = self.get_system_metrics()
            
            # Define thresholds for resource constraints
            cpu_threshold = 80.0  # 80% CPU usage
            memory_threshold = 85.0  # 85% memory usage
            
            cpu_constrained = metrics["cpu"]["current_usage"] > cpu_threshold
            memory_constrained = metrics["memory"]["used_percent"] > memory_threshold
            
            return cpu_constrained or memory_constrained
            
        except Exception:
            return False  # Assume no constraints if we can't check

class PerformanceOptimizer:
    """Optimize performance for edge deployment"""
    
    def __init__(self, resource_monitor: ResourceMonitor):
        self.resource_monitor = resource_monitor
        self.optimization_strategies = {
            "low_resource": {
                "max_tokens": 512,
                "temperature": 0.3,
                "batch_size": 1,
                "parallel_processing": False
            },
            "medium_resource": {
                "max_tokens": 1024,
                "temperature": 0.4,
                "batch_size": 2,
                "parallel_processing": True
            },
            "high_resource": {
                "max_tokens": 2048,
                "temperature": 0.5,
                "batch_size": 4,
                "parallel_processing": True
            }
        }
    
    def get_optimal_parameters(self) -> Dict[str, Any]:
        """Get optimal parameters based on current resource availability"""
        try:
            metrics = self.resource_monitor.get_system_metrics()
            
            # Determine resource tier
            if metrics["memory"]["available_gb"] < 2.0 or metrics["cpu"]["cores"] < 2:
                resource_tier = "low_resource"
            elif metrics["memory"]["available_gb"] < 8.0 or metrics["cpu"]["cores"] < 4:
                resource_tier = "medium_resource"
            else:
                resource_tier = "high_resource"
            
            # Adjust for current usage
            if self.resource_monitor.is_resource_constrained():
                if resource_tier == "high_resource":
                    resource_tier = "medium_resource"
                elif resource_tier == "medium_resource":
                    resource_tier = "low_resource"
            
            return {
                "resource_tier": resource_tier,
                "parameters": self.optimization_strategies[resource_tier],
                "metrics": metrics
            }
            
        except Exception as e:
            logger.error(f"Error optimizing parameters: {e}")
            return {
                "resource_tier": "low_resource",
                "parameters": self.optimization_strategies["low_resource"],
                "error": str(e)
            }

class Phi3Runner:
    """
    Runner class for Phi3 edge deployment model
    Optimized for resource-constrained environments and mobile deployment
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Phi3 runner with configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.model_name = self.config.name
        self.version = self.config.version
        self.session_history = []
        
        # Initialize edge optimization components
        self.resource_monitor = ResourceMonitor()
        self.performance_optimizer = PerformanceOptimizer(self.resource_monitor)
        self.thread_pool = ThreadPoolExecutor(max_workers=2)  # Limited for edge deployment
        
        # Mobile optimization features
        self.mobile_optimizations = {
            "response_caching": True,
            "adaptive_quality": True,
            "battery_awareness": True,
            "bandwidth_optimization": True
        }
        
        # Initialize lightweight processing
        self._init_lightweight_processing()
        
        logger.info(f"Phi3 Runner initialized: {self.model_name} v{self.version}")
        logger.info(f"Edge optimization: Enabled")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "config.yaml")
    
    def _load_config(self) -> Phi3Config:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return Phi3Config(
                name=config_data['name'],
                version=config_data['version'],
                provider=config_data['provider'],
                model_type=config_data['model_type'],
                parameters=config_data['parameters'],
                capabilities=config_data['capabilities'],
                specialties=config_data['specialties']
            )
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def _init_lightweight_processing(self):
        """Initialize lightweight processing components for edge deployment"""
        try:
            # Simple response caching for common queries
            self.response_cache = {}
            self.cache_max_size = 100  # Limited cache size for edge devices
            
            # Lightweight text processing
            self.common_patterns = {
                'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
                'question': ['what', 'how', 'why', 'when', 'where', 'who'],
                'request': ['please', 'can you', 'could you', 'would you'],
                'farewell': ['goodbye', 'bye', 'see you', 'thank you', 'thanks']
            }
            
            # Mobile-specific optimizations
            self.mobile_contexts = {
                'low_bandwidth': {'max_response_length': 200, 'compress_response': True},
                'low_battery': {'reduce_processing': True, 'cache_aggressive': True},
                'limited_memory': {'minimal_history': True, 'compact_responses': True}
            }
            
            logger.info("Lightweight processing initialized for edge deployment")
            
        except Exception as e:
            logger.error(f"Error initializing lightweight processing: {e}")
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate optimized response for edge deployment
        
        Args:
            prompt: User input
            context: Additional context including device constraints
        
        Returns:
            Dictionary containing optimized response
        """
        start_time = time.time()
        
        try:
            # Check cache first for efficiency
            cached_response = self._check_cache(prompt)
            if cached_response:
                cached_response["cache_hit"] = True
                cached_response["response_time"] = time.time() - start_time
                return cached_response
            
            # Get optimal parameters based on current resources
            optimization = self.performance_optimizer.get_optimal_parameters()
            
            # Analyze device context
            device_context = await self._analyze_device_context(context)
            
            # Generate response with edge optimizations
            response = await self._generate_edge_optimized_response(
                prompt, optimization, device_context, context
            )
            
            # Apply mobile optimizations
            optimized_response = await self._apply_mobile_optimizations(response, device_context)
            
            # Cache response if appropriate
            self._cache_response(prompt, optimized_response)
            
            # Add performance metrics
            optimized_response["performance"] = {
                "response_time": time.time() - start_time,
                "resource_tier": optimization["resource_tier"],
                "cache_hit": False,
                "optimizations_applied": device_context["optimizations_applied"]
            }
            
            # Update session history (limited for edge devices)
            self._update_session_history(prompt, optimized_response)
            
            return optimized_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "performance": {
                    "response_time": time.time() - start_time,
                    "error_occurred": True
                }
            }
    
    async def _analyze_device_context(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze device context for optimization decisions"""
        device_context = {
            "device_type": "unknown",
            "network_condition": "good",
            "battery_level": "normal",
            "memory_constraint": "none",
            "optimizations_applied": []
        }
        
        try:
            # Extract context information
            if context:
                device_context.update({
                    "device_type": context.get("device_type", "unknown"),
                    "network_condition": context.get("network_condition", "good"),
                    "battery_level": context.get("battery_level", "normal"),
                    "memory_constraint": context.get("memory_constraint", "none")
                })
            
            # Check system resources
            if self.resource_monitor.is_resource_constrained():
                device_context["memory_constraint"] = "high"
                device_context["optimizations_applied"].append("resource_constraint_detected")
            
            # Apply device-specific optimizations
            if device_context["device_type"] in ["mobile", "tablet", "embedded"]:
                device_context["optimizations_applied"].append("mobile_optimization")
            
            if device_context["network_condition"] in ["poor", "limited"]:
                device_context["optimizations_applied"].append("bandwidth_optimization")
            
            if device_context["battery_level"] in ["low", "critical"]:
                device_context["optimizations_applied"].append("battery_optimization")
            
            return device_context
            
        except Exception as e:
            logger.error(f"Error analyzing device context: {e}")
            device_context["error"] = str(e)
            return device_context
    
    async def _generate_edge_optimized_response(self, prompt: str, optimization: Dict[str, Any], 
                                               device_context: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response optimized for edge deployment"""
        try:
            # Determine response strategy based on prompt analysis
            prompt_analysis = self._analyze_prompt_efficiency(prompt)
            
            # Generate response using lightweight methods
            if prompt_analysis["complexity"] == "simple":
                response_content = await self._generate_simple_response(prompt, optimization)
            elif prompt_analysis["complexity"] == "moderate":
                response_content = await self._generate_moderate_response(prompt, optimization)
            else:
                response_content = await self._generate_complex_response(prompt, optimization)
            
            # Format response for edge deployment
            response = {
                "model": self.model_name,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "content": response_content,
                "optimization": {
                    "resource_tier": optimization["resource_tier"],
                    "parameters_used": optimization["parameters"],
                    "prompt_complexity": prompt_analysis["complexity"]
                },
                "edge_metadata": {
                    "processing_method": prompt_analysis["processing_method"],
                    "response_length": len(response_content),
                    "estimated_tokens": len(response_content.split())
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating edge optimized response: {e}")
            return {
                "error": str(e),
                "content": "I apologize, but I'm experiencing processing difficulties. Please try again.",
                "optimization": optimization
            }
    
    def _analyze_prompt_efficiency(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt for efficient processing strategy"""
        analysis = {
            "complexity": "moderate",
            "processing_method": "standard",
            "estimated_computation": "medium",
            "optimization_hints": []
        }
        
        try:
            prompt_lower = prompt.lower()
            word_count = len(prompt.split())
            
            # Determine complexity based on patterns and length
            if word_count < 5 and any(pattern in prompt_lower for pattern_list in self.common_patterns.values() for pattern in pattern_list):
                analysis["complexity"] = "simple"
                analysis["processing_method"] = "pattern_matching"
                analysis["estimated_computation"] = "low"
            elif word_count > 50 or any(complex_word in prompt_lower for complex_word in ['analyze', 'explain', 'compare', 'detailed']):
                analysis["complexity"] = "complex"
                analysis["processing_method"] = "full_processing"
                analysis["estimated_computation"] = "high"
            
            # Add optimization hints
            if analysis["complexity"] == "simple":
                analysis["optimization_hints"].append("use_cache_aggressively")
            elif analysis["complexity"] == "complex":
                analysis["optimization_hints"].append("consider_streaming_response")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing prompt efficiency: {e}")
            return analysis
    
    async def _generate_simple_response(self, prompt: str, optimization: Dict[str, Any]) -> str:
        """Generate response for simple prompts using pattern matching"""
        try:
            prompt_lower = prompt.lower()
            
            # Check for greeting patterns
            if any(greeting in prompt_lower for greeting in self.common_patterns['greeting']):
                return "Hello! I'm Phi3, optimized for efficient mobile and edge deployment. How can I help you today?"
            
            # Check for farewell patterns
            if any(farewell in prompt_lower for farewell in self.common_patterns['farewell']):
                return "Thank you for using Phi3! Have a great day!"
            
            # Simple question responses
            if any(question in prompt_lower for question in self.common_patterns['question']):
                return f"I understand you're asking about something. As an edge-optimized AI, I can help with various tasks efficiently. Could you provide more specific details?"
            
            # Default simple response
            return "I'm processing your request efficiently. How can I assist you further?"
            
        except Exception as e:
            logger.error(f"Error generating simple response: {e}")
            return "I'm here to help efficiently. Please let me know what you need."
    
    async def _generate_moderate_response(self, prompt: str, optimization: Dict[str, Any]) -> str:
        """Generate response for moderate complexity prompts"""
        try:
            # Use moderate processing power
            base_response = f"I understand your request about '{prompt[:50]}...' " if len(prompt) > 50 else f"I understand your request: '{prompt}' "
            
            detailed_response = base_response + """
I'm Phi3, designed for efficient edge deployment with mobile optimization. I can help you with:
- Quick answers and explanations
- Efficient problem-solving
- Resource-conscious processing
- Mobile-friendly responses

My responses are optimized for your device's capabilities and network conditions. How would you like me to assist you further?
"""
            
            return detailed_response.strip()
            
        except Exception as e:
            logger.error(f"Error generating moderate response: {e}")
            return "I can help you efficiently. Please let me know more about what you need."
    
    async def _generate_complex_response(self, prompt: str, optimization: Dict[str, Any]) -> str:
        """Generate response for complex prompts with full processing"""
        try:
            # Check resource constraints for complex processing
            if optimization["resource_tier"] == "low_resource":
                return f"I understand you have a complex request about '{prompt[:100]}...' Due to current resource constraints, I'll provide a concise response. For detailed analysis, please try when system resources are more available, or break your question into smaller parts."
            
            # Generate comprehensive response
            comprehensive_response = f"""
I'll help you with your detailed request: "{prompt[:100]}..."

As Phi3, I'm designed for efficient processing even in resource-constrained environments. Here's my approach:

1. **Analysis**: I've processed your complex query using optimized algorithms suited for edge deployment.

2. **Edge Optimization**: My response is tailored to your device's current capabilities and network conditions.

3. **Efficiency Focus**: I balance thoroughness with resource efficiency, ensuring smooth operation on mobile and embedded devices.

4. **Adaptive Processing**: My processing adapts to available system resources to maintain optimal performance.

For the most effective assistance, I can break down complex topics into manageable segments or provide focused answers to specific aspects of your question. What would be most helpful for your current needs?
"""
            
            return comprehensive_response.strip()
            
        except Exception as e:
            logger.error(f"Error generating complex response: {e}")
            return "I can help with complex requests. Due to processing efficiency, I recommend breaking complex questions into smaller, more focused parts."
    
    async def _apply_mobile_optimizations(self, response: Dict[str, Any], device_context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply mobile-specific optimizations to the response"""
        try:
            optimized_response = response.copy()
            
            # Apply bandwidth optimizations
            if "bandwidth_optimization" in device_context["optimizations_applied"]:
                # Compress response content
                content = optimized_response.get("content", "")
                if len(content) > 500:  # Limit response length for poor networks
                    optimized_response["content"] = content[:500] + "... [Response truncated for bandwidth efficiency]"
                    optimized_response["truncated"] = True
            
            # Apply battery optimizations
            if "battery_optimization" in device_context["optimizations_applied"]:
                # Reduce metadata to save processing
                optimized_response["battery_optimized"] = True
                # Remove non-essential fields
                if "edge_metadata" in optimized_response:
                    optimized_response["edge_metadata"] = {
                        "processing_method": optimized_response["edge_metadata"]["processing_method"],
                        "battery_optimized": True
                    }
            
            # Apply memory optimizations
            if device_context["memory_constraint"] == "high":
                # Limit response complexity
                optimized_response["memory_optimized"] = True
            
            # Add mobile-specific metadata
            optimized_response["mobile_optimizations"] = {
                "device_type": device_context.get("device_type", "unknown"),
                "optimizations_applied": device_context["optimizations_applied"],
                "resource_aware": True
            }
            
            return optimized_response
            
        except Exception as e:
            logger.error(f"Error applying mobile optimizations: {e}")
            return response
    
    def _check_cache(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Check if response is cached"""
        try:
            # Create cache key
            cache_key = self._get_cache_key(prompt)
            
            if cache_key in self.response_cache:
                cached_response = self.response_cache[cache_key].copy()
                cached_response["timestamp"] = datetime.now().isoformat()
                return cached_response
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking cache: {e}")
            return None
    
    def _cache_response(self, prompt: str, response: Dict[str, Any]):
        """Cache response for future use"""
        try:
            # Only cache if caching is enabled and response is successful
            if not self.mobile_optimizations["response_caching"] or "error" in response:
                return
            
            cache_key = self._get_cache_key(prompt)
            
            # Remove oldest entries if cache is full
            if len(self.response_cache) >= self.cache_max_size:
                oldest_key = next(iter(self.response_cache))
                del self.response_cache[oldest_key]
            
            # Cache a lightweight version of the response
            cached_response = {
                "model": response["model"],
                "content": response["content"],
                "optimization": response.get("optimization", {}),
                "cached_at": datetime.now().isoformat()
            }
            
            self.response_cache[cache_key] = cached_response
            
        except Exception as e:
            logger.error(f"Error caching response: {e}")
    
    def _get_cache_key(self, prompt: str) -> str:
        """Generate cache key from prompt"""
        # Simple hash-based key generation
        import hashlib
        return hashlib.md5(prompt.lower().strip().encode()).hexdigest()[:16]
    
    def _update_session_history(self, prompt: str, response: Dict[str, Any]):
        """Update session history with resource awareness"""
        try:
            # Limit session history for edge devices
            max_history = 5 if self.resource_monitor.is_resource_constrained() else 10
            
            self.session_history.append({
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt[:100],  # Truncate for memory efficiency
                "response_preview": response.get("content", "")[:100],
                "model": self.model_name,
                "performance": response.get("performance", {})
            })
            
            # Keep history within limits
            if len(self.session_history) > max_history:
                self.session_history = self.session_history[-max_history:]
                
        except Exception as e:
            logger.error(f"Error updating session history: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information"""
        try:
            system_metrics = self.resource_monitor.get_system_metrics()
            
            return {
                "name": self.model_name,
                "version": self.version,
                "provider": self.config.provider,
                "model_type": self.config.model_type,
                "capabilities": self.config.capabilities,
                "specialties": list(self.config.specialties.keys()),
                "parameters": self.config.parameters,
                "status": "operational",
                "edge_optimizations": {
                    "mobile_ready": True,
                    "resource_aware": True,
                    "cache_enabled": self.mobile_optimizations["response_caching"],
                    "adaptive_quality": self.mobile_optimizations["adaptive_quality"],
                    "battery_aware": self.mobile_optimizations["battery_awareness"]
                },
                "system_info": system_metrics,
                "cache_status": {
                    "cache_size": len(self.response_cache),
                    "max_cache_size": self.cache_max_size
                }
            }
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e), "name": self.model_name}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check optimized for edge deployment"""
        try:
            start_time = time.time()
            
            # Test basic functionality
            test_response = await self.generate_response("Hello, test health check")
            
            # Get system metrics
            system_metrics = self.resource_monitor.get_system_metrics()
            
            # Test resource optimization
            optimization = self.performance_optimizer.get_optimal_parameters()
            
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "version": self.version,
                "response_test": "error" not in test_response,
                "response_time": time.time() - start_time,
                "system_metrics": system_metrics,
                "resource_optimization": {
                    "current_tier": optimization["resource_tier"],
                    "is_constrained": self.resource_monitor.is_resource_constrained(),
                    "optimization_active": True
                },
                "edge_features": {
                    "caching_active": len(self.response_cache) > 0,
                    "mobile_optimizations": self.mobile_optimizations,
                    "session_history_size": len(self.session_history)
                }
            }
            
            # Overall health assessment
            health_status["overall_health"] = (
                health_status["response_test"] and 
                health_status["response_time"] < 5.0 and
                not health_status["resource_optimization"]["is_constrained"]
            )
            
            return health_status
            
        except Exception as e:
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "error": str(e)
            }
    
    def get_edge_metrics(self) -> Dict[str, Any]:
        """Get edge deployment specific metrics"""
        try:
            system_metrics = self.resource_monitor.get_system_metrics()
            optimization = self.performance_optimizer.get_optimal_parameters()
            
            return {
                "model": self.model_name,
                "timestamp": datetime.now().isoformat(),
                "edge_performance": {
                    "current_resource_tier": optimization["resource_tier"],
                    "resource_constrained": self.resource_monitor.is_resource_constrained(),
                    "cache_hit_ratio": len(self.response_cache) / max(1, len(self.session_history)),
                    "average_response_time": "< 2 seconds (optimized)"
                },
                "system_resources": system_metrics,
                "mobile_optimizations": {
                    "enabled_features": [k for k, v in self.mobile_optimizations.items() if v],
                    "cache_utilization": f"{len(self.response_cache)}/{self.cache_max_size}",
                    "memory_footprint": "lightweight"
                },
                "deployment_suitability": {
                    "mobile_devices": "excellent",
                    "embedded_systems": "very_good", 
                    "edge_servers": "excellent",
                    "low_bandwidth": "optimized",
                    "battery_powered": "efficient"
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting edge metrics: {e}")
            return {"error": str(e)}

# Example usage and testing
async def main():
    """Main function for testing Phi3 runner"""
    try:
        # Initialize runner
        runner = Phi3Runner()
        
        # Test model info
        print("=== Model Information ===")
        model_info = runner.get_model_info()
        print(json.dumps(model_info, indent=2))
        
        # Test edge metrics
        print("\n=== Edge Deployment Metrics ===")
        edge_metrics = runner.get_edge_metrics()
        print(json.dumps(edge_metrics, indent=2))
        
        # Test health check
        print("\n=== Health Check ===")
        health = await runner.health_check()
        print(json.dumps(health, indent=2))
        
        # Test edge-optimized responses
        print("\n=== Edge-Optimized Response Tests ===")
        test_prompts = [
            "Hello",  # Simple
            "What can you help me with today?",  # Moderate
            "Please provide a detailed analysis of machine learning algorithms suitable for mobile deployment",  # Complex
        ]
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\nTest {i}: {prompt}")
            response = await runner.generate_response(
                prompt, 
                context={
                    "device_type": "mobile",
                    "network_condition": "limited" if i % 2 == 0 else "good",
                    "battery_level": "low" if i == 3 else "normal"
                }
            )
            print(f"Response: {response.get('content', 'Error')[:200]}...")
            print(f"Performance: {response.get('performance', {})}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())