"""
Integration Tests for Model-Free Intelligence Engine and Multi-Agent Orchestrator.
Validates:
1. Model-free engine configuration and health status.
2. ModelFreeLLM instantiation and invoke compatibility.
3. LangGraph router node decision-making.
4. End-to-end multi-agent execution pipeline (Coding, Exam, Academic Tutor).
"""

import os
import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.core.config import settings
from backend.core.llm import get_llm, check_ollama_connection
from backend.agents.orchestrator import (
    app_graph,
    router_node,
    coding_node,
    exam_node,
    study_node,
    SystemMessage,
    HumanMessage
)


class TestModelFreeIntegration(unittest.TestCase):

    def test_01_model_free_configuration(self):
        """Verifies settings configure deepseek-coder:1.3b engine."""
        self.assertIn(settings.MODEL_PROVIDER, ["ollama", "model_free"])
        self.assertEqual(settings.MODEL_NAME, "deepseek-coder:1.3b")
        status = check_ollama_connection()
        self.assertIn("connected", status)
        self.assertIn("model_available", status)
        self.assertIn("models", status)

    def test_02_llm_instantiation(self):
        """Verifies get_llm returns a functional ModelFreeLLM instance."""
        llm = get_llm()
        self.assertTrue(hasattr(llm, "model_name"))
        self.assertTrue(hasattr(llm, "invoke"))

    def test_03_inference_execution(self):
        """Verifies direct inference invocation returns AIMessage with content."""
        llm = get_llm()
        resp = llm.invoke([
            SystemMessage(content="Answer in 5 words or less."),
            HumanMessage(content="What is Newton's first law about?")
        ])
        self.assertTrue(hasattr(resp, "content"))
        self.assertGreater(len(resp.content.strip()), 10)

    def test_04_router_node(self):
        """Verifies router node routes coding, exam, and study intents."""
        res_code = router_node({"messages": [HumanMessage(content="def binary_search(arr):")]})
        self.assertEqual(res_code["next_agent"], "coding_agent")

        res_exam = router_node({"messages": [HumanMessage(content="multiple choice exam quiz on biology")]})
        self.assertEqual(res_exam["next_agent"], "exam_agent")

        res_plan = router_node({"messages": [HumanMessage(content="create a study plan for 1 week")]})
        self.assertEqual(res_plan["next_agent"], "study_planner_agent")

    def test_05_agent_execution(self):
        """Verifies agent nodes execute and produce rich markdown content."""
        res_code = coding_node({"messages": [HumanMessage(content="explain binary search")]})
        self.assertIn("messages", res_code)
        self.assertGreater(len(res_code["messages"][-1].content), 20)

        res_exam = exam_node({"messages": [HumanMessage(content="quiz on Photosynthesis")]})
        self.assertIn("messages", res_exam)
        self.assertGreater(len(res_exam["messages"][-1].content), 20)

        res_study = study_node({"messages": [HumanMessage(content="explain Machine Learning")]})
        self.assertIn("messages", res_study)
        self.assertGreater(len(res_study["messages"][-1].content), 20)


if __name__ == "__main__":
    unittest.main()
