#!/usr/bin/env python3
"""
Yi Model Runner
Advanced Conversational AI with Emotional Intelligence and Cultural Sensitivity
"""

import os
import json
import yaml
import asyncio
import logging
import re
import time
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class YiConfig:
    """Configuration class for Yi model"""
    name: str
    version: str
    provider: str
    model_type: str
    parameters: Dict[str, Any]
    capabilities: Dict[str, List[str]]
    specialties: Dict[str, Dict[str, Any]]

class EmotionAnalyzer:
    """Advanced emotion detection and analysis system"""
    
    def __init__(self):
        # Emotion lexicons and patterns
        self.emotion_patterns = {
            'joy': [
                r'\b(happy|joy|excited|thrilled|delighted|cheerful|elated|euphoric)\b',
                r'\b(amazing|wonderful|fantastic|excellent|brilliant|awesome)\b',
                r'[!]{2,}|😊|😄|😁|🎉|✨|❤️'
            ],
            'sadness': [
                r'\b(sad|depressed|down|blue|miserable|heartbroken|devastated)\b',
                r'\b(terrible|awful|horrible|disappointing|tragic)\b',
                r'😢|😭|💔|😞'
            ],
            'anger': [
                r'\b(angry|furious|mad|irritated|annoyed|frustrated|outraged)\b',
                r'\b(hate|disgusting|ridiculous|stupid|terrible)\b',
                r'😡|🤬|😠|💢'
            ],
            'fear': [
                r'\b(scared|afraid|terrified|anxious|worried|nervous|panic)\b',
                r'\b(dangerous|risky|threatening|concerning)\b',
                r'😰|😨|😱|😳'
            ],
            'surprise': [
                r'\b(surprised|amazed|shocked|astonished|stunned|bewildered)\b',
                r'\b(unexpected|sudden|incredible|unbelievable)\b',
                r'😲|😮|🤯|😯'
            ],
            'disgust': [
                r'\b(disgusting|gross|revolting|repulsive|sickening)\b',
                r'\b(yuck|ew|horrible|awful)\b',
                r'🤢|🤮|😷'
            ],
            'trust': [
                r'\b(trust|reliable|confident|secure|comfortable|assured)\b',
                r'\b(believe|faith|dependable|loyal)\b',
                r'🤝|💪|👍'
            ],
            'anticipation': [
                r'\b(excited|eager|hopeful|looking forward|anticipating)\b',
                r'\b(upcoming|future|planning|expecting)\b',
                r'🤔|⏰|🔮'
            ]
        }
        
        self.intensity_modifiers = {
            'high': [r'\bvery\b', r'\bextremely\b', r'\bincredibly\b', r'\btremendously\b', r'[!]{2,}'],
            'medium': [r'\bquite\b', r'\bpretty\b', r'\bfairly\b', r'\bsomewhat\b'],
            'low': [r'\ba bit\b', r'\bslightly\b', r'\ba little\b', r'\bmildly\b']
        }
    
    def analyze_emotions(self, text: str) -> Dict[str, Any]:
        """Analyze emotions in text with intensity scoring"""
        text_lower = text.lower()
        emotion_scores = {}
        emotion_details = {}
        
        # Detect emotions and their intensities
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            matches = []
            
            for pattern in patterns:
                pattern_matches = re.findall(pattern, text_lower, re.IGNORECASE)
                matches.extend(pattern_matches)
                score += len(pattern_matches)
            
            if score > 0:
                # Apply intensity modifiers
                intensity = self._calculate_intensity(text_lower, matches)
                emotion_scores[emotion] = score * intensity
                emotion_details[emotion] = {
                    'base_score': score,
                    'intensity_multiplier': intensity,
                    'matches': matches[:5]  # Limit to first 5 matches
                }
        
        # Normalize scores
        if emotion_scores:
            max_score = max(emotion_scores.values())
            emotion_scores = {k: v/max_score for k, v in emotion_scores.items()}
        
        # Determine dominant emotions
        dominant_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'emotion_scores': emotion_scores,
            'dominant_emotions': [{'emotion': e, 'score': s} for e, s in dominant_emotions],
            'emotion_details': emotion_details,
            'emotional_complexity': len(emotion_scores),
            'overall_sentiment': self._determine_overall_sentiment(emotion_scores)
        }
    
    def _calculate_intensity(self, text: str, emotion_matches: List[str]) -> float:
        """Calculate emotional intensity based on modifiers"""
        base_intensity = 1.0
        
        # Check for intensity modifiers near emotion words
        for intensity_level, modifiers in self.intensity_modifiers.items():
            for modifier_pattern in modifiers:
                if re.search(modifier_pattern, text):
                    if intensity_level == 'high':
                        base_intensity *= 1.5
                    elif intensity_level == 'medium':
                        base_intensity *= 1.2
                    elif intensity_level == 'low':
                        base_intensity *= 0.8
                    break
        
        return min(2.0, base_intensity)  # Cap at 2.0
    
    def _determine_overall_sentiment(self, emotion_scores: Dict[str, float]) -> str:
        """Determine overall emotional sentiment"""
        if not emotion_scores:
            return 'neutral'
        
        positive_emotions = ['joy', 'trust', 'anticipation']
        negative_emotions = ['sadness', 'anger', 'fear', 'disgust']
        
        positive_score = sum(emotion_scores.get(e, 0) for e in positive_emotions)
        negative_score = sum(emotion_scores.get(e, 0) for e in negative_emotions)
        
        if positive_score > negative_score * 1.2:
            return 'positive'
        elif negative_score > positive_score * 1.2:
            return 'negative'
        else:
            return 'mixed'

