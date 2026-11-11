"""
Unit & Integration Tests for AI Chat Assistant.
Verifies instant responsive streaming yields, fast-path routing, Gradio 6 message formatting, and persistence.
"""

import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.core import chat_history_db
from backend.agents.orchestrator import app_graph, router_node, HumanMessage
from frontend.app import chat_respond, get_session_choices


class TestAiChatAssistant(unittest.TestCase):

    def test_fast_path_router_for_chat_assistant(self):
        """Verify router_node routes conceptual study queries to study_agent without LLM lag."""
        state = {
            "messages": [HumanMessage(content="Explain how photosynthesis works in plants")]
        }
        decision = router_node(state)
        self.assertEqual(decision["next_agent"], "study_agent")

        state_coding = {
            "messages": [HumanMessage(content="Debug this python code: def foo(): print(x)")]
        }
        decision_coding = router_node(state_coding)
        self.assertEqual(decision_coding["next_agent"], "coding_agent")

        state_quiz = {
            "messages": [HumanMessage(content="Generate an exam quiz with MCQs on world history")]
        }
        decision_quiz = router_node(state_quiz)
        self.assertEqual(decision_quiz["next_agent"], "exam_agent")

    def test_chat_respond_instant_yield_and_format(self):
        """Verify chat_respond yields immediately with proper Gradio 6 message dictionary structure."""
        generator = chat_respond(
            user_message="Hello, test message",
            chat_history=[],
            session_id="new",
            chatbot_mode="💬 Chat"
        )
        
        # First yield must be instantaneous with pending status
        msg_box, pending_history, session_id, session_dropdown, ref_img, f_up, img_up, media_dl = next(generator)
        
        self.assertEqual(msg_box, "")
        self.assertIsInstance(pending_history, list)
        self.assertGreaterEqual(len(pending_history), 2)
        self.assertEqual(pending_history[-2]["role"], "user")
        self.assertEqual(pending_history[-2]["content"], "Hello, test message")
        self.assertEqual(pending_history[-1]["role"], "assistant")
        self.assertIn("Thinking", pending_history[-1]["content"])
        self.assertNotEqual(session_id, "new")
        self.assertIsNotNone(session_id)

    def test_chat_history_db_persistence(self):
        """Verify session creation and message storage in SQLite database."""
        session_id = chat_history_db.create_session(title="Test Automated Session")
        self.assertIsNotNone(session_id)
        
        chat_history_db.add_message(session_id, "user", "What is gravity?")
        chat_history_db.add_message(session_id, "assistant", "Gravity is a fundamental force.")
        
        messages = chat_history_db.get_session_messages(session_id)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "What is gravity?")
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertEqual(messages[1]["content"], "Gravity is a fundamental force.")
        
        # Cleanup test session
        chat_history_db.delete_session(session_id)


if __name__ == "__main__":
    unittest.main()
