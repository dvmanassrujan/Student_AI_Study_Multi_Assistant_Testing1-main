"""
Integration Tests for Meta Llama 3.2:latest Ollama Integration and Multi-Agent Orchestrator
Validates:
1. Ollama server connection (http://localhost:11434) and llama3.2:latest availability.
2. LangChain ChatOllama instantiation.
3. LangGraph router node decision-making.
4. End-to-end multi-agent execution pipeline.
5. Coding, Exam, and Academic agent synthesis.
"""

import os
import sys
import unittest
from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.core.config import settings
from backend.core.llm import get_llm, check_ollama_connection
from backend.agents.orchestrator import app_graph, router_node, coding_node, exam_node, study_node

class TestLlama32OllamaIntegration(unittest.TestCase):

    def test_01_ollama_model_configuration(self):
        """Verifies settings configure Meta Llama 3.2:latest through Ollama."""
        self.assertEqual(settings.MODEL_PROVIDER, "ollama")
        self.assertEqual(settings.MODEL_NAME, "llama3.2:latest")
        self.assertEqual(settings.OLLAMA_BASE_URL, "http://localhost:11434")
        
        status = check_ollama_connection()
        self.assertTrue(status["connected"], f"Ollama not connected: {status.get('message')}")
        self.assertTrue(status["model_available"], f"Model llama3.2:latest not available: {status.get('message')}")

    def test_02_llm_instantiation(self):
        """Verifies get_llm returns a functional ChatOllama instance for llama3.2:latest."""
        llm = get_llm()
        self.assertEqual(llm.model, "llama3.2:latest")
        self.assertIn("11434", llm.base_url)

    def test_03_live_inference_execution(self):
        """Verifies direct inference invocation with llama3.2:latest returns AIMessage with content."""
        llm = get_llm()
        resp = llm.invoke([
            SystemMessage(content="Answer in 5 words or less."),
            HumanMessage(content="What is Newton's first law about?")
        ])
        self.assertTrue(hasattr(resp, "content"))
        self.assertGreater(len(resp.content.strip()), 3)

    def test_04_router_node_routing(self):
        """Verifies router node correctly directs coding queries to coding_agent."""
        state = {"messages": [HumanMessage(content="How do I debug an IndexError in Python list?")]}
        route = router_node(state)
        self.assertIn("next_agent", route)
        self.assertEqual(route.get("next_agent"), "coding_agent")

    def test_05_specialized_nodes(self):
        """Verifies individual agent nodes produce expected domain-specific content."""
        code_res = coding_node({"messages": [HumanMessage(content="Explain binary search complexity in one sentence.")]})
        self.assertIn("generated_content", code_res)
        self.assertEqual(code_res["generated_content"]["type"], "coding")
        self.assertGreater(len(code_res["generated_content"]["content"]), 10)

    def test_06_end_to_end_graph_execution(self):
        """Verifies complete LangGraph graph execution workflow."""
        result = app_graph.invoke({"messages": [HumanMessage(content="Define velocity in one sentence.")]})
        self.assertIn("messages", result)
        last_msg = result["messages"][-1]
        self.assertGreater(len(last_msg.content), 5)

if __name__ == "__main__":
    unittest.main()

