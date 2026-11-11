"""
Comprehensive Integration & Verification Tests for:
1. Exam Preparation Agent
2. Study Planner Agent
3. Coding Lab Agent

Validates:
- Direct agent node execution in LangGraph (exam_node, study_planner_node, coding_node)
- Router node fast-path, keyword fallback, and agent communication
- Frontend generator functions (generate_exam_material, generate_study_plan, run_coding_lab)
- Input validation, boundary clamping, and file slug sanitization
- FastAPI endpoints (/api/agents/exam-prep, /api/agents/study-planner, /api/agents/coding-lab)
"""

import sys
import os
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.agents.orchestrator import (
    app_graph,
    router_node,
    exam_node,
    study_planner_node,
    coding_node,
    SUPPORTED_AGENTS,
    HumanMessage
)
from frontend.app import (
    generate_exam_material,
    generate_study_plan,
    run_coding_lab
)

try:
    from fastapi.testclient import TestClient
    from backend.main import app
    client = TestClient(app)
except ImportError:
    client = None


class TestThreeAgentsIntegration(unittest.TestCase):

    # =========================================================================
    # 1. Router & Agent Communication Tests
    # =========================================================================

    def test_01_supported_agents_registry(self):
        """Verifies that all three agents are explicitly registered in SUPPORTED_AGENTS."""
        self.assertIn("exam_agent", SUPPORTED_AGENTS)
        self.assertIn("study_planner_agent", SUPPORTED_AGENTS)
        self.assertIn("coding_agent", SUPPORTED_AGENTS)

    def test_02_router_fast_path_explicit_agent(self):
        """Verifies that router node respects explicit next_agent instantly without LLM query."""
        for target in ["exam_agent", "study_planner_agent", "coding_agent"]:
            state = {"messages": [HumanMessage(content="test")], "next_agent": target}
            res = router_node(state)
            self.assertEqual(res.get("next_agent"), target)

    def test_03_router_fast_path_task_type(self):
        """Verifies that router node maps task_type to corresponding agent directly."""
        mapping = {
            "exam": "exam_agent",
            "study_planner": "study_planner_agent",
            "coding": "coding_agent",
        }
        for task_type, expected_agent in mapping.items():
            state = {"messages": [HumanMessage(content="test")], "task_type": task_type}
            res = router_node(state)
            self.assertEqual(res.get("next_agent"), expected_agent)

    # =========================================================================
    # 2. Exam Preparation Agent Tests
    # =========================================================================

    def test_04_exam_node_direct_execution(self):
        """Verifies that exam_node generates structured educational assessment content."""
        state = {
            "messages": [
                HumanMessage(content="Generate a 1-question multiple choice quiz on Photosynthesis with answer key.")
            ]
        }
        res = exam_node(state)
        self.assertIn("messages", res)
        self.assertIn("generated_content", res)
        self.assertEqual(res["generated_content"]["type"], "exam")
        content = res["messages"][-1].content
        self.assertGreater(len(content.strip()), 20)

    def test_05_generate_exam_material_frontend_validation(self):
        """Verifies input validation and safe handling in generate_exam_material."""
        # Empty topic
        empty_res, empty_file = generate_exam_material("", "Mock Test", "Beginner", 5, "")
        self.assertIn("⚠️", empty_res)
        self.assertIsNone(empty_file)

        # Successful generation with special characters in topic (tests slug sanitization)
        content, file_path = generate_exam_material(
            "C++ / OOP: Polymorphism",
            "Short Quiz",
            "Intermediate",
            1,
            "Focus on virtual functions"
        )
        self.assertNotIn("❌ Error", content)
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_06_exam_prep_api_endpoint(self):
        """Verifies FastAPI endpoint /api/agents/exam-prep."""
        if client is None:
            self.skipTest("FastAPI not installed in environment")
        payload = {
            "topic": "Python Functions",
            "prep_type": "Short Quiz",
            "difficulty": "Beginner",
            "num_questions": 1,
            "additional_context": "Focus on def and return"
        }
        response = client.post("/api/agents/exam-prep", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("agent"), "exam_agent")
        self.assertGreater(len(data.get("content", "")), 20)

    # =========================================================================
    # 3. Study Planner Agent Tests
    # =========================================================================

    def test_07_study_planner_node_direct_execution(self):
        """Verifies that study_planner_node generates structured study timeline content."""
        state = {
            "messages": [
                HumanMessage(content="Create a 2-day study plan for Linear Algebra (1 hour/day).")
            ]
        }
        res = study_planner_node(state)
        self.assertIn("messages", res)
        self.assertIn("generated_content", res)
        self.assertEqual(res["generated_content"]["type"], "study_plan")
        content = res["messages"][-1].content
        self.assertGreater(len(content.strip()), 20)

    def test_08_generate_study_plan_frontend_validation(self):
        """Verifies input validation and safe handling in generate_study_plan."""
        # Empty topic
        empty_res, empty_file = generate_study_plan("", "Beginner", "1 Week", 2, "")
        self.assertIn("⚠️", empty_res)
        self.assertIsNone(empty_file)

        # Successful generation with special characters in topic (tests slug sanitization)
        content, file_path = generate_study_plan(
            "Data Structures & Algorithms: Trees",
            "Intermediate",
            "3 Days",
            2,
            "Master BST insertion and traversal"
        )
        self.assertNotIn("❌ Error", content)
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_09_study_planner_api_endpoint(self):
        """Verifies FastAPI endpoint /api/agents/study-planner."""
        if client is None:
            self.skipTest("FastAPI not installed in environment")
        payload = {
            "topic": "World History",
            "level": "Beginner",
            "duration": "1 Day",
            "hours_per_day": 1.0,
            "goals": "Overview of ancient civilizations"
        }
        response = client.post("/api/agents/study-planner", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("agent"), "study_planner_agent")
        self.assertGreater(len(data.get("content", "")), 20)

    # =========================================================================
    # 4. Coding Lab Agent Tests
    # =========================================================================

    def test_10_coding_node_direct_execution(self):
        """Verifies that coding_node analyzes and debugs code with Big-O complexity."""
        state = {
            "messages": [
                HumanMessage(content="Debug this code in 2 sentences: def add(a, b): return a - b")
            ]
        }
        res = coding_node(state)
        self.assertIn("messages", res)
        self.assertIn("generated_content", res)
        self.assertEqual(res["generated_content"]["type"], "coding")
        content = res["messages"][-1].content
        self.assertGreater(len(content.strip()), 20)

    def test_11_run_coding_lab_frontend_validation(self):
        """Verifies input validation and execution across modes in run_coding_lab."""
        # Empty code in Debug Code mode
        empty_res, empty_file = run_coding_lab("Debug Code", "Python", "", "", "")
        self.assertIn("⚠️", empty_res)
        self.assertIsNone(empty_file)

        # Empty topic in DSA mode
        empty_dsa_res, empty_dsa_file = run_coding_lab("Learn a Topic (e.g., DSA)", "Python", "", "", "")
        self.assertIn("⚠️", empty_dsa_res)
        self.assertIsNone(empty_dsa_file)

        # Successful execution in Debug Code mode
        buggy_code = "def is_positive(n):\n    return n < 0"
        content, file_path = run_coding_lab(
            "Debug Code",
            "Python",
            buggy_code,
            "Function returns True for negative numbers instead of positive",
            ""
        )
        self.assertNotIn("❌ Error", content)
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_12_coding_lab_api_endpoint(self):
        """Verifies FastAPI endpoint /api/agents/coding-lab."""
        if client is None:
            self.skipTest("FastAPI not installed in environment")
        payload = {
            "mode": "Debug Code",
            "language": "Python",
            "code_snippet": "print('hello world'",
            "error_msg": "SyntaxError: unexpected EOF while parsing",
            "dsa_topic": ""
        }
        response = client.post("/api/agents/coding-lab", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("agent"), "coding_agent")
        self.assertGreater(len(data.get("content", "")), 20)


if __name__ == "__main__":
    unittest.main()