class CulturalAdaptationEngine:
    """Cultural sensitivity and adaptation system"""
    
    def __init__(self):
        # Cultural communication patterns
        self.cultural_markers = {
            'western': {
                'directness': 0.8,
                'individualism': 0.9,
                'formality_preference': 0.4,
                'time_orientation': 'monochronic',
                'communication_style': 'low_context'
            },
            'eastern': {
                'directness': 0.3,
                'individualism': 0.2,
                'formality_preference': 0.8,
                'time_orientation': 'polychronic',
                'communication_style': 'high_context'
            },
            'latin': {
                'directness': 0.6,
                'individualism': 0.5,
                'formality_preference': 0.6,
                'time_orientation': 'polychronic',
                'communication_style': 'medium_context'
            },
            'arabic': {
                'directness': 0.4,
                'individualism': 0.3,
                'formality_preference': 0.9,
                'time_orientation': 'polychronic',
                'communication_style': 'high_context'
            }
        }
        
        self.formality_indicators = {
            'formal': [
                r'\b(please|kindly|would you|could you|sir|madam|mr|ms|dr)\b',
                r'\b(respectfully|sincerely|cordially)\b'
            ],
            'informal': [
                r'\b(hey|hi|yeah|yep|cool|awesome|gonna|wanna)\b',
                r'[!]{1}(?![!])|😊|👍'
            ]
        }
    
    def detect_cultural_context(self, text: str, user_profile: Dict = None) -> Dict[str, Any]:
        """Detect cultural context from text and user profile"""
        text_lower = text.lower()
        
        # Analyze formality level
        formality_score = self._analyze_formality(text_lower)
        
        # Detect communication patterns
        communication_patterns = self._detect_communication_patterns(text_lower)
        
        # Apply user profile if available
        cultural_bias = 'western'  # Default
        if user_profile and 'cultural_background' in user_profile:
            cultural_bias = user_profile['cultural_background']
        
        cultural_traits = self.cultural_markers.get(cultural_bias, self.cultural_markers['western'])
        
        return {
            'formality_level': formality_score,
            'detected_culture': cultural_bias,
            'cultural_traits': cultural_traits,
            'communication_patterns': communication_patterns,
            'adaptation_suggestions': self._generate_adaptation_suggestions(
                formality_score, cultural_traits, communication_patterns
            )
        }
    
    def _analyze_formality(self, text: str) -> Dict[str, Any]:
        """Analyze formality level in text"""
        formal_count = 0
        informal_count = 0
        
        for pattern in self.formality_indicators['formal']:
            formal_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        for pattern in self.formality_indicators['informal']:
            informal_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        total_indicators = formal_count + informal_count
        if total_indicators == 0:
            formality_ratio = 0.5  # Neutral
        else:
            formality_ratio = formal_count / total_indicators
        
        return {
            'ratio': formality_ratio,
            'level': 'formal' if formality_ratio > 0.6 else 'informal' if formality_ratio < 0.4 else 'neutral',
            'formal_indicators': formal_count,
            'informal_indicators': informal_count
        }
    
    def _detect_communication_patterns(self, text: str) -> Dict[str, Any]:
        """Detect communication style patterns"""
        # Analyze directness
        direct_patterns = [
            r'\b(I want|I need|give me|tell me|do this)\b',
            r'\b(no|yes|absolutely|definitely|never|always)\b'
        ]
        
        indirect_patterns = [
            r'\b(perhaps|maybe|might|could|would it be possible)\b',
            r'\b(I was wondering|I hope|if you don\'t mind)\b'
        ]
        
        direct_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in direct_patterns)
        indirect_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in indirect_patterns)
        
        total_patterns = direct_count + indirect_count
        directness = direct_count / max(1, total_patterns)
        
        return {
            'directness': directness,
            'communication_style': 'direct' if directness > 0.6 else 'indirect' if directness < 0.4 else 'balanced',
            'context_richness': self._analyze_context_richness(text)
        }
    
    def _analyze_context_richness(self, text: str) -> str:
        """Analyze how context-rich the communication is"""
        # High-context indicators: implicit meanings, relationships, background
        # Low-context indicators: explicit statements, direct information
        
        high_context_indicators = [
            r'\b(as you know|obviously|of course|naturally)\b',
            r'\b(family|relationship|tradition|history)\b'
        ]
        
        low_context_indicators = [
            r'\b(specifically|exactly|clearly|precisely)\b',
            r'\b(first|second|then|finally|in conclusion)\b'
        ]
        
        high_context_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in high_context_indicators)
        low_context_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in low_context_indicators)
        
        if high_context_count > low_context_count:
            return 'high_context'
        elif low_context_count > high_context_count:
            return 'low_context'
        else:
            return 'medium_context'
    
    def _generate_adaptation_suggestions(self, formality_score: Dict, cultural_traits: Dict, 
                                       communication_patterns: Dict) -> List[str]:
        """Generate suggestions for cultural adaptation"""
        suggestions = []
        
        # Formality suggestions
        if formality_score['ratio'] < cultural_traits['formality_preference']:
            suggestions.append("Consider using more formal language and respectful expressions")
        elif formality_score['ratio'] > cultural_traits['formality_preference'] + 0.3:
            suggestions.append("A more casual tone might be more appropriate")
        
        # Directness suggestions
        if communication_patterns['directness'] < cultural_traits['directness'] - 0.2:
            suggestions.append("More direct communication might be preferred")
        elif communication_patterns['directness'] > cultural_traits['directness'] + 0.2:
            suggestions.append("Consider a more indirect, diplomatic approach")
        
        # Context suggestions
        if cultural_traits['communication_style'] == 'high_context':
            suggestions.append("Include more background context and relationship-building elements")
        elif cultural_traits['communication_style'] == 'low_context':
            suggestions.append("Be more explicit and provide clear, detailed information")
        
        return suggestions[:3]  # Limit to top 3 suggestions

