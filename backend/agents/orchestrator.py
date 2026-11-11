from typing import Literal
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from backend.agents.state import AgentState
from backend.core.llm import get_llm
import json
import logging

logger = logging.getLogger(__name__)

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

def router_node(state: AgentState):
    """Orchestrator to route to the correct agent based on the task"""
    # 1. Fast-path: Explicit agent or task_type already requested in state
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
    
    # Extract recent user text for fast-path heuristic
    last_user_text = ""
    for m in reversed(messages):
        if isinstance(m, HumanMessage) or getattr(m, "type", "") == "human":
            last_user_text = str(getattr(m, "content", "")).lower()
            break

    # Fast-path 3: High-confidence keyword heuristics (0ms routing latency, eliminates ~45s LLM router delay)
    if any(w in last_user_text for w in ["study plan", "study schedule", "timetable", "revision plan", "hours per day", "study roadmap"]):
        return {"next_agent": "study_planner_agent"}
    elif any(w in last_user_text for w in ["exam", "quiz", "mock test", "test questions", "mcq", "multiple choice", "practice questions"]):
        return {"next_agent": "exam_agent"}
    elif any(w in last_user_text for w in ["debug", "def ", "function", "class ", "python", "java", "c++", "javascript", "algorithm", "dsa", "syntax error", "runtime error", "leetcode", "code"]):
        return {"next_agent": "coding_agent"}
    elif any(w in last_user_text for w in ["project idea", "project architecture", "tech stack", "build an app", "module breakdown"]):
        return {"next_agent": "project_agent"}
    elif any(w in last_user_text for w in ["flashcard", "flashcards", "mnemonic", "spaced repetition", "anki", "memorize"]):
        return {"next_agent": "memory_agent"}
    elif any(w in last_user_text for w in ["video script", "storyboard", "scene 1", "visual cue", "create a video script"]):
        return {"next_agent": "video_agent"}
    elif any(w in last_user_text for w in ["audio script", "podcast script", "voiceover", "spoken explanation"]):
        return {"next_agent": "audio_agent"}
    elif any(w in last_user_text for w in ["document", "pdf", "docx", "summarize notes", "summarize this text"]):
        return {"next_agent": "document_agent"}
    elif not state.get("use_llm_router", False):
        # Default fast path for conversational assistant (explaining concepts, general Q&A, greetings)
        return {"next_agent": "study_agent"}

    llm = get_llm()
    system_prompt = """You are the Orchestrator Agent for an AI Student Assistant.
Your job is to analyze the user's request and determine which specialized agent should handle it.
Available Agents:
- study_planner_agent: Creates structured daily/weekly study plans, timetables, and learning milestones.
- study_agent: Explains concepts, teaches topics simply, and generates summaries.
- exam_agent: Creates quizzes, mock tests, important questions, and exam preparation.
- coding_agent: Debugs code, explains algorithms, writes code, DSA trainer.
- project_agent: Generates project ideas, architectures, documentation.
- document_agent: Analyzes uploaded documents, text files, and notes.
- audio_agent: Text to speech and audio learning assistant.
- video_agent: Educational video script and explanation generator.
- memory_agent: Flashcards, memory techniques, spaced repetition tracking.
- personalization_agent: Progress tracking, weak topics, personalized schedules.

Respond with ONLY a JSON object containing the `next_agent` key. Example: {"next_agent": "study_agent"}"""
    
    try:
        response = llm.invoke([SystemMessage(content=system_prompt)] + messages)
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        elif "{" in content and "}" in content:
            start = content.find("{")
            end = content.rfind("}") + 1
            content = content[start:end].strip()
        
        data = json.loads(content)
        next_agent = data.get("next_agent", "study_agent")
        if next_agent not in SUPPORTED_AGENTS:
            next_agent = "study_agent"
    except Exception as e:
        logger.warning(f"Router parsing failed ({e}). Defaulting to study_agent.")
        next_agent = "study_agent"
        
    return {"next_agent": next_agent}

