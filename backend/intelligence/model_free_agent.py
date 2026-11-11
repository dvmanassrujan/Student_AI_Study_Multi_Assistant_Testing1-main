"""
Unified Model-Free Agent Orchestrator & LangChain-Compatible Adapter.
Routes academic queries to deterministic intelligence engines with zero external APIs and zero LLMs:
1. Study Planner Engine
2. Exam Coach & Quiz Generator
3. Senior Coding Mentor & DSA Lab
4. Document Intelligence & Grounded Extractive Search
5. Academic Tutor (Concept Explainer & Analogies)
6. Project Architect (System Design & Schemas)
7. Memory & Spaced Repetition Flashcards
"""

import re
import logging
from typing import Dict, Any, List, Optional, Union

from backend.intelligence.nlp import (
    normalize_text,
    tokenize_sentences,
    extract_keywords,
    classify_intent
)
from backend.intelligence.study_planner import generate_study_plan_schedule
from backend.intelligence.quiz_flashcards import (
    generate_mcqs_from_text,
    generate_mcqs_for_topic,
    format_exam_material,
    generate_flashcards,
    format_flashcard_markdown
)
from backend.intelligence.coding_mentor import (
    debug_code_snippet,
    explain_code_snippet,
    optimize_code_snippet,
    teach_dsa_topic
)
from backend.intelligence.summarizer import (
    generate_short_summary,
    generate_detailed_summary,
    generate_important_points,
    generate_definitions_lexicon,
    generate_exam_notes
)
from backend.intelligence.document_engine import (
    chunk_document,
    DocumentSearchIndex,
    answer_document_query
)

logger = logging.getLogger(__name__)


# =========================================================================
# 1. Specialized Deterministic Academic Generators
# =========================================================================

def generate_academic_explanation(query: str) -> str:
    """
    Synthesizes a structured academic tutorial for a concept using
    heuristic pedagogical decomposition (Intuition, Mechanism, Example, Summary).
    """
    clean_q = normalize_text(query).strip()
    topic = clean_q
    for prefix in ["what is", "explain", "how does", "tell me about", "teach me", "what are"]:
        if clean_q.lower().startswith(prefix):
            topic = clean_q[len(prefix):].strip().rstrip("?").strip()
            break

    title = topic.title() if topic else "Academic Concept"

    return f"""# 🎓 Academic Concept Guide: {title}

## 💡 1. Core Intuition & Overview
**{title}** is a fundamental principle in this field of study. 
At its core, it provides the underlying mechanism for understanding how components interact, transform, and achieve equilibrium or computational results.

> 🌍 **Real-World Analogy:** Think of **{title}** like an orchestrated feedback loop: inputs are received, processed according to defined rules, and transformed into predictable, verifiable outcomes.

---

## ⚙️ 2. Key Mechanisms & Principles
- **Core Definition:** The formal study and application of `{topic}` within standard academic curricula.
- **Fundamental Rule:** Actions and transformations follow conservation and systematic operational constraints.
- **Primary Utility:** Used to analyze behavior, solve domain-specific problems, and design robust scalable systems.

---

## 📚 3. High-Yield Examples & Applications
1. **Foundational Scenario:** Applying `{topic}` to initial baseline conditions allows calculation of the primary state.
2. **Advanced Application:** When scaled, it provides predictable bounds, enabling optimization and error mitigation.

---

## 🧠 4. Active Recall & Self-Test Questions
- [ ] What is the single most critical defining attribute of **{title}**?
- [ ] How does **{title}** differ from related adjacent concepts?
- [ ] In what real-world or theoretical scenario would you apply this principle?

---
*Generated deterministically by the Model-Free Academic Intelligence Engine.*"""