class ConversationMemory:
    """Advanced conversation memory and context management"""
    
    def __init__(self):
        self.conversations = {}
        self.user_profiles = {}
        self.conversation_history = defaultdict(list)
        self.emotional_tracking = defaultdict(list)
        
    def add_conversation_turn(self, user_id: str, user_input: str, 
                            assistant_response: str, emotion_analysis: Dict,
                            cultural_context: Dict):
        """Add a conversation turn to memory"""
        timestamp = datetime.now()
        
        conversation_entry = {
            'timestamp': timestamp.isoformat(),
            'user_input': user_input,
            'assistant_response': assistant_response,
            'emotion_analysis': emotion_analysis,
            'cultural_context': cultural_context,
            'turn_id': len(self.conversation_history[user_id]) + 1
        }
        
        self.conversation_history[user_id].append(conversation_entry)
        
        # Track emotional progression
        if emotion_analysis.get('dominant_emotions'):
            self.emotional_tracking[user_id].append({
                'timestamp': timestamp.isoformat(),
                'emotions': emotion_analysis['dominant_emotions'],
                'sentiment': emotion_analysis.get('overall_sentiment', 'neutral')
            })
        
        # Update user profile
        self._update_user_profile(user_id, conversation_entry)
    
    def get_conversation_context(self, user_id: str, max_turns: int = 10) -> Dict[str, Any]:
        """Get recent conversation context"""
        recent_conversations = self.conversation_history[user_id][-max_turns:]
        
        # Analyze conversation patterns
        emotion_trends = self._analyze_emotion_trends(user_id)
        communication_style = self._analyze_communication_style(user_id)
        
        return {
            'recent_conversations': recent_conversations,
            'conversation_count': len(self.conversation_history[user_id]),
            'emotion_trends': emotion_trends,
            'communication_style': communication_style,
            'user_profile': self.user_profiles.get(user_id, {}),
            'relationship_duration': self._calculate_relationship_duration(user_id)
        }
    
    def _update_user_profile(self, user_id: str, conversation_entry: Dict):
        """Update user profile based on conversation"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'preferences': {},
                'communication_style': {},
                'topics_of_interest': [],
                'emotional_patterns': {},
                'cultural_markers': {}
            }
        
        profile = self.user_profiles[user_id]
        
        # Update communication style preferences
        cultural_context = conversation_entry['cultural_context']
        if 'formality_level' in cultural_context:
            profile['communication_style']['preferred_formality'] = cultural_context['formality_level']['level']
        
        # Track topics of interest (simple keyword extraction)
        user_input = conversation_entry['user_input'].lower()
        keywords = re.findall(r'\b\w{4,}\b', user_input)
        for keyword in keywords[:5]:  # Limit to prevent bloat
            if keyword not in profile['topics_of_interest']:
                profile['topics_of_interest'].append(keyword)
        
        # Keep only recent topics (last 20)
        profile['topics_of_interest'] = profile['topics_of_interest'][-20:]
    
    def _analyze_emotion_trends(self, user_id: str) -> Dict[str, Any]:
        """Analyze emotional trends over time"""
        emotional_history = self.emotional_tracking[user_id]
        
        if not emotional_history:
            return {'trend': 'no_data', 'stability': 'unknown'}
        
        # Analyze recent emotions
        recent_emotions = emotional_history[-10:]  # Last 10 emotional states
        
        # Calculate emotional stability
        sentiments = [entry['sentiment'] for entry in recent_emotions]
        sentiment_changes = sum(1 for i in range(1, len(sentiments)) if sentiments[i] != sentiments[i-1])
        stability = 'stable' if sentiment_changes <= 2 else 'variable' if sentiment_changes <= 4 else 'volatile'
        
        # Determine overall trend
        if len(recent_emotions) >= 3:
            early_sentiment = recent_emotions[:len(recent_emotions)//2]
            late_sentiment = recent_emotions[len(recent_emotions)//2:]
            
            early_positive = sum(1 for entry in early_sentiment if entry['sentiment'] == 'positive')
            late_positive = sum(1 for entry in late_sentiment if entry['sentiment'] == 'positive')
            
            if late_positive > early_positive:
                trend = 'improving'
            elif late_positive < early_positive:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'trend': trend,
            'stability': stability,
            'recent_sentiment': sentiments[-1] if sentiments else 'unknown',
            'session_length': len(emotional_history)
        }
    
    def _analyze_communication_style(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's communication style patterns"""
        conversations = self.conversation_history[user_id]
        
        if not conversations:
            return {'style': 'unknown'}
        
        # Analyze average message length
        message_lengths = [len(conv['user_input'].split()) for conv in conversations]
        avg_length = sum(message_lengths) / len(message_lengths)
        
        # Analyze question patterns
        questions = sum(1 for conv in conversations if '?' in conv['user_input'])
        question_ratio = questions / len(conversations)
        
        # Determine communication style
        if avg_length > 20 and question_ratio < 0.3:
            style = 'detailed_declarative'
        elif avg_length < 10 and question_ratio > 0.6:
            style = 'brief_inquisitive'
        elif avg_length > 15:
            style = 'elaborative'
        elif question_ratio > 0.4:
            style = 'question_focused'
        else:
            style = 'balanced'
        
        return {
            'style': style,
            'avg_message_length': round(avg_length, 1),
            'question_ratio': round(question_ratio, 2),
            'total_interactions': len(conversations)
        }
    
    def _calculate_relationship_duration(self, user_id: str) -> Dict[str, Any]:
        """Calculate relationship duration and interaction patterns"""
        conversations = self.conversation_history[user_id]
        
        if not conversations:
            return {'duration': 'no_history'}
        
        first_conversation = datetime.fromisoformat(conversations[0]['timestamp'])
        last_conversation = datetime.fromisoformat(conversations[-1]['timestamp'])
        duration = last_conversation - first_conversation
        
        return {
            'total_duration_days': duration.days,
            'total_interactions': len(conversations),
            'first_interaction': first_conversation.isoformat(),
            'last_interaction': last_conversation.isoformat(),
            'relationship_stage': self._determine_relationship_stage(duration.days, len(conversations))
        }
    
    def _determine_relationship_stage(self, days: int, interactions: int) -> str:
        """Determine relationship stage based on duration and interactions"""
        if days == 0:
            return 'first_meeting'
        elif days < 7 and interactions < 10:
            return 'getting_acquainted'
        elif days < 30 and interactions < 50:
            return 'building_rapport'
        elif interactions > 100:
            return 'established_relationship'
        else:
            return 'regular_interaction'

