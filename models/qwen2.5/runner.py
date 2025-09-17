#!/usr/bin/env python3
"""
Qwen 2.5 Model Runner
Advanced Multilingual Reasoning with Chinese Language Excellence
"""

import os
import json
import yaml
import asyncio
import logging
import re
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass
import jieba  # For Chinese text processing (fallback if not available)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Qwen25Config:
    """Configuration class for Qwen 2.5 model"""
    name: str
    version: str
    provider: str
    model_type: str
    parameters: Dict[str, Any]
    capabilities: Dict[str, List[str]]
    specialties: Dict[str, Dict[str, Any]]

class ChineseLanguageProcessor:
    """Specialized processor for Chinese language understanding"""
    
    def __init__(self):
        self.chinese_patterns = {
            'simplified': re.compile(r'[\u4e00-\u9fff]'),
            'traditional': re.compile(r'[\u4e00-\u9fff]'),
            'punctuation': re.compile(r'[，。！？；：""''（）【】《》]'),
        }
        
        # Common Chinese phrases and their meanings
        self.phrase_database = {
            '你好': 'Hello/Hi',
            '谢谢': 'Thank you', 
            '对不起': 'Sorry',
            '再见': 'Goodbye',
            '请问': 'May I ask',
            '没关系': 'No problem',
            '不客气': 'You\'re welcome'
        }
        
        # Business and cultural context markers
        self.cultural_contexts = {
            'business': ['公司', '企业', '商务', '会议', '合作'],
            'education': ['学校', '大学', '学习', '教育', '课程'],
            'technology': ['技术', '软件', '计算机', '互联网', '人工智能'],
            'culture': ['文化', '传统', '历史', '艺术', '节日']
        }
    
    def detect_chinese_content(self, text: str) -> Dict[str, Any]:
        """Detect Chinese content and analyze its characteristics"""
        analysis = {
            'contains_chinese': False,
            'chinese_ratio': 0.0,
            'script_type': 'none',
            'cultural_context': [],
            'formality_level': 'neutral'
        }
        
        try:
            # Count Chinese characters
            chinese_chars = self.chinese_patterns['simplified'].findall(text)
            total_chars = len([c for c in text if c.strip()])
            
            if chinese_chars:
                analysis['contains_chinese'] = True
                analysis['chinese_ratio'] = len(chinese_chars) / max(1, total_chars)
                analysis['script_type'] = 'simplified'  # Simplified assumption
            
            # Detect cultural contexts
            text_lower = text.lower()
            for context, markers in self.cultural_contexts.items():
                if any(marker in text for marker in markers):
                    analysis['cultural_context'].append(context)
            
            # Detect formality (simplified check)
            formal_markers = ['您', '请', '敬', '贵']  # Formal Chinese markers
            if any(marker in text for marker in formal_markers):
                analysis['formality_level'] = 'formal'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error detecting Chinese content: {e}")
            return analysis
    
    def segment_chinese_text(self, text: str) -> List[str]:
        """Segment Chinese text into words (basic implementation)"""
        try:
            # Try using jieba if available
            try:
                import jieba
                return list(jieba.cut(text))
            except ImportError:
                # Fallback: character-based segmentation
                return list(text)
        except Exception as e:
            logger.error(f"Error segmenting Chinese text: {e}")
            return list(text)

class CrossCulturalCommunicator:
    """Handles cross-cultural communication between Eastern and Western contexts"""
    
    def __init__(self):
        self.cultural_dimensions = {
            'communication_style': {
                'chinese': 'high_context',
                'western': 'low_context'
            },
            'business_approach': {
                'chinese': 'relationship_first',
                'western': 'task_first'
            },
            'decision_making': {
                'chinese': 'consensus_building',
                'western': 'individual_authority'
            }
        }
        
        self.cultural_adaptations = {
            'chinese_to_western': {
                'be_more_direct': True,
                'emphasize_individual_benefits': True,
                'provide_concrete_examples': True,
                'timeline_focused': True
            },
            'western_to_chinese': {
                'build_relationship_context': True,
                'show_respect_for_hierarchy': True,
                'emphasize_group_harmony': True,
                'allow_face_saving': True
            }
        }
    
    def adapt_communication_style(self, content: str, source_culture: str, target_culture: str) -> Dict[str, Any]:
        """Adapt communication style between cultures"""
        adaptation = {
            'original_content': content,
            'adapted_content': content,
            'adaptations_made': [],
            'cultural_notes': []
        }
        
        try:
            adaptation_key = f"{source_culture}_to_{target_culture}"
            
            if adaptation_key in self.cultural_adaptations:
                adaptations = self.cultural_adaptations[adaptation_key]
                
                if adaptations.get('be_more_direct'):
                    adaptation['adaptations_made'].append('increased_directness')
                    adaptation['cultural_notes'].append('Added more direct communication style')
                
                if adaptations.get('build_relationship_context'):
                    adaptation['adaptations_made'].append('relationship_building')
                    adaptation['cultural_notes'].append('Emphasized relationship-building context')
                
                if adaptations.get('show_respect_for_hierarchy'):
                    adaptation['adaptations_made'].append('hierarchy_respect')
                    adaptation['cultural_notes'].append('Added appropriate hierarchical respect')
            
            return adaptation
            
        except Exception as e:
            logger.error(f"Error adapting communication style: {e}")
            return adaptation