def generate_project_scaffold(prompt: str) -> str:
    """Generates structured software architecture and module breakdown."""
    idea = prompt.replace("project", "").strip() or "Full-Stack Application"
    title = idea.title()

    return f"""# 🏗️ System Architecture & Project Blueprint: {title}

## 🎯 1. Executive System Overview
A production-grade, modular software solution designed for scalability, maintainability, and clean separation of concerns.

---

## 🏛️ 2. Recommended Technology Stack
- **Frontend Layer:** React.js / Next.js / TypeScript with Tailwind CSS for high-performance responsive UI.
- **Backend API Layer:** Python FastAPI / Node.js with RESTful and WebSocket endpoints.
- **Database & Storage:** PostgreSQL for relational data with Redis for in-memory caching.
- **Data Integrity & Validation:** Pydantic / Zod schema validation.

---

## 📦 3. Modular Directory Structure
```text
{idea.lower().replace(" ", "_")}/
├── backend/
│   ├── api/             # Route handlers & endpoints
│   ├── core/            # Config, security, database connection
│   ├── models/          # Data schemas & ORM entities
│   ├── services/        # Business logic & algorithms
│   └── tests/           # Unit & integration test suites
├── frontend/
│   ├── components/      # Reusable UI widgets
│   ├── pages/           # Application views
│   └── styles/          # Design system & CSS
├── docs/                # API specifications & architecture diagrams
└── README.md
```

---

## 🗄️ 4. Core Database Schema Design
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    payload JSONB DEFAULT '{{}}'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🚀 5. Implementation Roadmap
1. **Phase 1 (MVP):** Database schema migration and core CRUD API routes.
2. **Phase 2 (UI Integration):** Responsive frontend connecting to API endpoints.
3. **Phase 3 (Testing & Hardening):** Automated unit tests, input validation, and deployment setup.
"""


def generate_audio_script(text: str) -> str:
    """Formats educational explanation into spoken-word script."""
    clean = normalize_text(text)
    sents = tokenize_sentences(clean)
    lines = [
        "### 🎙️ Spoken-Word Educational Audio Script\n",
        "**Host/Narrator:** Welcome back, students! Today we are diving into an important topic. Let's break it down clearly.\n"
    ]
    for s in sents[:6]:
        lines.append(f"**Narrator:** {s}\n")
    lines.append("**Narrator:** Keep practicing active recall, and I'll catch you in the next lesson!")
    return "\n".join(lines)


def generate_video_script(text: str) -> str:
    """Formats educational explanation into a scene-by-scene video script."""
    clean = normalize_text(text)
    sents = tokenize_sentences(clean)
    lines = [
        "# 🎬 Educational Video Script & Storyboard\n",
        "**Format:** Widescreen 16:9 | **Style:** Engaging Educational Explainer\n",
        "---"
    ]

    for idx, s in enumerate(sents[:4], 1):
        lines.extend([
            f"### 🎥 Scene {idx}",
            f"- **Visual Cue:** Animated diagram illustrating key concept with smooth camera pan.",
            f"- **On-Screen Graphic:** Text callout highlighting core terms.",
            f"- **Voiceover Narration:** \"{s}\"\n"
        ])

    lines.append("---\n*Storyboard generated by Model-Free Video Intelligence Engine.*")
    return "\n".join(lines)


# =========================================================================
# 2. Unified Model-Free Study Engine
# =========================================================================

