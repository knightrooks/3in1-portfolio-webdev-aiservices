#!/usr/bin/env python3
"""
Mistral Model Runner
Advanced Multilingual Processing with European Language Expertise
"""

import os
import json
import yaml
import requests
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import re
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MistralConfig:
    """Configuration class for Mistral model"""
    name: str
    version: str
    provider: str
    model_type: str
    parameters: Dict[str, Any]
    capabilities: Dict[str, List[str]]
    specialties: Dict[str, Dict[str, Any]]

class MistralRunner:
    """
    Runner class for Mistral multilingual processing model
    Handles multilingual content, European languages, and cross-cultural communication
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Mistral runner with configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.model_name = self.config.name
        self.version = self.config.version
        self.session_history = []
        self.language_context = {}
        self.cultural_context = {}
        
        # Initialize language processing capabilities
        self._init_language_processing()
        
        logger.info(f"Mistral Runner initialized: {self.model_name} v{self.version}")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "config.yaml")
    
    def _load_config(self) -> MistralConfig:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return MistralConfig(
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
    
    def _init_language_processing(self):
        """Initialize language processing capabilities"""
        try:
            # Language detection patterns
            self.language_patterns = {
                'french': {
                    'patterns': [r'\b(le|la|les|un|une|des|et|ou|mais|donc|car|à|de|du|dans|sur|avec|pour|par|sans|sous|vers|chez)\b'],
                    'confidence_threshold': 0.7
                },
                'spanish': {
                    'patterns': [r'\b(el|la|los|las|un|una|y|o|pero|que|de|del|en|con|por|para|sin|sobre|bajo|hacia|desde)\b'],
                    'confidence_threshold': 0.7
                },
                'german': {
                    'patterns': [r'\b(der|die|das|den|dem|des|ein|eine|eines|und|oder|aber|dass|von|mit|zu|für|auf|in|an|bei|nach)\b'],
                    'confidence_threshold': 0.7
                },
                'italian': {
                    'patterns': [r'\b(il|la|lo|gli|le|un|una|e|o|ma|che|di|del|in|con|per|da|su|tra|fra|verso|presso)\b'],
                    'confidence_threshold': 0.7
                },
                'portuguese': {
                    'patterns': [r'\b(o|a|os|as|um|uma|e|ou|mas|que|de|do|da|em|com|por|para|sem|sobre|sob|até|desde)\b'],
                    'confidence_threshold': 0.7
                }
            }
            
            # Cultural context markers
            self.cultural_markers = {
                'formal_tone': ['vous', 'usted', 'sie', 'lei', 'o senhor'],
                'informal_tone': ['tu', 'tú', 'du', 'tu', 'você'],
                'business_context': ['entreprise', 'empresa', 'unternehmen', 'azienda', 'negócio'],
                'academic_context': ['université', 'universidad', 'universität', 'università', 'universidade']
            }
            
            # Translation memory for common phrases
            self.translation_memory = {
                'hello': {
                    'french': 'Bonjour',
                    'spanish': 'Hola',
                    'german': 'Hallo',
                    'italian': 'Ciao',
                    'portuguese': 'Olá'
                },
                'thank_you': {
                    'french': 'Merci',
                    'spanish': 'Gracias',
                    'german': 'Danke',
                    'italian': 'Grazie',
                    'portuguese': 'Obrigado'
                },
                'please': {
                    'french': 'S\'il vous plaît',
                    'spanish': 'Por favor',
                    'german': 'Bitte',
                    'italian': 'Per favore',
                    'portuguese': 'Por favor'
                }
            }
            
            logger.info("Language processing capabilities initialized")
        except Exception as e:
            logger.error(f"Error initializing language processing: {e}")
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate multilingual response with cultural awareness
        
        Args:
            prompt: User input in any supported language
            context: Additional context including language preferences
        
        Returns:
            Dictionary containing the multilingual response
        """
        try:
            # Detect input language and cultural context
            language_analysis = await self._analyze_language_context(prompt, context)
            
            # Generate culturally appropriate response
            response = await self._generate_multilingual_response(prompt, language_analysis, context)
            
            # Format response with multilingual considerations
            formatted_response = await self._format_multilingual_response(response, language_analysis)
            
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
    
    async def _analyze_language_context(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze language and cultural context of the input"""
        analysis = {
            "detected_language": "english",
            "confidence": 0.5,
            "cultural_markers": [],
            "formality_level": "neutral",
            "domain": "general",
            "regional_variant": None,
            "translation_needed": False,
            "target_language": None
        }
        
        # Language detection
        prompt_lower = prompt.lower()
        language_scores = {}
        
        for language, config in self.language_patterns.items():
            score = 0
            for pattern in config['patterns']:
                matches = len(re.findall(pattern, prompt_lower, re.IGNORECASE))
                score += matches
            
            if score > 0:
                language_scores[language] = score / len(prompt.split())
        
        # Determine primary language
        if language_scores:
            detected_lang = max(language_scores.items(), key=lambda x: x[1])
            analysis["detected_language"] = detected_lang[0]
            analysis["confidence"] = min(1.0, detected_lang[1] * 2)  # Normalize confidence
        
        # Detect cultural markers
        for marker_type, markers in self.cultural_markers.items():
            for marker in markers:
                if marker.lower() in prompt_lower:
                    analysis["cultural_markers"].append(marker_type)
        
        # Determine formality level
        formal_indicators = ['vous', 'usted', 'sie', 'lei', 'monsieur', 'madame', 'señor', 'señora']
        informal_indicators = ['tu', 'tú', 'du', 'salut', 'hola', 'ciao']
        
        if any(indicator in prompt_lower for indicator in formal_indicators):
            analysis["formality_level"] = "formal"
        elif any(indicator in prompt_lower for indicator in informal_indicators):
            analysis["formality_level"] = "informal"
        
        # Extract context information
        if context:
            analysis["target_language"] = context.get("target_language")
            analysis["domain"] = context.get("domain", "general")
            analysis["regional_variant"] = context.get("regional_variant")
            
            if context.get("translate_to"):
                analysis["translation_needed"] = True
                analysis["target_language"] = context["translate_to"]
        
        return analysis
    
    async def _generate_multilingual_response(self, prompt: str, language_analysis: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response considering multilingual and cultural factors"""
        response = {
            "content": "",
            "language": language_analysis["detected_language"],
            "cultural_adaptations": [],
            "translation": None,
            "alternatives": [],
            "confidence": language_analysis["confidence"]
        }
        
        try:
            # Generate base response
            if language_analysis["detected_language"] == "french":
                response["content"] = await self._generate_french_response(prompt, language_analysis)
            elif language_analysis["detected_language"] == "spanish":
                response["content"] = await self._generate_spanish_response(prompt, language_analysis)
            elif language_analysis["detected_language"] == "german":
                response["content"] = await self._generate_german_response(prompt, language_analysis)
            elif language_analysis["detected_language"] == "italian":
                response["content"] = await self._generate_italian_response(prompt, language_analysis)
            elif language_analysis["detected_language"] == "portuguese":
                response["content"] = await self._generate_portuguese_response(prompt, language_analysis)
            else:
                response["content"] = await self._generate_english_response(prompt, language_analysis)
            
            # Add translation if needed
            if language_analysis["translation_needed"] and language_analysis["target_language"]:
                response["translation"] = await self._translate_response(
                    response["content"], 
                    language_analysis["detected_language"], 
                    language_analysis["target_language"]
                )
            
            # Generate cultural adaptations
            response["cultural_adaptations"] = await self._generate_cultural_adaptations(
                response["content"], language_analysis
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating multilingual response: {e}")
            response["error"] = str(e)
            return response
    
    async def _generate_french_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate French language response with cultural appropriateness"""
        base_response = "Bonjour! Je comprends votre question en français."
        
        # Adapt formality
        if analysis["formality_level"] == "formal":
            return f"Bonjour, je vous remercie pour votre question. {base_response} Je serais ravi de vous aider avec votre demande."
        else:
            return f"Salut! {base_response} Je peux t'aider avec ça!"
    
    async def _generate_spanish_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate Spanish language response with cultural appropriateness"""
        base_response = "¡Hola! Entiendo su pregunta en español."
        
        # Adapt formality
        if analysis["formality_level"] == "formal":
            return f"Buenos días, le agradezco su pregunta. {base_response} Estaré encantado de ayudarle."
        else:
            return f"¡Hola! {base_response} ¡Puedo ayudarte con eso!"
    
    async def _generate_german_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate German language response with cultural appropriateness"""
        base_response = "Hallo! Ich verstehe Ihre Frage auf Deutsch."
        
        # Adapt formality
        if analysis["formality_level"] == "formal":
            return f"Guten Tag, vielen Dank für Ihre Frage. {base_response} Ich helfe Ihnen gerne weiter."
        else:
            return f"Hi! {base_response} Ich kann dir dabei helfen!"
    
    async def _generate_italian_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate Italian language response with cultural appropriateness"""
        base_response = "Ciao! Capisco la tua domanda in italiano."
        
        # Adapt formality
        if analysis["formality_level"] == "formal":
            return f"Buongiorno, La ringrazio per la Sua domanda. {base_response} Sarò lieto di aiutarLa."
        else:
            return f"Ciao! {base_response} Posso aiutarti con questo!"
    
    async def _generate_portuguese_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate Portuguese language response with cultural appropriateness"""
        base_response = "Olá! Entendo sua pergunta em português."
        
        # Adapt formality
        if analysis["formality_level"] == "formal":
            return f"Bom dia, agradeço sua pergunta. {base_response} Ficarei feliz em ajudá-lo."
        else:
            return f"Oi! {base_response} Posso te ajudar com isso!"
    
    async def _generate_english_response(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Generate English language response as fallback"""
        return f"Hello! I understand your message. I specialize in multilingual communication and can help you with European languages including French, Spanish, German, Italian, and Portuguese. How can I assist you today?"
    
    async def _translate_response(self, content: str, source_lang: str, target_lang: str) -> str:
        """Translate response between supported languages"""
        try:
            # Simple translation logic (in production, would use advanced translation service)
            translation_mappings = {
                ('english', 'french'): "Voici la traduction en français de ma réponse.",
                ('english', 'spanish'): "Aquí está la traducción al español de mi respuesta.",
                ('english', 'german'): "Hier ist die deutsche Übersetzung meiner Antwort.",
                ('english', 'italian'): "Ecco la traduzione italiana della mia risposta.",
                ('english', 'portuguese'): "Aqui está a tradução em português da minha resposta.",
                ('french', 'english'): "Here is the English translation of my response.",
                ('spanish', 'english'): "Here is the English translation of my response.",
                ('german', 'english'): "Here is the English translation of my response.",
                ('italian', 'english'): "Here is the English translation of my response.",
                ('portuguese', 'english'): "Here is the English translation of my response."
            }
            
            translation_key = (source_lang, target_lang)
            if translation_key in translation_mappings:
                return translation_mappings[translation_key]
            else:
                return f"Translation from {source_lang} to {target_lang}: {content}"
                
        except Exception as e:
            logger.error(f"Error translating response: {e}")
            return f"Translation unavailable: {str(e)}"
    
    async def _generate_cultural_adaptations(self, content: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate cultural adaptation suggestions"""
        adaptations = []
        
        detected_lang = analysis["detected_language"]
        
        if detected_lang == "french":
            adaptations.extend([
                "Consider French cultural emphasis on formality in business contexts",
                "French communication tends to be more direct and intellectual",
                "Regional variations exist between France, Quebec, and African French"
            ])
        elif detected_lang == "spanish":
            adaptations.extend([
                "Spanish cultures value personal relationships in business",
                "Consider regional differences (Spain vs. Latin America)",
                "Formal address (usted) is important in professional settings"
            ])
        elif detected_lang == "german":
            adaptations.extend([
                "German business culture values punctuality and directness",
                "Formal titles and proper addressing are crucial",
                "Efficiency and thoroughness are highly appreciated"
            ])
        elif detected_lang == "italian":
            adaptations.extend([
                "Italian culture emphasizes relationship-building",
                "Regional variations are significant (North vs. South)",
                "Style and presentation are important considerations"
            ])
        elif detected_lang == "portuguese":
            adaptations.extend([
                "Consider differences between Brazilian and European Portuguese",
                "Personal relationships are central to business interactions",
                "Formal courtesy is valued in professional contexts"
            ])
        
        # Add formality adaptations
        if analysis["formality_level"] == "formal":
            adaptations.append("Maintain formal register throughout the interaction")
        elif analysis["formality_level"] == "informal":
            adaptations.append("Casual tone is appropriate for this context")
        
        return adaptations[:3]  # Return top 3 most relevant adaptations
    
    async def _format_multilingual_response(self, response: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Format the multilingual response with comprehensive information"""
        formatted_response = {
            "model": self.model_name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "language_analysis": analysis,
            "response": response,
            "multilingual_features": {
                "primary_language": response["language"],
                "cultural_awareness": len(response["cultural_adaptations"]) > 0,
                "translation_available": response["translation"] is not None,
                "formality_adapted": analysis["formality_level"] != "neutral"
            },
            "recommendations": self._generate_multilingual_recommendations(analysis, response),
            "confidence": response["confidence"]
        }
        
        return formatted_response
    
    def _generate_multilingual_recommendations(self, analysis: Dict[str, Any], response: Dict[str, Any]) -> List[str]:
        """Generate recommendations for multilingual communication"""
        recommendations = []
        
        detected_lang = analysis["detected_language"]
        
        if detected_lang != "english":
            recommendations.append(f"Continue conversation in {detected_lang} for better cultural connection")
        
        if analysis["confidence"] < 0.7:
            recommendations.append("Language detection confidence is low - consider clarifying the preferred language")
        
        if response["cultural_adaptations"]:
            recommendations.append("Cultural adaptations have been applied - review for appropriateness")
        
        if analysis["formality_level"] == "neutral":
            recommendations.append("Consider establishing appropriate formality level for better communication")
        
        return recommendations[:3]
    
    def _update_session_history(self, prompt: str, response: Dict[str, Any]):
        """Update session history with multilingual context"""
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "model": self.model_name,
            "language_context": response.get("language_analysis", {}),
            "multilingual_features": response.get("multilingual_features", {})
        })
        
        # Keep only last 15 interactions (more for multilingual context)
        if len(self.session_history) > 15:
            self.session_history = self.session_history[-15:]
    
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
            "supported_languages": list(self.language_patterns.keys()) + ["english"],
            "cultural_awareness": True,
            "translation_capabilities": True,
            "formality_adaptation": True
        }
    
    def get_supported_languages(self) -> Dict[str, Any]:
        """Get detailed information about supported languages"""
        return {
            "primary_languages": {
                "french": {
                    "proficiency": "native",
                    "cultural_contexts": ["France", "Quebec", "African French"],
                    "business_communication": "formal_emphasis"
                },
                "spanish": {
                    "proficiency": "native", 
                    "cultural_contexts": ["Spain", "Latin America"],
                    "business_communication": "relationship_focused"
                },
                "german": {
                    "proficiency": "native",
                    "cultural_contexts": ["Germany", "Austria", "Switzerland"],
                    "business_communication": "direct_formal"
                },
                "italian": {
                    "proficiency": "native",
                    "cultural_contexts": ["Italy", "Regional variations"],
                    "business_communication": "style_conscious"
                },
                "portuguese": {
                    "proficiency": "native",
                    "cultural_contexts": ["Brazil", "Portugal"],
                    "business_communication": "relationship_centered"
                },
                "english": {
                    "proficiency": "native",
                    "cultural_contexts": ["Global", "Business standard"],
                    "business_communication": "versatile"
                }
            },
            "translation_pairs": [
                "english ↔ french", "english ↔ spanish", "english ↔ german",
                "english ↔ italian", "english ↔ portuguese",
                "french ↔ spanish", "spanish ↔ italian", "german ↔ french"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the multilingual model"""
        try:
            # Test multilingual capabilities
            test_phrases = {
                "french": "Bonjour, comment allez-vous?",
                "spanish": "Hola, ¿cómo está usted?",
                "german": "Guten Tag, wie geht es Ihnen?",
                "italian": "Buongiorno, come sta?",
                "portuguese": "Bom dia, como está?"
            }
            
            test_results = {}
            for lang, phrase in test_phrases.items():
                result = await self.generate_response(phrase)
                test_results[lang] = "error" not in result
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "version": self.version,
                "language_tests": test_results,
                "all_tests_passed": all(test_results.values()),
                "multilingual_processing": "operational",
                "cultural_adaptation": "active"
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
    """Main function for testing Mistral runner"""
    try:
        # Initialize runner
        runner = MistralRunner()
        
        # Test model info
        print("=== Model Information ===")
        model_info = runner.get_model_info()
        print(json.dumps(model_info, indent=2))
        
        # Test supported languages
        print("\n=== Supported Languages ===")
        languages = runner.get_supported_languages()
        print(json.dumps(languages, indent=2))
        
        # Test health check
        print("\n=== Health Check ===")
        health = await runner.health_check()
        print(json.dumps(health, indent=2))
        
        # Test multilingual processing
        print("\n=== Multilingual Processing Tests ===")
        test_inputs = [
            "Bonjour, comment puis-je vous aider?",
            "Hola, ¿cómo puedo ayudarle?",
            "Hallo, wie kann ich Ihnen helfen?",
            "Ciao, come posso aiutarla?",
            "Olá, como posso ajudá-lo?"
        ]
        
        for test_input in test_inputs:
            print(f"\nInput: {test_input}")
            response = await runner.generate_response(test_input)
            lang_analysis = response.get('language_analysis', {})
            print(f"Detected Language: {lang_analysis.get('detected_language', 'unknown')}")
            print(f"Confidence: {lang_analysis.get('confidence', 0):.2f}")
            print(f"Response: {response.get('response', {}).get('content', 'No response')}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())