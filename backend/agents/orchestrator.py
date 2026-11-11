"""
Model-Free Multi-Agent Orchestrator.
Coordinates specialized academic agents using deterministic Python intelligence.
100% Model-Free, API-Free, Zero-Cost.
"""

from typing import Literal, Dict, Any, List, Optional
import json
import logging
import re

from backend.agents.state import AgentState
from backend.core.llm import get_llm
from backend.intelligence import (
    classify_intent,
    study_engine,
    generate_study_plan_schedule,
    generate_mcqs_for_topic,
    generate_mcqs_from_text,
    format_exam_material,
    debug_code_snippet,
    explain_code_snippet,
    optimize_code_snippet,
    teach_dsa_topic,
    chunk_document,
    DocumentSearchIndex,
    answer_document_query,
    generate_short_summary,
    generate_detailed_summary,
    generate_important_points,
    generate_definitions_lexicon,
    generate_exam_notes,
    generate_flashcards,
    format_flashcard_markdown
)

logger = logging.getLogger(__name__)

# Message class fallbacks if langchain_core is not installed
try:
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
except ImportError:
    class BaseMessage:
        def __init__(self, content: str, type: str = "base"):
            self.content = content
            self.type = type
        def __repr__(self):
            return f"{self.__class__.__name__}(content={self.content[:30]!r}...)"

    class SystemMessage(BaseMessage):
        def __init__(self, content: str):
            super().__init__(content, type="system")

    class HumanMessage(BaseMessage):
        def __init__(self, content: str):
            super().__init__(content, type="human")

    class AIMessage(BaseMessage):
        def __init__(self, content: str):
            super().__init__(content, type="ai")

# LangGraph fallback if langgraph is not installed
try:
    from langgraph.graph import StateGraph, END
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    END = "__end__"

SUPPORTED_AGENTS = {
    "study_agent",
    "study_planner_agent",
    "exam_agent",
    "coding_agent",
    "project_agent",
    "document_agent",
    "audio_agent",
    "video_agent",
    "memory_agent",
    "personalization_agent",
}


def _extract_prompt_text(messages: List[Any]) -> str:
    """Helper to extract clean prompt text from list of messages."""
    for m in reversed(messages):
        if isinstance(m, HumanMessage) or getattr(m, "type", "") == "human" or getattr(m, "role", "") == "user":
            return str(getattr(m, "content", ""))
        elif isinstance(m, dict) and m.get("role") == "user":
            return str(m.get("content", ""))
    if messages:
        last = messages[-1]
        return str(getattr(last, "content", last))
    return ""


# =========================================================================
# 1. Orchestrator Router Node
# =========================================================================

def router_node(state: AgentState) -> Dict[str, Any]:
    """Orchestrator to route to the correct agent based on task type or intent."""
    explicit_agent = state.get("next_agent")
    if explicit_agent and explicit_agent in SUPPORTED_AGENTS:
        return {"next_agent": explicit_agent}

    task_type = state.get("task_type")
    if task_type:
        task_map = {
            "exam": "exam_agent",
            "exam_prep": "exam_agent",
            "study_planner": "study_planner_agent",
            "study_plan": "study_planner_agent",
            "study": "study_agent",
            "coding": "coding_agent",
            "coding_lab": "coding_agent",
            "project": "project_agent",
            "document": "document_agent",
            "audio": "audio_agent",
            "video": "video_agent",
            "memory": "memory_agent",
            "personalization": "personalization_agent",
        }
        if task_type in task_map:
            return {"next_agent": task_map[task_type]}

    messages = state.get("messages", [])
    user_text = _extract_prompt_text(messages).lower()

    # Fast-path deterministic classification (0ms latency)
    intent = classify_intent(user_text)
    intent_map = {
        "study_planner": "study_planner_agent",
        "exam": "exam_agent",
        "coding": "coding_agent",
        "project": "project_agent",
        "document": "document_agent",
        "memory": "memory_agent",
        "audio": "audio_agent",
        "video": "video_agent",
        "study": "study_agent"
    }
    next_agent = intent_map.get(intent, "study_agent")
    return {"next_agent": next_agent}


# =========================================================================
# 2. Specialized Agent Nodes (Direct Model-Free Intelligence)
# =========================================================================

def study_planner_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    # Extract topic from prompt if pattern exists
    topic = prompt
    for prefix in ["for the topic:", "topic:", "study plan for", "plan for"]:
        if prefix in prompt.lower():
            topic = prompt.lower().split(prefix)[-1].split("\n")[0].strip().strip("'\"")
            break

    # Extract hours if mentioned
    hours = 2.0
    h_match = re.search(r"(\d+(?:\.\d+)?)\s*hours?\s+per\s+day", prompt, re.IGNORECASE)
    if h_match:
        try:
            hours = float(h_match.group(1))
        except ValueError:
            pass

    content = generate_study_plan_schedule(topic=topic or "Academic Curriculum", hours_per_day=hours)
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "study_plan", "content": content}}


def study_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    content = study_engine.process_prompt(prompt, task_type="study")
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "study", "content": content}}