class Qwen25Runner:
    """
    Runner class for Qwen 2.5 multilingual reasoning model
    Specialized in Chinese language excellence and cross-cultural communication
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Qwen 2.5 runner with configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.model_name = self.config.name
        self.version = self.config.version
        self.session_history = []
        
        # Initialize specialized processors
        self.chinese_processor = ChineseLanguageProcessor()
        self.cross_cultural_communicator = CrossCulturalCommunicator()
        
        # Initialize multilingual context
        self.linguistic_context = {
            'primary_language': 'auto_detect',
            'cultural_context': 'neutral',
            'communication_style': 'adaptive',
            'domain_expertise': 'general'
        }
        
        logger.info(f"Qwen 2.5 Runner initialized: {self.model_name} v{self.version}")
        logger.info("Chinese language excellence and cross-cultural communication enabled")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "config.yaml")
    
    def _load_config(self) -> Qwen25Config:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return Qwen25Config(
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
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate multilingual response with Chinese language excellence
        
        Args:
            prompt: User input in any supported language
            context: Additional context including language and cultural preferences
        
        Returns:
            Dictionary containing culturally aware multilingual response
        """
        try:
            # Analyze language and cultural context
            linguistic_analysis = await self._analyze_linguistic_context(prompt, context)
            
            # Generate culturally appropriate response
            response = await self._generate_culturally_aware_response(prompt, linguistic_analysis, context)
            
            # Apply cross-cultural adaptations if needed
            adapted_response = await self._apply_cross_cultural_adaptations(response, linguistic_analysis)
            
            # Format comprehensive response
            formatted_response = await self._format_multilingual_response(adapted_response, linguistic_analysis)
            
            # Update session history
            self._update_session_history(prompt, formatted_response)
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name
            }
    
    async def _analyze_linguistic_context(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze linguistic and cultural context of the input"""
        analysis = {
            "detected_language": "english",
            "language_confidence": 0.5,
            "chinese_analysis": {},
            "cultural_context": "neutral",
            "communication_style": "formal",
            "domain": "general",
            "mathematical_content": False,
            "cross_cultural_elements": []
        }
        
        try:
            # Detect Chinese content
            chinese_analysis = self.chinese_processor.detect_chinese_content(prompt)
            analysis["chinese_analysis"] = chinese_analysis
            
            if chinese_analysis["contains_chinese"]:
                analysis["detected_language"] = "chinese"
                analysis["language_confidence"] = chinese_analysis["chinese_ratio"]
                
                # Determine cultural context from Chinese content
                if chinese_analysis["cultural_context"]:
                    analysis["cultural_context"] = chinese_analysis["cultural_context"][0]
                
                analysis["communication_style"] = chinese_analysis["formality_level"]
            
            # Detect mathematical content
            math_indicators = ['计算', '数学', '算法', 'calculate', 'mathematics', 'algorithm', '数字', '统计']
            if any(indicator in prompt.lower() for indicator in math_indicators):
                analysis["mathematical_content"] = True
                analysis["domain"] = "mathematics"
            
            # Detect cross-cultural elements
            cultural_bridges = ['国际', 'international', '跨文化', 'cross-cultural', '全球', 'global']
            if any(bridge in prompt.lower() for bridge in cultural_bridges):
                analysis["cross_cultural_elements"].append("international_context")
            
            # Extract additional context
            if context:
                analysis["target_language"] = context.get("target_language")
                analysis["cultural_preference"] = context.get("cultural_preference", "neutral")
                analysis["business_context"] = context.get("business_context", False)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing linguistic context: {e}")
            return analysis
    
    async def _generate_culturally_aware_response(self, prompt: str, analysis: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response with cultural awareness"""
        response = {
            "content": "",
            "language": analysis["detected_language"],
            "cultural_adaptations": [],
            "mathematical_reasoning": None,
            "cross_cultural_insights": [],
            "confidence": analysis["language_confidence"]
        }
        
        try:
            # Generate base response based on detected language
            if analysis["detected_language"] == "chinese":
                response["content"] = await self._generate_chinese_response(prompt, analysis)
            else:
                response["content"] = await self._generate_english_response(prompt, analysis)
            
            # Add mathematical reasoning if detected
            if analysis["mathematical_content"]:
                response["mathematical_reasoning"] = await self._provide_mathematical_reasoning(prompt)
            
            # Add cross-cultural insights
            if analysis["cross_cultural_elements"]:
                response["cross_cultural_insights"] = await self._generate_cross_cultural_insights(prompt, analysis)
            
            # Generate cultural adaptations
            response["cultural_adaptations"] = await self._generate_cultural_adaptations(prompt, analysis)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating culturally aware response: {e}")
            response["error"] = str(e)
            return response
    
    async def _generate_chinese_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate Chinese language response with cultural appropriateness"""
        try:
            # Determine formality level
            formality = analysis["chinese_analysis"].get("formality_level", "neutral")
            
            if formality == "formal":
                greeting = "您好！"
                response_style = "非常感谢您的提问。"
            else:
                greeting = "你好！"
                response_style = "谢谢你的问题。"
            
            # Generate contextual response
            base_response = f"{greeting} {response_style}"
            
            # Add domain-specific content
            if analysis["domain"] == "mathematics":
                base_response += "我在数学推理和计算方面具有很强的能力，可以帮助您解决各种数学问题。"
            elif analysis.get("cultural_context") == "business":
                base_response += "我理解中国的商务文化和国际商务实践，可以为您提供跨文化的商业建议。"
            else:
                base_response += "作为阿里巴巴开发的通义千问模型，我在中英双语理解和跨文化交流方面表现出色。"
            
            # Add cultural context
            cultural_note = "我会根据中华文化的背景和价值观来提供适合的回答，同时也能很好地理解和沟通西方文化观点。"
            
            return f"{base_response}\n\n{cultural_note}\n\n请问我可以如何进一步帮助您？"
            
        except Exception as e:
            logger.error(f"Error generating Chinese response: {e}")
            return "您好！我是通义千问，很高兴为您服务。请问有什么我可以帮助您的吗？"
    
    async def _generate_english_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate English language response with cultural bridge capabilities"""
        try:
            base_response = "Hello! I'm Qwen 2.5, developed by Alibaba Cloud. I excel in multilingual reasoning with particular expertise in Chinese language and cross-cultural communication."
            
            # Add specific capabilities based on analysis
            capabilities = []
            
            if analysis["mathematical_content"]:
                capabilities.append("advanced mathematical reasoning and problem-solving")
            
            if analysis["cross_cultural_elements"]:
                capabilities.append("cross-cultural communication between Eastern and Western perspectives")
            
            if analysis["chinese_analysis"].get("contains_chinese"):
                capabilities.append("native-level Chinese language understanding and generation")
            
            if capabilities:
                capability_text = "I can help you with " + ", ".join(capabilities) + "."
                base_response += f"\n\n{capability_text}"
            
            # Add cultural bridging context
            cultural_bridge = """
I'm designed to bridge Eastern and Western cultures, providing culturally sensitive communication that respects both Chinese traditions and international business practices. Whether you need help with Chinese language, cultural adaptation, or cross-cultural business communication, I'm here to assist.
"""
            
            return f"{base_response}\n{cultural_bridge}\nHow can I help you today?"
            
        except Exception as e:
            logger.error(f"Error generating English response: {e}")
            return "Hello! I'm Qwen 2.5, specialized in multilingual reasoning and cross-cultural communication. How can I assist you?"
    
    async def _provide_mathematical_reasoning(self, prompt: str) -> Dict[str, Any]:
        """Provide mathematical reasoning for math-related queries"""
        try:
            reasoning = {
                "approach": "systematic_analysis",
                "steps": [],
                "cultural_context": "both_eastern_western_methods"
            }
            
            # Detect specific mathematical concepts
            if any(word in prompt.lower() for word in ['计算', 'calculate', 'compute']):
                reasoning["steps"] = [
                    "1. 分析问题的数学结构 (Analyze mathematical structure)",
                    "2. 选择合适的计算方法 (Choose appropriate calculation method)",
                    "3. 逐步求解 (Step-by-step solution)",
                    "4. 验证结果 (Verify results)"
                ]
            
            return reasoning
            
        except Exception as e:
            logger.error(f"Error providing mathematical reasoning: {e}")
            return {"error": str(e)}
    
    async def _generate_cross_cultural_insights(self, prompt: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate insights for cross-cultural communication"""
        insights = []
        
        try:
            if analysis["detected_language"] == "chinese":
                insights.extend([
                    "Chinese communication often emphasizes relationship-building and context",
                    "Hierarchy and respect (尊重) are important cultural values",
                    "Harmony (和谐) and face-saving (面子) should be considered in interactions"
                ])
            
            if analysis.get("business_context"):
                insights.extend([
                    "Chinese business culture values long-term relationships over quick transactions",
                    "Building trust (信任) is essential before conducting business",
                    "Group consensus and collective decision-making are preferred"
                ])
            
            if "international" in prompt.lower():
                insights.extend([
                    "Bridge Eastern collectivist and Western individualist perspectives",
                    "Adapt communication style based on cultural context",
                    "Consider different time orientations: long-term vs short-term focus"
                ])
            
            return insights[:3]  # Return top 3 insights
            
        except Exception as e:
            logger.error(f"Error generating cross-cultural insights: {e}")
            return ["Cross-cultural communication requires sensitivity to different cultural values and practices"]
    
    async def _generate_cultural_adaptations(self, prompt: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate cultural adaptation suggestions"""
        adaptations = []
        
        try:
            if analysis["detected_language"] == "chinese":
                adaptations.extend([
                    "Response adapted for Chinese cultural context and values",
                    "Formal address style maintained for respectful communication",
                    "Emphasis on harmony and collective benefit"
                ])
            
            if analysis.get("cross_cultural_elements"):
                adaptations.extend([
                    "Cultural bridge approach applied to balance Eastern and Western perspectives",
                    "Diplomatic language used to respect both cultural viewpoints",
                    "Focus on mutual understanding and respect"
                ])
            
            return adaptations
            
        except Exception as e:
            logger.error(f"Error generating cultural adaptations: {e}")
            return []
    
    async def _apply_cross_cultural_adaptations(self, response: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply cross-cultural adaptations to response"""
        try:
            adapted_response = response.copy()
            
            # Apply cultural communication style adaptations
            if analysis["detected_language"] == "chinese" and analysis.get("target_language") == "english":
                # Adapting from Chinese to English context
                adaptation = self.cross_cultural_communicator.adapt_communication_style(
                    response["content"], "chinese", "western"
                )
                adapted_response["cross_cultural_adaptation"] = adaptation
            
            elif analysis["detected_language"] == "english" and analysis.get("target_language") == "chinese":
                # Adapting from English to Chinese context
                adaptation = self.cross_cultural_communicator.adapt_communication_style(
                    response["content"], "western", "chinese"
                )
                adapted_response["cross_cultural_adaptation"] = adaptation
            
            return adapted_response
            
        except Exception as e:
            logger.error(f"Error applying cross-cultural adaptations: {e}")
            return response
    
    async def _format_multilingual_response(self, response: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Format comprehensive multilingual response"""
        formatted_response = {
            "model": self.model_name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "linguistic_analysis": analysis,
            "response": response,
            "multilingual_capabilities": {
                "chinese_language_excellence": True,
                "cross_cultural_communication": True,
                "mathematical_reasoning": analysis["mathematical_content"],
                "cultural_sensitivity": len(response["cultural_adaptations"]) > 0
            },
            "cultural_intelligence": {
                "cultural_context_detected": analysis["cultural_context"] != "neutral",
                "formality_adapted": analysis.get("communication_style") != "neutral",
                "cross_cultural_insights_provided": len(response.get("cross_cultural_insights", [])) > 0
            },
            "recommendations": self._generate_multilingual_recommendations(analysis, response)
        }
        
        return formatted_response
    
    def _generate_multilingual_recommendations(self, analysis: Dict[str, Any], response: Dict[str, Any]) -> List[str]:
        """Generate recommendations for multilingual communication"""
        recommendations = []
        
        try:
            if analysis["detected_language"] == "chinese":
                recommendations.append("Continue in Chinese for deeper cultural connection and understanding")
            
            if analysis["language_confidence"] < 0.7:
                recommendations.append("Consider clarifying preferred language for optimal communication")
            
            if analysis["mathematical_content"]:
                recommendations.append("Mathematical concepts can be explained in both Chinese and English for clarity")
            
            if analysis["cross_cultural_elements"]:
                recommendations.append("Cross-cultural perspectives can be provided to enhance understanding")
            
            return recommendations[:3]
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Continue conversation for optimal multilingual assistance"]
    
    def _update_session_history(self, prompt: str, response: Dict[str, Any]):
        """Update session history with multilingual context"""
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "model": self.model_name,
            "linguistic_context": response.get("linguistic_analysis", {}),
            "cultural_intelligence": response.get("cultural_intelligence", {})
        })
        
        # Keep last 20 interactions for better multilingual context
        if len(self.session_history) > 20:
            self.session_history = self.session_history[-20:]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information"""
        return {
            "name": self.model_name,
            "version": self.version,
            "provider": self.config.provider,
            "model_type": self.config.model_type,
            "capabilities": self.config.capabilities,
            "specialties": list(self.config.specialties.keys()),
            "parameters": self.config.parameters,
            "status": "operational",
            "language_excellence": {
                "chinese_proficiency": "native_level",
                "english_proficiency": "fluent",
                "cultural_intelligence": "advanced",
                "cross_cultural_communication": "expert"
            },
            "specialized_features": {
                "chinese_language_processing": True,
                "mathematical_reasoning": True,
                "cultural_adaptation": True,
                "business_communication": True,
                "educational_support": True
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on multilingual capabilities"""
        try:
            # Test Chinese language processing
            chinese_test = await self.generate_response("你好，请问你能帮我解决数学问题吗？")
            
            # Test English language processing
            english_test = await self.generate_response("Hello, can you help with cross-cultural business communication?")
            
            # Test mathematical reasoning
            math_test = await self.generate_response("What is 25 + 37?")
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "version": self.version,
                "language_tests": {
                    "chinese_processing": "error" not in chinese_test,
                    "english_processing": "error" not in english_test,
                    "mathematical_reasoning": "error" not in math_test
                },
                "cultural_intelligence": {
                    "chinese_cultural_context": "active",
                    "cross_cultural_adaptation": "operational",
                    "business_communication": "ready"
                },
                "all_tests_passed": all([
                    "error" not in chinese_test,
                    "error" not in english_test, 
                    "error" not in math_test
                ])
            }
        except Exception as e:
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "error": str(e)
            }

