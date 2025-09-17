"""
Tests for Gossip Queen Agent
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.cortex.controller import GossipqueenController


class TestGossipqueenAgent(unittest.TestCase):
    """Test cases for Gossip Queen agent"""

    def setUp(self):
        """Set up test fixtures"""
        self.controller = GossipqueenController()
        self.test_session_id = "test_session"

    def test_controller_initialization(self):
        """Test controller initialization"""
        self.assertIsNotNone(self.controller)
        self.assertEqual(
            self.controller.personality_traits,
            [
                "talkative",
                "social",
                "curious",
                "enthusiastic",
                "dramatic",
                "well_informed",
            ],
        )
        self.assertEqual(
            self.controller.response_style,
            {
                "tone": "excited_chatty",
                "formality": "very_casual",
                "verbosity": "very_verbose",
                "humor": "gossipy_fun",
            },
        )

    def test_message_processing(self):
        """Test message processing"""
        message = "Hello!"
        response = self.controller.process_message(message, self.test_session_id)

        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_personality_traits(self):
        """Test personality trait adherence"""
        # Test messages that should trigger personality-specific responses
        test_cases = {
            "Romantic": "I love you",
            "Laid-back": "Do I really have to do this?",
            "Social": "Tell me some gossip!",
            "Emotional": "I'm feeling really sad",
            "Authoritative": "Have you completed your tasks?",
            "Technical": "Write me a Python function",
        }

        personality_message = test_cases.get("Social", "Hello")
        response = self.controller.process_message(
            personality_message, self.test_session_id
        )

        # Response should be non-empty and contextual
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_fallback_response(self):
        """Test fallback response handling"""
        fallback = self.controller._get_fallback_response()
        self.assertIsInstance(fallback, str)
        self.assertGreater(len(fallback), 0)

    def test_emotional_state_assessment(self):
        """Test emotional state assessment"""
        happy_message = "I'm so excited and happy!"
        sad_message = "I feel really depressed today"

        happy_emotion = self.controller._assess_emotional_state(happy_message)
        sad_emotion = self.controller._assess_emotional_state(sad_message)

        self.assertEqual(happy_emotion, "happy")
        self.assertEqual(sad_emotion, "sad")

    def test_context_building(self):
        """Test context building for responses"""
        context = self.controller._build_context(self.test_session_id, "Test message")

        self.assertIsInstance(context, dict)
        self.assertIn("agent_name", context)
        self.assertIn("personality_type", context)
        self.assertIn("current_message", context)
        self.assertEqual(context["agent_name"], "Gossip Queen")
        self.assertEqual(context["personality_type"], "Social")


if __name__ == "__main__":
    unittest.main()
