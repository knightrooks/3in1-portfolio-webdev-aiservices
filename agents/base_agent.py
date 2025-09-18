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
import json
import base64
from io import BytesIO
import tempfile

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
        
        # Voice configuration
        self.voice_config = config.get("voice_config", {})
        self.voice_enabled = self.voice_config.get("enabled", False)
        self.tts_engine = None

        # Agent state
        self.session_data = {}
        self.conversation_history = []
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 0.0,
            "average_response_time": 0.0,
            "user_satisfaction": 0.0,
            "voice_requests": 0,
            "voice_success_rate": 0.0,
        }

        logger.info(f"Initialized {self.__class__.__name__}: {self.name}")
        
        # Initialize voice if enabled
        if self.voice_enabled:
            asyncio.create_task(self._initialize_voice())

    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request and return response"""
        pass

    @abstractmethod
    async def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        pass

    # Voice Functionality Methods
    async def _initialize_voice(self):
        """Initialize TTS engine based on configuration"""
        try:
            if not self.voice_enabled:
                return False

            tts_provider = self.voice_config.get("provider", "gTTS")
            
            if tts_provider == "gTTS":
                await self._initialize_gtts()
            elif tts_provider == "pyttsx3":
                await self._initialize_pyttsx3()
            elif tts_provider == "azure":
                await self._initialize_azure_tts()
            else:
                logger.warning(f"Unknown TTS provider: {tts_provider}")
                return False

            logger.info(f"Voice initialized for {self.name} using {tts_provider}")
            return True

        except Exception as e:
            logger.error(f"Error initializing voice for {self.name}: {e}")
            self.voice_enabled = False
            return False

    async def _initialize_gtts(self):
        """Initialize Google TTS"""
        try:
            from gtts import gTTS
            self.tts_engine = "gTTS"
            return True
        except ImportError:
            logger.error("gTTS not available. Install with: pip install gTTS")
            return False

    async def _initialize_pyttsx3(self):
        """Initialize pyttsx3 TTS"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Configure voice based on personality
            voice_props = self._get_voice_properties()
            self.tts_engine.setProperty('rate', voice_props['rate'])
            self.tts_engine.setProperty('volume', voice_props['volume'])
            
            # Try to set voice gender/type if available
            voices = self.tts_engine.getProperty('voices')
            if voices and voice_props.get('gender'):
                for voice in voices:
                    if voice_props['gender'].lower() in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            return True
        except ImportError:
            logger.error("pyttsx3 not available. Install with: pip install pyttsx3")
            return False

    async def _initialize_azure_tts(self):
        """Initialize Azure Cognitive Services TTS"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_key = os.getenv("AZURE_SPEECH_KEY")
            service_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
            
            if not speech_key:
                logger.error("Azure Speech key not found in environment variables")
                return False

            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            speech_config.speech_synthesis_voice_name = self._get_azure_voice_name()
            
            self.tts_engine = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            return True
        except ImportError:
            logger.error("Azure Speech SDK not available. Install with: pip install azure-cognitiveservices-speech")
            return False

    def _get_voice_properties(self) -> Dict[str, Any]:
        """Get voice properties based on agent personality"""
        # Default properties
        props = {
            'rate': 200,  # words per minute
            'volume': 0.8,
            'gender': 'neutral'
        }
        
        # Customize based on agent personality
        personality = self.persona.get('personality', {})
        agent_name = self.name.lower()
        
        # Agent-specific voice characteristics
        if 'emotional' in agent_name or 'jenny' in agent_name:
            props.update({
                'rate': 180,
                'volume': 0.9,
                'gender': 'female',
                'tone': 'warm',
                'emotion': 'empathetic'
            })
        elif 'strict' in agent_name or 'wife' in agent_name:
            props.update({
                'rate': 160,
                'volume': 0.95,
                'gender': 'female',
                'tone': 'authoritative',
                'emotion': 'stern'
            })
        elif 'gossip' in agent_name or 'queen' in agent_name:
            props.update({
                'rate': 220,
                'volume': 0.9,
                'gender': 'female',
                'tone': 'animated',
                'emotion': 'excited'
            })
        elif 'lazy' in agent_name or 'john' in agent_name:
            props.update({
                'rate': 140,
                'volume': 0.7,
                'gender': 'male',
                'tone': 'monotone',
                'emotion': 'casual'
            })
        elif 'girlfriend' in agent_name:
            props.update({
                'rate': 190,
                'volume': 0.85,
                'gender': 'female',
                'tone': 'sweet',
                'emotion': 'affectionate'
            })
        elif 'coder' in agent_name or 'developer' in agent_name:
            props.update({
                'rate': 170,
                'volume': 0.8,
                'gender': 'neutral',
                'tone': 'technical',
                'emotion': 'focused'
            })
        elif 'strategist' in agent_name:
            props.update({
                'rate': 160,
                'volume': 0.85,
                'gender': 'neutral',
                'tone': 'analytical',
                'emotion': 'confident'
            })
        elif 'security' in agent_name:
            props.update({
                'rate': 150,
                'volume': 0.9,
                'gender': 'male',
                'tone': 'serious',
                'emotion': 'vigilant'
            })

        # Override with config if present
        props.update(self.voice_config.get('properties', {}))
        
        return props

    def _get_azure_voice_name(self) -> str:
        """Get Azure voice name based on agent personality"""
        voice_props = self._get_voice_properties()
        
        # Map personality to Azure voices
        voice_mapping = {
            ('female', 'warm'): "en-US-AriaNeural",
            ('female', 'authoritative'): "en-US-SaraNeural", 
            ('female', 'animated'): "en-US-JennyNeural",
            ('female', 'sweet'): "en-US-MichelleNeural",
            ('male', 'monotone'): "en-US-GuyNeural",
            ('male', 'serious'): "en-US-DavisNeural",
            ('neutral', 'technical'): "en-US-BrianNeural",
            ('neutral', 'analytical'): "en-US-RogerNeural"
        }
        
        key = (voice_props.get('gender', 'neutral'), voice_props.get('tone', 'neutral'))
        return voice_mapping.get(key, "en-US-AriaNeural")

    async def text_to_speech(self, text: str, format: str = "audio/mp3") -> Optional[bytes]:
        """Convert text to speech audio"""
        if not self.voice_enabled or not text:
            return None

        try:
            self.performance_metrics["voice_requests"] += 1
            
            if self.tts_engine == "gTTS":
                return await self._gtts_synthesize(text, format)
            elif hasattr(self.tts_engine, 'say'):  # pyttsx3
                return await self._pyttsx3_synthesize(text, format)
            elif hasattr(self.tts_engine, 'speak_text_async'):  # Azure
                return await self._azure_synthesize(text, format)
            else:
                logger.error(f"Unknown TTS engine type: {type(self.tts_engine)}")
                return None

        except Exception as e:
            logger.error(f"Error in text-to-speech for {self.name}: {e}")
            return None

    async def _gtts_synthesize(self, text: str, format: str) -> bytes:
        """Synthesize speech using gTTS"""
        from gtts import gTTS
        
        # Apply personality-based language and accent
        voice_props = self._get_voice_properties()
        lang = voice_props.get('language', 'en')
        
        # Add personality-specific text modifications
        text = self._apply_personality_to_text(text)
        
        tts = gTTS(text=text, lang=lang, slow=False)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts.save(temp_file.name)
            with open(temp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
            os.unlink(temp_file.name)
            
        return audio_data

    async def _pyttsx3_synthesize(self, text: str, format: str) -> bytes:
        """Synthesize speech using pyttsx3"""
        text = self._apply_personality_to_text(text)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            self.tts_engine.save_to_file(text, temp_file.name)
            self.tts_engine.runAndWait()
            
            with open(temp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
            os.unlink(temp_file.name)
            
        return audio_data

    async def _azure_synthesize(self, text: str, format: str) -> bytes:
        """Synthesize speech using Azure Cognitive Services"""
        text = self._apply_personality_to_text(text)
        
        result = self.tts_engine.speak_text_async(text).get()
        
        if result.reason == result.reason.SynthesizingAudioCompleted:
            return result.audio_data
        else:
            logger.error(f"Azure TTS failed: {result.reason}")
            return None

    def _apply_personality_to_text(self, text: str) -> str:
        """Apply personality-specific modifications to text before TTS"""
        agent_name = self.name.lower()
        
        # Agent-specific text modifications
        if 'emotional' in agent_name or 'jenny' in agent_name:
            # Add emotional warmth
            if not any(word in text.lower() for word in ['honey', 'dear', 'sweetie']):
                text = f"Oh, {text}"
                
        elif 'strict' in agent_name or 'wife' in agent_name:
            # Add authoritative tone
            text = text.replace('maybe', 'definitely')
            text = text.replace('might', 'will')
            if '?' in text:
                text = text.replace('?', '!')
                
        elif 'gossip' in agent_name or 'queen' in agent_name:
            # Add excitement and emphasis
            text = text.replace('.', '!')
            if not text.startswith(('Oh my', 'Girl', 'Honey')):
                text = f"Oh my gosh, {text.lower()}"
                
        elif 'lazy' in agent_name or 'john' in agent_name:
            # Add casual, laid-back tone
            text = text.replace('!', '.')
            text = text.replace('very', 'kinda')
            if not text.lower().startswith(('yeah', 'well', 'uhh')):
                text = f"Yeah, {text.lower()}"
                
        elif 'girlfriend' in agent_name:
            # Add affectionate tone
            if not any(word in text.lower() for word in ['babe', 'baby', 'love']):
                text = f"Hey babe, {text}"

        return text

    async def get_voice_capabilities(self) -> Dict[str, Any]:
        """Get voice-specific capabilities and status"""
        return {
            "voice_enabled": self.voice_enabled,
            "tts_provider": self.voice_config.get("provider", "none"),
            "voice_properties": self._get_voice_properties() if self.voice_enabled else {},
            "supported_formats": ["audio/mp3", "audio/wav"] if self.voice_enabled else [],
            "personality_voice_active": self.voice_enabled and bool(self.persona),
            "voice_metrics": {
                "total_voice_requests": self.performance_metrics.get("voice_requests", 0),
                "voice_success_rate": self.performance_metrics.get("voice_success_rate", 0.0)
            }
        }

    async def speak_response(self, response_text: str, include_audio: bool = True) -> Dict[str, Any]:
        """Generate both text and audio response"""
        result = {
            "text": response_text,
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "voice_enabled": self.voice_enabled
        }
        
        if include_audio and self.voice_enabled:
            try:
                audio_data = await self.text_to_speech(response_text)
                if audio_data:
                    # Convert to base64 for JSON serialization
                    result["audio"] = base64.b64encode(audio_data).decode('utf-8')
                    result["audio_format"] = "audio/mp3"
                    result["audio_size"] = len(audio_data)
                    
                    # Update success metrics
                    current_requests = self.performance_metrics["voice_requests"]
                    current_success_rate = self.performance_metrics.get("voice_success_rate", 0.0)
                    self.performance_metrics["voice_success_rate"] = (
                        current_success_rate * (current_requests - 1) + 1.0
                    ) / current_requests
                else:
                    result["audio_error"] = "Failed to generate audio"
                    
            except Exception as e:
                result["audio_error"] = str(e)
                logger.error(f"Error generating audio for {self.name}: {e}")
        
        return result

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
            "voice_capabilities": self.get_voice_capabilities() if hasattr(self, 'get_voice_capabilities') else {}
        }