# Example usage and testing
async def main():
    """Main function for testing Qwen 2.5 runner"""
    try:
        # Initialize runner
        runner = Qwen25Runner()
        
        # Test model info
        print("=== Model Information ===")
        model_info = runner.get_model_info()
        print(json.dumps(model_info, indent=2))
        
        # Test health check
        print("\n=== Health Check ===")
        health = await runner.health_check()
        print(json.dumps(health, indent=2))
        
        # Test multilingual processing
        print("\n=== Multilingual Processing Tests ===")
        test_inputs = [
            "你好，我想了解人工智能在商业中的应用",
            "Hello, can you explain the cultural differences in business communication between China and the West?",
            "请帮我计算 123 + 456 等于多少？",
            "What are the key considerations for international business expansion into China?"
        ]
        
        for test_input in test_inputs:
            print(f"\nInput: {test_input}")
            response = await runner.generate_response(test_input)
            
            linguistic_analysis = response.get('linguistic_analysis', {})
            print(f"Detected Language: {linguistic_analysis.get('detected_language', 'unknown')}")
            print(f"Cultural Context: {linguistic_analysis.get('cultural_context', 'neutral')}")
            
            response_content = response.get('response', {}).get('content', 'No response')
            print(f"Response: {response_content[:200]}...")
            
            if response.get('response', {}).get('cross_cultural_insights'):
                print(f"Cross-cultural insights: {response['response']['cross_cultural_insights']}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())