def exam_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    context = state.get("context", "")

    # Extract topic from prompt
    topic = prompt
    for prefix in ["for the topic:", "topic:", "test on", "quiz on", "about"]:
        if prefix in prompt.lower():
            topic = prompt.lower().split(prefix)[-1].split("\n")[0].strip().strip("'\"")
            break

    # Extract question count
    num_q = 10
    q_match = re.search(r"(\d+)\s*(?:questions?|items?)", prompt, re.IGNORECASE)
    if q_match:
        try:
            num_q = max(1, min(50, int(q_match.group(1))))
        except ValueError:
            pass

    if context and len(context.split()) > 20:
        mcqs = generate_mcqs_from_text(context, num_questions=num_q)
        content = format_exam_material(mcqs, topic=topic or "Document Review")
    else:
        mcqs = generate_mcqs_for_topic(topic=topic or "General Science", num_questions=num_q)
        content = format_exam_material(mcqs, topic=topic or "Assessment")

    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "exam", "content": content}}


def coding_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    code_match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", prompt)
    code_snippet = code_match.group(1) if code_match else prompt

    if "teach" in prompt.lower() or "dsa" in prompt.lower():
        dsa_topic = prompt.replace("teach", "").replace("dsa", "").replace("in python", "").strip()
        content = teach_dsa_topic(dsa_topic or "Binary Search", student_code=code_snippet if code_match else "")
    elif "optimize" in prompt.lower():
        content = optimize_code_snippet(code_snippet)
    elif "explain" in prompt.lower():
        content = explain_code_snippet(code_snippet)
    else:
        content = debug_code_snippet(code_snippet)

    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "coding", "content": content}}


def project_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    content = study_engine.process_prompt(prompt, task_type="project")
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "project", "content": content}}


def document_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    context = state.get("context", "")
    content = study_engine.process_prompt(prompt, task_type="document", context=context)
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "document", "content": content}}


def audio_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    content = study_engine.process_prompt(prompt, task_type="audio")
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "audio", "content": content}}


def video_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    content = study_engine.process_prompt(prompt, task_type="video")
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "video", "content": content}}


def memory_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    content = study_engine.process_prompt(prompt, task_type="memory")
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "memory", "content": content}}


def personalization_node(state: AgentState) -> Dict[str, Any]:
    prompt = _extract_prompt_text(state.get("messages", []))
    content = (
        f"### 🎯 Personalized Learning Strategy\n\n"
        f"Based on your recent study activities for **{prompt.strip()}**:\n"
        f"- **Strengths Identified:** Core theoretical definitions and baseline concepts.\n"
        f"- **Recommended Next Steps:** Complete a 10-question mock assessment and 1 hands-on practice implementation.\n"
        f"- **Next Revision Interval:** In 24 hours (Day 2 active recall check)."
    )
    response = AIMessage(content=content)
    return {"messages": [response], "generated_content": {"type": "personalization", "content": content}}


# =========================================================================
# 3. Graph Builder with Native & Fallback Execution
# =========================================================================

class ModelFreeCompiledGraph:
    """Fallback graph execution engine when LangGraph is not installed."""
    def __init__(self):
        self.node_map = {
            "study_agent": study_node,
            "study_planner_agent": study_planner_node,
            "exam_agent": exam_node,
            "coding_agent": coding_node,
            "project_agent": project_node,
            "document_agent": document_node,
            "audio_agent": audio_node,
            "video_agent": video_node,
            "memory_agent": memory_node,
            "personalization_agent": personalization_node,
        }

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Executes router node followed by the selected specialized agent node."""
        state_copy = dict(state)
        # 1. Route
        router_res = router_node(state_copy)
        target_agent = router_res.get("next_agent", "study_agent")
        state_copy["next_agent"] = target_agent

        # 2. Execute selected agent node
        handler = self.node_map.get(target_agent, study_node)
        agent_res = handler(state_copy)

        # Merge results
        result_messages = list(state_copy.get("messages", []))
        if "messages" in agent_res:
            result_messages.extend(agent_res["messages"])

        state_copy["messages"] = result_messages
        state_copy["generated_content"] = agent_res.get("generated_content", {})
        return state_copy


def build_graph():
    if HAS_LANGGRAPH:
        workflow = StateGraph(AgentState)
        workflow.add_node("orchestrator", router_node)
        workflow.add_node("study_agent", study_node)
        workflow.add_node("study_planner_agent", study_planner_node)
        workflow.add_node("exam_agent", exam_node)
        workflow.add_node("coding_agent", coding_node)
        workflow.add_node("project_agent", project_node)
        workflow.add_node("document_agent", document_node)
        workflow.add_node("audio_agent", audio_node)
        workflow.add_node("video_agent", video_node)
        workflow.add_node("memory_agent", memory_node)
        workflow.add_node("personalization_agent", personalization_node)

        workflow.set_entry_point("orchestrator")

        def route_to_agent(state: AgentState):
            agent = state.get("next_agent", "study_agent")
            return agent if agent in SUPPORTED_AGENTS else "study_agent"

        agent_map = {agent: agent for agent in SUPPORTED_AGENTS}
        workflow.add_conditional_edges("orchestrator", route_to_agent, agent_map)

        for agent in SUPPORTED_AGENTS:
            workflow.add_edge(agent, END)

        return workflow.compile()
    else:
        return ModelFreeCompiledGraph()


app_graph = build_graph()