def study_planner_node(state: AgentState):
    llm = get_llm()
    system_prompt = (
        "You are an expert AI Study Planner and Academic Strategist. "
        "Create personalized, realistic, and highly structured day-by-day or week-by-week study plans tailored to the student's level, timeline, and available hours. "
        "Include specific topics, proven learning techniques (Active Recall, Spaced Repetition, Pomodoro), actionable milestones, practice exercises, and review checkpoints. Format cleanly in Markdown."
    )
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "study_plan", "content": response.content}}

def study_node(state: AgentState):
    llm = get_llm()
    system_prompt = (
        "You are an expert AI Student Assistant and Dedicated Academic Tutor. "
        "Provide helpful, accurate, and engaging explanations tailored to the student's questions. "
        "Break down complex concepts step-by-step with intuitive analogies and concrete real-world examples. "
        "Answer direct questions thoroughly, provide study tips, and format your response cleanly in Markdown."
    )
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "study", "content": response.content}}

def exam_node(state: AgentState):
    llm = get_llm()
    system_prompt = (
        "You are an expert AI Exam Preparation Coach and Assessment Specialist. "
        "Your objective is to generate rigorous, high-yield educational exam materials, mock tests, quizzes, and revision questions. "
        "Structure mock tests with clear question numbering, 4 distinct options (A, B, C, D) for multiple choice, and provide an Answer Key with detailed explanations at the end. "
        "Ensure questions accurately test conceptual understanding, critical thinking, and problem solving. Format beautifully in Markdown."
    )
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "exam", "content": response.content}}

def coding_node(state: AgentState):
    llm = get_llm()
    system_prompt = (
        "You are a Senior Software Engineer and Expert Coding Mentor. "
        "Analyze, debug, explain, and optimize code with surgical precision. "
        "Always provide corrected, production-ready code snippets with comments, explain the underlying logic and bugs step-by-step, "
        "and analyze Time and Space Complexity (Big-O notation). Format code cleanly in Markdown code blocks."
    )
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "coding", "content": response.content}}

def project_node(state: AgentState):
    llm = get_llm()
    system_prompt = "You are a Project Guide. Help design architecture, create module breakdowns, and documentation."
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "project", "content": response.content}}

def document_node(state: AgentState):
    llm = get_llm()
    system_prompt = "You are a Document Analysis Specialist. Summarize, extract key takeaways, and answer queries about documents."
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "document", "content": response.content}}

def audio_node(state: AgentState):
    llm = get_llm()
    system_prompt = "You are an Audio Learning Assistant. Format explanations into clear spoken-word scripts."
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "audio", "content": response.content}}

def video_node(state: AgentState):
    llm = get_llm()
    system_prompt = "You are a Video Script Creator. Turn explanations into structured video scripts with visual cues."
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "video", "content": response.content}}

def memory_node(state: AgentState):
    llm = get_llm()
    system_prompt = "You are a Memory & Flashcard Expert. Create spaced repetition flashcards and mnemonics."
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "memory", "content": response.content}}

def personalization_node(state: AgentState):
    llm = get_llm()
    system_prompt = "You are a Personalized Learning Coach. Track learning progress and recommend tailored study schedules."
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "generated_content": {"type": "personalization", "content": response.content}}

# Build Graph
def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add all nodes
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
    
    # Set entry point
    workflow.set_entry_point("orchestrator")
    
    # Conditional Edges
    def route_to_agent(state: AgentState):
        agent = state.get("next_agent", "study_agent")
        return agent if agent in SUPPORTED_AGENTS else "study_agent"
        
    agent_map = {agent: agent for agent in SUPPORTED_AGENTS}
    workflow.add_conditional_edges("orchestrator", route_to_agent, agent_map)
    
    # End edges for all nodes
    for agent in SUPPORTED_AGENTS:
        workflow.add_edge(agent, END)
        
    return workflow.compile()

app_graph = build_graph()