class ModelFreeStudyEngine:
    """
    Central dispatcher executing intelligent deterministic study tasks
    without requiring external APIs, LLMs, or paid services.
    """

    def process_prompt(
        self,
        prompt: str,
        task_type: Optional[str] = None,
        next_agent: Optional[str] = None,
        context: str = ""
    ) -> str:
        """Processes a prompt and dispatches to the corresponding deterministic engine."""
        clean_prompt = prompt.strip() if prompt else ""

        # Determine target intent
        target = "study"
        if next_agent:
            target = next_agent.replace("_agent", "")
        elif task_type:
            target = task_type
        else:
            target = classify_intent(clean_prompt)

        # 1. Study Planner
        if target in ["study_planner", "study_plan", "planner"]:
            topic = clean_prompt
            match = re.search(r"(?:topic|plan for|schedule for|about)\s+['\"]?([^'\"\n,]+)['\"]?", clean_prompt, re.IGNORECASE)
            if match:
                topic = match.group(1).strip()
            return generate_study_plan_schedule(topic=topic, level="Beginner", duration="1 Week", hours_per_day=2.0)

        # 2. Exam Preparation & Quizzes
        elif target in ["exam", "exam_prep", "quiz"]:
            if context and len(context.split()) > 15:
                mcqs = generate_mcqs_from_text(context, num_questions=8)
                return format_exam_material(mcqs, topic="Uploaded Document Review")
            else:
                topic = clean_prompt
                match = re.search(r"(?:topic|about|for)\s+['\"]?([^'\"\n,]+)['\"]?", clean_prompt, re.IGNORECASE)
                if match:
                    topic = match.group(1).strip()
                mcqs = generate_mcqs_for_topic(topic=topic, num_questions=8)
                return format_exam_material(mcqs, topic=topic)

        # 3. Coding Mentor & DSA Lab
        elif target in ["coding", "coding_lab"]:
            code_match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", clean_prompt)
            code_snippet = code_match.group(1) if code_match else clean_prompt

            if "teach" in clean_prompt.lower() or "dsa" in clean_prompt.lower():
                dsa_topic = clean_prompt.replace("teach", "").replace("dsa", "").replace("in python", "").strip()
                return teach_dsa_topic(dsa_topic or "Binary Search")
            elif "optimize" in clean_prompt.lower():
                return optimize_code_snippet(code_snippet)
            elif "explain" in clean_prompt.lower():
                return explain_code_snippet(code_snippet)
            else:
                return debug_code_snippet(code_snippet)

        # 4. Document Intelligence
        elif target in ["document", "doc"]:
            doc_text = context if context else clean_prompt
            if "short summary" in clean_prompt.lower():
                return generate_short_summary(doc_text)
            elif "important points" in clean_prompt.lower() or "takeaway" in clean_prompt.lower():
                return generate_important_points(doc_text)
            elif "definition" in clean_prompt.lower() or "lexicon" in clean_prompt.lower():
                return generate_definitions_lexicon(doc_text)
            elif "exam notes" in clean_prompt.lower():
                return generate_exam_notes(doc_text)
            else:
                chunks = chunk_document(doc_text)
                index = DocumentSearchIndex(chunks)
                return answer_document_query(clean_prompt, index)

        # 5. Project Builder & Architect
        elif target in ["project", "architecture"]:
            return generate_project_scaffold(clean_prompt)

        # 6. Memory & Flashcards
        elif target in ["memory", "flashcard", "flashcards"]:
            cards = generate_flashcards(clean_prompt, num_cards=6, is_raw_text=bool(context))
            return format_flashcard_markdown(cards, topic="Core Concepts")

        # 7. Audio Learning Script
        elif target == "audio":
            return generate_audio_script(clean_prompt)

        # 8. Video Storyboard Script
        elif target == "video":
            return generate_video_script(clean_prompt)

        # 9. Default: Academic Tutor Explainer
        else:
            return generate_academic_explanation(clean_prompt)


# Singleton instance
study_engine = ModelFreeStudyEngine()


# =========================================================================
# 3. LangChain-Compatible Model-Free Adapter
# =========================================================================

class ModelFreeMessage:
    """Lightweight drop-in replacement for LangChain AIMessage."""
    def __init__(self, content: str):
        self.content = content
        self.type = "ai"

    def __repr__(self):
        return f"AIMessage(content={self.content[:40]!r}...)"


class ModelFreeLLM:
    """
    Drop-in replacement for ChatOllama / LangChain BaseChatModel.
    Provides identical interface (`invoke`, `__call__`) without requiring
    Ollama, local LLM weights, or external APIs.
    """

    def __init__(self, model_name: str = "model-free-engine-v1", temperature: float = 0.0):
        self.model_name = model_name
        self.temperature = temperature

    def invoke(self, messages: Any, **kwargs) -> ModelFreeMessage:
        """Executes model-free intelligence on the provided messages."""
        prompt_text = ""
        context_text = ""
        task_type = None
        next_agent = None

        if isinstance(messages, list):
            for m in reversed(messages):
                content = getattr(m, "content", "")
                if not content and isinstance(m, dict):
                    content = m.get("content", "")

                if getattr(m, "type", "") == "human" or getattr(m, "role", "") == "user":
                    prompt_text = str(content)
                    break
            # Collect any system messages for context
            for m in messages:
                if getattr(m, "type", "") == "system":
                    context_text += str(getattr(m, "content", "")) + "\n"
        elif isinstance(messages, str):
            prompt_text = messages
        else:
            prompt_text = str(messages)

        # Extract explicit router cues if present
        if "next_agent" in kwargs:
            next_agent = kwargs["next_agent"]
        if "task_type" in kwargs:
            task_type = kwargs["task_type"]

        response_content = study_engine.process_prompt(
            prompt=prompt_text,
            task_type=task_type,
            next_agent=next_agent,
            context=context_text
        )

        return ModelFreeMessage(content=response_content)

    def stream(self, messages: Any, **kwargs):
        """Yields response content for streaming compatibility."""
        res = self.invoke(messages, **kwargs)
        yield res

    def __call__(self, messages: Any, **kwargs) -> ModelFreeMessage:
        return self.invoke(messages, **kwargs)

