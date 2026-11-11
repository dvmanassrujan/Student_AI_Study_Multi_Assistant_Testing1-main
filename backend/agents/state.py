"""
Agent State Definition for Multi-Agent Orchestrator.
Supports both native LangGraph and model-free fallback environments.
"""

from typing import TypedDict, List, Dict, Any, Optional

try:
    from typing import Annotated
    from langchain_core.messages import BaseMessage
    from langgraph.graph.message import add_messages
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False

if HAS_LANGGRAPH:
    class AgentState(TypedDict):
        messages: Annotated[list[BaseMessage], add_messages]
        context: str
        task_type: str
        metadata: Dict[str, Any]
        next_agent: str
        errors: List[str]
        current_topic: str
        learning_history: List[Dict[str, Any]]
        generated_content: Dict[str, Any]
else:
    class AgentState(TypedDict, total=False):
        messages: List[Any]
        context: str
        task_type: str
        metadata: Dict[str, Any]
        next_agent: str
        errors: List[str]
        current_topic: str
        learning_history: List[Dict[str, Any]]
        generated_content: Dict[str, Any]