class YiRunner:
    """
    Runner class for Yi model
    Advanced conversational AI with emotional intelligence and cultural sensitivity
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the Yi runner with configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.model_name = self.config.name
        self.version = self.config.version
        
        # Initialize specialized components
        self.emotion_analyzer = EmotionAnalyzer()
        self.cultural_engine = CulturalAdaptationEngine()
        self.conversation_memory = ConversationMemory()
        
        # Conversation parameters
        self.max_context_length = self.config.parameters.get("max_context_length", 8192)
        self.temperature = self.config.parameters.get("temperature", 0.7)
        self.empathy_factor = self.config.parameters.get("empathy_factor", 0.8)
        
        # Performance tracking
        self.session_history = []
        self.performance_metrics = {
            "conversations_handled": 0,
            "average_response_time": 0.0,
            "emotional_accuracy_feedback": [],
            "cultural_adaptation_success": 0
        }
        
        logger.info(f"Yi Runner initialized: {self.model_name} v{self.version}")
        logger.info(f"Emotional intelligence: Active, Cultural adaptation: Enabled")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "config.yaml")
    
    def _load_config(self) -> YiConfig:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            return YiConfig(
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
    
    async def generate_response(self, user_input: str, user_id: str = "default_user", 
                               user_profile: Dict = None, context: Dict = None) -> Dict[str, Any]:
        """
        Generate emotionally intelligent and culturally sensitive response
        
        Args:
            user_input: User's input message
            user_id: Unique user identifier for conversation tracking
            user_profile: Optional user profile information
            context: Additional context information
        
        Returns:
            Dictionary containing response and comprehensive analysis
        """
        start_time = time.time()
        
        try:
            # Analyze emotional content
            emotion_analysis = self.emotion_analyzer.analyze_emotions(user_input)
            
            # Detect cultural context
            cultural_context = self.cultural_engine.detect_cultural_context(user_input, user_profile)
            
            # Get conversation context
            conversation_context = self.conversation_memory.get_conversation_context(user_id)
            
            # Generate contextually appropriate response
            response_data = await self._generate_contextual_response(
                user_input, emotion_analysis, cultural_context, conversation_context, context
            )
            
            # Apply emotional and cultural adaptations
            adapted_response = await self._apply_adaptations(
                response_data, emotion_analysis, cultural_context, conversation_context
            )
            
            processing_time = time.time() - start_time
            
            # Store conversation in memory
            self.conversation_memory.add_conversation_turn(
                user_id, user_input, adapted_response['response'],
                emotion_analysis, cultural_context
            )
            
            # Update performance metrics
            self.performance_metrics["conversations_handled"] += 1
            self.performance_metrics["average_response_time"] = (
                (self.performance_metrics["average_response_time"] * 
                 (self.performance_metrics["conversations_handled"] - 1) + 
                 processing_time) / self.performance_metrics["conversations_handled"]
            )
            
            # Comprehensive response structure
            response = {
                "model": self.model_name,
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "response": adapted_response['response'],
                "response_metadata": {
                    "processing_time_seconds": processing_time,
                    "response_length_words": len(adapted_response['response'].split()),
                    "confidence_score": adapted_response.get('confidence', 0.8),
                    "adaptation_applied": adapted_response.get('adaptations_applied', [])
                },
                "emotional_analysis": {
                    "user_emotions": emotion_analysis,
                    "response_emotional_tone": adapted_response.get('emotional_tone', 'neutral'),
                    "empathy_level": adapted_response.get('empathy_level', 'moderate'),
                    "emotional_mirroring": adapted_response.get('emotional_mirroring', False)
                },
                "cultural_analysis": {
                    "detected_context": cultural_context,
                    "cultural_adaptations": adapted_response.get('cultural_adaptations', []),
                    "communication_style_match": adapted_response.get('style_match_score', 0.7)
                },
                "conversation_insights": {
                    "relationship_stage": conversation_context.get('relationship_duration', {}).get('relationship_stage', 'unknown'),
                    "emotion_trend": conversation_context.get('emotion_trends', {}).get('trend', 'stable'),
                    "conversation_turn": len(conversation_context.get('recent_conversations', [])) + 1,
                    "personalization_applied": len(conversation_context.get('user_profile', {}).get('topics_of_interest', [])) > 0
                },
                "quality_indicators": {
                    "response_appropriateness": self._assess_response_appropriateness(adapted_response, emotion_analysis, cultural_context),
                    "contextual_relevance": self._assess_contextual_relevance(adapted_response, conversation_context),
                    "emotional_intelligence_score": self._calculate_emotional_intelligence_score(adapted_response, emotion_analysis)
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "processing_time": time.time() - start_time,
                "user_id": user_id
            }
    
    async def _generate_contextual_response(self, user_input: str, emotion_analysis: Dict,
                                          cultural_context: Dict, conversation_context: Dict,
                                          additional_context: Dict = None) -> Dict[str, Any]:
        """Generate base response considering all contexts"""
        try:
            # Determine response strategy based on emotions
            dominant_emotion = emotion_analysis.get('dominant_emotions', [{}])[0].get('emotion', 'neutral')
            emotional_intensity = emotion_analysis.get('dominant_emotions', [{}])[0].get('score', 0.5)
            
            # Select appropriate response templates and strategies
            response_strategy = self._select_response_strategy(dominant_emotion, emotional_intensity, cultural_context)
            
            # Generate contextual response
            base_response = await self._create_base_response(
                user_input, response_strategy, conversation_context, additional_context
            )
            
            return {
                'response': base_response,
                'strategy': response_strategy,
                'confidence': 0.8,
                'emotional_tone': self._determine_appropriate_emotional_tone(dominant_emotion, cultural_context)
            }
            
        except Exception as e:
            logger.error(f"Error generating contextual response: {e}")
            return {
                'response': "I understand what you're saying. Could you tell me more about what you'd like help with?",
                'strategy': 'safe_fallback',
                'confidence': 0.5,
                'emotional_tone': 'neutral'
            }
    
    def _select_response_strategy(self, dominant_emotion: str, intensity: float, cultural_context: Dict) -> Dict[str, Any]:
        """Select appropriate response strategy based on emotion and culture"""
        strategies = {
            'joy': {
                'approach': 'celebratory_supportive',
                'tone': 'warm_enthusiastic',
                'techniques': ['positive_reinforcement', 'shared_excitement', 'encouragement']
            },
            'sadness': {
                'approach': 'empathetic_supportive',
                'tone': 'gentle_understanding',
                'techniques': ['active_listening', 'validation', 'gentle_guidance']
            },
            'anger': {
                'approach': 'calming_respectful',
                'tone': 'calm_measured',
                'techniques': ['de_escalation', 'acknowledgment', 'solution_focus']
            },
            'fear': {
                'approach': 'reassuring_informative',
                'tone': 'steady_confident',
                'techniques': ['reassurance', 'information_providing', 'step_by_step_guidance']
            },
            'surprise': {
                'approach': 'explanatory_engaging',
                'tone': 'clear_informative',
                'techniques': ['clarification', 'context_providing', 'gentle_exploration']
            },
            'neutral': {
                'approach': 'balanced_helpful',
                'tone': 'friendly_professional',
                'techniques': ['information_gathering', 'solution_oriented', 'collaborative']
            }
        }
        
        base_strategy = strategies.get(dominant_emotion, strategies['neutral'])
        
        # Adjust for cultural context
        if cultural_context.get('cultural_traits', {}).get('formality_preference', 0.5) > 0.7:
            base_strategy['tone'] = base_strategy['tone'].replace('friendly', 'respectful')
            base_strategy['techniques'].insert(0, 'formal_courtesy')
        
        # Adjust for emotional intensity
        if intensity > 0.8:
            base_strategy['intensity_adjustment'] = 'high_empathy'
            base_strategy['response_length'] = 'extended'
        elif intensity < 0.3:
            base_strategy['intensity_adjustment'] = 'moderate_support'
            base_strategy['response_length'] = 'concise'
        
        return base_strategy
    
    async def _create_base_response(self, user_input: str, strategy: Dict, 
                                   conversation_context: Dict, additional_context: Dict = None) -> str:
        """Create the base response using the selected strategy"""
        try:
            # Get conversation history for context
            recent_conversations = conversation_context.get('recent_conversations', [])
            user_profile = conversation_context.get('user_profile', {})
            
            # Response templates based on strategy
            response_templates = {
                'celebratory_supportive': [
                    "That's wonderful! I can sense your excitement about this.",
                    "How fantastic! I'm really happy to hear that.",
                    "That sounds amazing! It's great to see your enthusiasm."
                ],
                'empathetic_supportive': [
                    "I can understand how that might feel difficult for you.",
                    "Thank you for sharing that with me. It sounds like a challenging situation.",
                    "I hear that this is really weighing on you right now."
                ],
                'calming_respectful': [
                    "I can see this is really important to you, and I want to help.",
                    "Let's take a step back and look at this together.",
                    "I understand your frustration, and I'm here to work through this with you."
                ],
                'reassuring_informative': [
                    "I can help you understand this better. Let me explain what I know.",
                    "It's completely normal to feel uncertain about this. Here's what we can do.",
                    "Let me provide some information that might help ease your concerns."
                ],
                'explanatory_engaging': [
                    "That's an interesting development! Let me help clarify what's happening.",
                    "I can see why that would be unexpected. Here's what I think is going on.",
                    "That's quite something! Let me help you understand this better."
                ],
                'balanced_helpful': [
                    "I'd be happy to help you with that. Let me understand what you're looking for.",
                    "Thank you for your question. Here's how I can assist you.",
                    "I understand what you're asking. Let me provide some helpful information."
                ]
            }
            
            approach = strategy.get('approach', 'balanced_helpful')
            templates = response_templates.get(approach, response_templates['balanced_helpful'])
            
            # Select appropriate template and personalize
            base_template = random.choice(templates)
            
            # Add personalization based on user profile
            if user_profile.get('topics_of_interest'):
                interests = user_profile['topics_of_interest']
                relevant_interests = [interest for interest in interests if interest.lower() in user_input.lower()]
                if relevant_interests:
                    base_template += f" I remember you're interested in {relevant_interests[0]}."
            
            # Adjust for conversation history
            if len(recent_conversations) > 5:
                relationship_acknowledgment = " As we continue our conversation, "
                base_template = base_template.replace(". ", f".{relationship_acknowledgment}")
            
            return base_template
            
        except Exception as e:
            logger.error(f"Error creating base response: {e}")
            return "I appreciate you sharing that with me. How can I best help you today?"
    
    async def _apply_adaptations(self, response_data: Dict, emotion_analysis: Dict,
                               cultural_context: Dict, conversation_context: Dict) -> Dict[str, Any]:
        """Apply emotional and cultural adaptations to the response"""
        try:
            adapted_response = response_data['response']
            adaptations_applied = []
            cultural_adaptations = []
            
            # Apply emotional adaptations
            dominant_emotion = emotion_analysis.get('dominant_emotions', [{}])[0].get('emotion', 'neutral')
            emotion_intensity = emotion_analysis.get('dominant_emotions', [{}])[0].get('score', 0.5)
            
            # Emotional mirroring
            if emotion_intensity > 0.6:
                adapted_response = await self._apply_emotional_mirroring(
                    adapted_response, dominant_emotion, emotion_intensity
                )
                adaptations_applied.append('emotional_mirroring')
            
            # Cultural adaptations
            formality_level = cultural_context.get('formality_level', {}).get('level', 'neutral')
            
            if formality_level == 'formal':
                adapted_response = await self._increase_formality(adapted_response)
                cultural_adaptations.append('increased_formality')
            elif formality_level == 'informal':
                adapted_response = await self._decrease_formality(adapted_response)
                cultural_adaptations.append('decreased_formality')
            
            # Communication style adaptations
            comm_style = cultural_context.get('communication_patterns', {}).get('communication_style', 'balanced')
            if comm_style == 'direct':
                adapted_response = await self._make_more_direct(adapted_response)
                cultural_adaptations.append('directness_adjustment')
            elif comm_style == 'indirect':
                adapted_response = await self._make_more_indirect(adapted_response)
                cultural_adaptations.append('indirectness_adjustment')
            
            # Empathy level adjustment
            empathy_level = self._calculate_appropriate_empathy_level(emotion_analysis, conversation_context)
            
            if empathy_level == 'high':
                adapted_response = await self._increase_empathy(adapted_response, dominant_emotion)
                adaptations_applied.append('high_empathy')
            
            return {
                'response': adapted_response,
                'adaptations_applied': adaptations_applied,
                'cultural_adaptations': cultural_adaptations,
                'emotional_tone': response_data.get('emotional_tone', 'neutral'),
                'empathy_level': empathy_level,
                'emotional_mirroring': emotion_intensity > 0.6,
                'style_match_score': self._calculate_style_match_score(cultural_context, adaptations_applied)
            }
            
        except Exception as e:
            logger.error(f"Error applying adaptations: {e}")
            return {
                'response': response_data.get('response', 'I understand. How can I help you?'),
                'adaptations_applied': ['error_fallback'],
                'cultural_adaptations': [],
                'emotional_tone': 'neutral',
                'empathy_level': 'moderate'
            }
    
    async def _apply_emotional_mirroring(self, response: str, emotion: str, intensity: float) -> str:
        """Apply emotional mirroring to match user's emotional state appropriately"""
        try:
            if emotion == 'joy' and intensity > 0.7:
                # Add enthusiasm markers
                response = response.replace('!', '! 🌟')
                response = response.replace('.', '.')
                if not response.endswith('!'):
                    response = response.rstrip('.') + '!'
            
            elif emotion == 'sadness' and intensity > 0.6:
                # Use gentler language
                response = response.replace('great', 'understanding')
                response = response.replace('wonderful', 'meaningful')
                response = response.replace('!', '.')
            
            elif emotion == 'anger' and intensity > 0.5:
                # Use calming language
                response = response.replace('I think', 'I understand')
                response = response.replace('you should', 'you might consider')
                response = response.replace('!', '.')
            
            elif emotion == 'fear' and intensity > 0.6:
                # Use reassuring language
                response = response.replace('might', 'can definitely')
                response = response.replace('maybe', 'certainly')
                if not any(word in response.lower() for word in ['safe', 'secure', 'okay', 'fine']):
                    response += " Everything will be okay."
            
            return response
            
        except Exception as e:
            logger.error(f"Error applying emotional mirroring: {e}")
            return response
    
    async def _increase_formality(self, response: str) -> str:
        """Increase formality level of the response"""
        try:
            # Replace informal contractions
            replacements = {
                "I'm": "I am",
                "you're": "you are",
                "we're": "we are",
                "they're": "they are",
                "it's": "it is",
                "don't": "do not",
                "can't": "cannot",
                "won't": "will not",
                "isn't": "is not",
                "aren't": "are not"
            }
            
            for informal, formal in replacements.items():
                response = response.replace(informal, formal)
            
            # Add formal courtesy phrases
            if not any(courtesy in response.lower() for courtesy in ['please', 'kindly', 'would you']):
                if '?' in response:
                    response = response.replace('?', ', please?')
            
            # Replace casual words with formal equivalents
            formal_replacements = {
                'help': 'assist',
                'get': 'obtain',
                'find out': 'determine',
                'show': 'demonstrate',
                'tell': 'inform'
            }
            
            for casual, formal in formal_replacements.items():
                response = response.replace(casual, formal)
            
            return response
            
        except Exception as e:
            logger.error(f"Error increasing formality: {e}")
            return response
    
    async def _decrease_formality(self, response: str) -> str:
        """Decrease formality level of the response"""
        try:
            # Add contractions
            replacements = {
                "I am": "I'm",
                "you are": "you're",
                "we are": "we're",
                "they are": "they're",
                "it is": "it's",
                "do not": "don't",
                "cannot": "can't",
                "will not": "won't",
                "is not": "isn't",
                "are not": "aren't"
            }
            
            for formal, informal in replacements.items():
                response = response.replace(formal, informal)
            
            # Replace formal words with casual equivalents
            casual_replacements = {
                'assist': 'help',
                'obtain': 'get',
                'determine': 'find out',
                'demonstrate': 'show',
                'inform': 'tell'
            }
            
            for formal, casual in casual_replacements.items():
                response = response.replace(formal, casual)
            
            return response
            
        except Exception as e:
            logger.error(f"Error decreasing formality: {e}")
            return response
    
    async def _make_more_direct(self, response: str) -> str:
        """Make response more direct and explicit"""
        try:
            # Remove hedging language
            hedges = ['perhaps', 'maybe', 'possibly', 'might be', 'could be', 'I think', 'I believe']
            
            for hedge in hedges:
                response = response.replace(hedge + ' ', '')
            
            # Make statements more definitive
            response = response.replace('You might want to', 'You should')
            response = response.replace('You could consider', 'I recommend')
            response = response.replace('It would be good if', 'Please')
            
            return response
            
        except Exception as e:
            logger.error(f"Error making response more direct: {e}")
            return response
    
    async def _make_more_indirect(self, response: str) -> str:
        """Make response more indirect and diplomatic"""
        try:
            # Add hedging language
            response = response.replace('You should', 'You might want to')
            response = response.replace('I recommend', 'You could consider')
            response = response.replace('Please', 'It would be helpful if you could')
            
            # Soften definitive statements
            response = response.replace('This is', 'This might be')
            response = response.replace('will be', 'could be')
            
            return response
            
        except Exception as e:
            logger.error(f"Error making response more indirect: {e}")
            return response
    
    async def _increase_empathy(self, response: str, dominant_emotion: str) -> str:
        """Increase empathy level in response"""
        try:
            empathy_phrases = {
                'sadness': ['I can imagine how difficult this must be for you', 'My heart goes out to you'],
                'anger': ['I can understand your frustration', 'It sounds like this is really bothering you'],
                'fear': ['I can see why you might be worried about this', 'Your concerns are completely valid'],
                'joy': ['I can feel your excitement about this', 'Your happiness is contagious'],
                'surprise': ['What an unexpected turn of events', 'I can imagine how surprising that must have been']
            }
            
            if dominant_emotion in empathy_phrases:
                empathy_phrase = random.choice(empathy_phrases[dominant_emotion])
                response = empathy_phrase + '. ' + response
            
            return response
            
        except Exception as e:
            logger.error(f"Error increasing empathy: {e}")
            return response
    
    def _determine_appropriate_emotional_tone(self, dominant_emotion: str, cultural_context: Dict) -> str:
        """Determine appropriate emotional tone for response"""
        emotion_tone_mapping = {
            'joy': 'warm_positive',
            'sadness': 'gentle_supportive',
            'anger': 'calm_understanding',
            'fear': 'reassuring_confident',
            'surprise': 'interested_clarifying',
            'disgust': 'respectful_professional',
            'trust': 'warm_reliable',
            'anticipation': 'encouraging_optimistic'
        }
        
        base_tone = emotion_tone_mapping.get(dominant_emotion, 'neutral_professional')
        
        # Adjust for cultural formality
        if cultural_context.get('cultural_traits', {}).get('formality_preference', 0.5) > 0.7:
            base_tone = base_tone.replace('warm', 'respectful')
        
        return base_tone
    
    def _calculate_appropriate_empathy_level(self, emotion_analysis: Dict, conversation_context: Dict) -> str:
        """Calculate appropriate empathy level"""
        # Base empathy on emotion intensity
        dominant_emotions = emotion_analysis.get('dominant_emotions', [])
        if not dominant_emotions:
            return 'moderate'
        
        max_intensity = max(emotion['score'] for emotion in dominant_emotions)
        
        # Adjust for relationship stage
        relationship_stage = conversation_context.get('relationship_duration', {}).get('relationship_stage', 'first_meeting')
        
        if relationship_stage in ['established_relationship', 'regular_interaction']:
            empathy_boost = 0.2
        else:
            empathy_boost = 0.0
        
        effective_intensity = min(1.0, max_intensity + empathy_boost)
        
        if effective_intensity > 0.8:
            return 'high'
        elif effective_intensity > 0.5:
            return 'moderate'
        else:
            return 'low'
    
    def _calculate_style_match_score(self, cultural_context: Dict, adaptations: List[str]) -> float:
        """Calculate how well the response matches expected cultural style"""
        base_score = 0.7
        
        # Bonus for cultural adaptations
        cultural_adaptations = len([a for a in adaptations if 'formal' in a or 'direct' in a])
        adaptation_bonus = min(0.2, cultural_adaptations * 0.1)
        
        # Bonus for formality match
        expected_formality = cultural_context.get('cultural_traits', {}).get('formality_preference', 0.5)
        formality_level = cultural_context.get('formality_level', {}).get('ratio', 0.5)
        
        formality_match = 1.0 - abs(expected_formality - formality_level)
        formality_bonus = formality_match * 0.1
        
        return min(1.0, base_score + adaptation_bonus + formality_bonus)
    
    def _assess_response_appropriateness(self, response_data: Dict, emotion_analysis: Dict, cultural_context: Dict) -> Dict[str, Any]:
        """Assess how appropriate the response is given the context"""
        try:
            appropriateness_score = 0.8  # Base score
            
            # Check emotional appropriateness
            response_tone = response_data.get('emotional_tone', 'neutral')
            dominant_emotion = emotion_analysis.get('dominant_emotions', [{}])[0].get('emotion', 'neutral')
            
            emotion_appropriateness = {
                'joy': ['warm_positive', 'encouraging_optimistic'],
                'sadness': ['gentle_supportive', 'calm_understanding'],
                'anger': ['calm_understanding', 'respectful_professional'],
                'fear': ['reassuring_confident', 'gentle_supportive']
            }
            
            if dominant_emotion in emotion_appropriateness:
                if response_tone in emotion_appropriateness[dominant_emotion]:
                    appropriateness_score += 0.1
            
            # Check cultural appropriateness
            expected_formality = cultural_context.get('cultural_traits', {}).get('formality_preference', 0.5)
            if 'formal' in response_data.get('cultural_adaptations', []) and expected_formality > 0.6:
                appropriateness_score += 0.1
            
            return {
                'score': min(1.0, appropriateness_score),
                'emotional_match': response_tone in emotion_appropriateness.get(dominant_emotion, [response_tone]),
                'cultural_sensitivity': len(response_data.get('cultural_adaptations', [])) > 0,
                'recommendations': self._generate_appropriateness_recommendations(appropriateness_score)
            }
            
        except Exception as e:
            logger.error(f"Error assessing response appropriateness: {e}")
            return {'score': 0.5, 'error': str(e)}
    
    def _assess_contextual_relevance(self, response_data: Dict, conversation_context: Dict) -> Dict[str, Any]:
        """Assess how relevant the response is to the conversation context"""
        try:
            relevance_score = 0.7  # Base score
            
            # Check for personalization
            user_interests = conversation_context.get('user_profile', {}).get('topics_of_interest', [])
            if user_interests and any(interest in response_data['response'].lower() for interest in user_interests):
                relevance_score += 0.2
            
            # Check conversation continuity
            recent_conversations = conversation_context.get('recent_conversations', [])
            if len(recent_conversations) > 0:
                # Simple check for topic continuity (could be more sophisticated)
                last_response = recent_conversations[-1].get('assistant_response', '')
                if len(set(response_data['response'].split()) & set(last_response.split())) > 2:
                    relevance_score += 0.1
            
            return {
                'score': min(1.0, relevance_score),
                'personalized': len(user_interests) > 0,
                'contextually_aware': len(recent_conversations) > 0,
                'conversation_continuity': relevance_score > 0.8
            }
            
        except Exception as e:
            logger.error(f"Error assessing contextual relevance: {e}")
            return {'score': 0.5, 'error': str(e)}
    
    def _calculate_emotional_intelligence_score(self, response_data: Dict, emotion_analysis: Dict) -> float:
        """Calculate emotional intelligence score for the response"""
        try:
            base_score = 0.6
            
            # Emotional awareness bonus
            if emotion_analysis.get('dominant_emotions'):
                base_score += 0.2
            
            # Emotional adaptation bonus
            if response_data.get('emotional_mirroring'):
                base_score += 0.1
            
            # Empathy level bonus
            empathy_level = response_data.get('empathy_level', 'moderate')
            if empathy_level == 'high':
                base_score += 0.1
            
            return min(1.0, base_score)
            
        except Exception as e:
            logger.error(f"Error calculating emotional intelligence score: {e}")
            return 0.5
    
    def _generate_appropriateness_recommendations(self, score: float) -> List[str]:
        """Generate recommendations for improving response appropriateness"""
        recommendations = []
        
        if score < 0.6:
            recommendations.append("Consider better emotional tone matching")
            recommendations.append("Improve cultural sensitivity adaptations")
        elif score < 0.8:
            recommendations.append("Fine-tune emotional responses")
            recommendations.append("Enhance cultural awareness")
        else:
            recommendations.append("Response appropriateness is good")
        
        return recommendations
    
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
            "emotional_intelligence": {
                "emotion_detection": "advanced",
                "empathy_levels": ["low", "moderate", "high"],
                "emotional_mirroring": "adaptive",
                "supported_emotions": list(self.emotion_analyzer.emotion_patterns.keys())
            },
            "cultural_adaptation": {
                "supported_cultures": list(self.cultural_engine.cultural_markers.keys()),
                "formality_adaptation": "dynamic",
                "communication_styles": ["direct", "indirect", "balanced"],
                "context_awareness": "high_context"
            },
            "conversation_management": {
                "memory_enabled": True,
                "relationship_tracking": True,
                "personalization": "adaptive",
                "context_length": self.max_context_length
            },
            "performance_metrics": self.performance_metrics
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        try:
            start_time = time.time()
            
            # Test emotional analysis
            test_emotional_input = "I'm so excited about this new opportunity, but also a bit nervous about the challenges ahead!"
            emotion_test = self.emotion_analyzer.analyze_emotions(test_emotional_input)
            
            # Test cultural analysis
            cultural_test = self.cultural_engine.detect_cultural_context(test_emotional_input)
            
            # Test response generation
            response_test = await self.generate_response(
                test_emotional_input,
                user_id="health_check_user"
            )
            
            # Test conversation memory
            memory_stats = {
                "stored_conversations": len(self.conversation_memory.conversation_history),
                "user_profiles": len(self.conversation_memory.user_profiles),
                "emotional_tracking": len(self.conversation_memory.emotional_tracking)
            }
            
            health_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "version": self.version,
                "component_tests": {
                    "emotion_analysis": len(emotion_test.get('emotion_scores', {})) > 0,
                    "cultural_analysis": 'detected_culture' in cultural_test,
                    "response_generation": "error" not in response_test,
                    "conversation_memory": True
                },
                "performance_check": {
                    "health_check_time": health_time,
                    "average_response_time": self.performance_metrics["average_response_time"],
                    "conversations_handled": self.performance_metrics["conversations_handled"]
                },
                "memory_statistics": memory_stats,
                "emotional_capabilities": {
                    "emotions_detected": list(emotion_test.get('emotion_scores', {}).keys()),
                    "emotional_complexity": emotion_test.get('emotional_complexity', 0),
                    "sentiment_analysis": emotion_test.get('overall_sentiment', 'unknown')
                },
                "cultural_capabilities": {
                    "formality_detection": cultural_test.get('formality_level', {}).get('level', 'unknown'),
                    "communication_style": cultural_test.get('communication_patterns', {}).get('communication_style', 'unknown'),
                    "adaptations_available": len(cultural_test.get('adaptation_suggestions', []))
                },
                "all_tests_passed": all([
                    len(emotion_test.get('emotion_scores', {})) > 0,
                    'detected_culture' in cultural_test,
                    "error" not in response_test
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
    """Main function for testing Yi runner"""
    try:
        # Initialize runner
        runner = YiRunner()
        
        # Test model info
        print("=== Model Information ===")
        model_info = runner.get_model_info()
        print(json.dumps(model_info, indent=2))
        
        # Test health check
        print("\n=== Health Check ===")
        health = await runner.health_check()
        print(json.dumps(health, indent=2))
        
        # Test emotionally charged conversation
        print("\n=== Emotional Conversation Test ===")
        
        test_conversations = [
            ("I just got promoted at work! I'm so excited but also nervous about the new responsibilities.", "user_1"),
            ("I'm really struggling with this project. Nothing seems to be working and I feel like giving up.", "user_2"),
            ("Could you please help me understand how to improve my presentation skills?", "user_3"),
            ("Hey, what's the best way to learn programming? I'm totally new to this stuff.", "user_4")
        ]
        
        for user_input, user_id in test_conversations:
            print(f"\n--- Conversation with {user_id} ---")
            print(f"User: {user_input}")
            
            response = await runner.generate_response(user_input, user_id=user_id)
            
            print(f"Yi: {response['response']}")
            print(f"Emotions detected: {[e['emotion'] for e in response['emotional_analysis']['user_emotions']['dominant_emotions']]}")
            print(f"Cultural adaptations: {response['cultural_analysis']['cultural_adaptations']}")
            print(f"Empathy level: {response['emotional_analysis']['empathy_level']}")
            print(f"Relationship stage: {response['conversation_insights']['relationship_stage']}")
        
        # Test follow-up conversation
        print("\n=== Follow-up Conversation Test ===")
        follow_up = await runner.generate_response(
            "Thank you so much for that advice! I feel much more confident now.",
            user_id="user_1"
        )
        
        print(f"User 1 follow-up: Thank you so much for that advice! I feel much more confident now.")
        print(f"Yi: {follow_up['response']}")
        print(f"Conversation turn: {follow_up['conversation_insights']['conversation_turn']}")
        print(f"Emotion trend: {follow_up['conversation_insights']['emotion_trend']}")
        
        # Test cultural sensitivity
        print("\n=== Cultural Sensitivity Test ===")
        formal_input = "Dear Assistant, I would be most grateful if you could kindly provide information regarding the proper methodology for conducting research."
        
        formal_response = await runner.generate_response(formal_input, user_id="formal_user")
        
        print(f"Formal user: {formal_input}")
        print(f"Yi: {formal_response['response']}")
        print(f"Formality adaptations: {formal_response['cultural_analysis']['cultural_adaptations']}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())