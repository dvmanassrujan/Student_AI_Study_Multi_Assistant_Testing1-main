---
title: Student AI Study Assistant - Model-Free Intelligence Engine
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# 🎓 AI Multi-Study Assistant & Educational Production Platform
### 🧠 100% Model-Free, API-Free, Cost-Free Deterministic Intelligence Engine

A comprehensive educational study platform featuring a fully offline, deterministic **Model-Free Intelligence Engine**, a 16-agent multi-agent study workflow, an 8-stage document intelligence pipeline, an interactive coding lab, and an autonomous educational production studio.

---

## 🚫 Zero-Model Guarantee & Strict Principles

This project has been engineered to run with **zero external dependencies on neural models or paid cloud APIs**:
- ❌ **No Ollama or local LLMs** (no Llama, Mistral, Phi, DeepSeek, etc.).
- ❌ **No Cloud AI APIs** (no OpenAI, Gemini, Groq, Anthropic Claude, etc.).
- ❌ **No Pretrained Embedding Models** (no Sentence-Transformers, HuggingFace downloads).
- ❌ **No Paid Subscriptions or API Keys**.
- ❌ **No Hallucinations**: Grounded document answering with explicit insufficiency warnings.
- ✅ **Pure Python Algorithms**: Mathematical formulas, graph theory (TextRank PageRank), information retrieval (Okapi BM25 + TF-IDF), AST static analysis, and deterministic NLP.
- ✅ **Sub-Millisecond Execution**: Instantaneous local responses without network latency or GPU requirements.

---

## 🏛️ System Architecture

```
                                  [ User Interface: Gradio Blocks (Tabbed UI) ]
                                                        │
                  ┌─────────────────────────────────────┴─────────────────────────────────────┐
                  │                                                                           │
    [ Division A: Educational Study Assistant ]                             [ Division B: Educational Studio ]
                  │                                                                           │
   ┌──────────────┼──────────────┬──────────────┐                             ┌───────────────┼───────────────┐
   ▼              ▼              ▼              ▼                             ▼               ▼               ▼
[Study Planner] [Coding Lab]   [Exam Prep]   [Doc Intelligence]         [Video Studio]  [Cover Studio]  [Audio Engine]
- Pomodoro      - AST Analyzer - MCQs / Cloze - Multi-Format Parser     - Auto-EDL      - 1080x1920     - Edge-TTS /
- Ebbinghaus    - Cyclomatic   - Flashcards  - BM25 + TF-IDF Hybrid    - Subtitles     - Reel Cover      pyttsx3
- Milestones    - Anti-Patterns- Auto-Grader - Strict Anti-Hallucination- 9:16 Format  - Safe Zones    - Multilingual
```

### 🧠 Core Subsystems of `backend/intelligence/`

| Module | Core Techniques & Algorithms | Key Capabilities |
| :--- | :--- | :--- |
| **`nlp.py`** | Abbreviation-aware segmentation, Porter Stemmer, RAKE keyword scoring, TF-IDF ($L_2$ norm), Okapi BM25 ($k_1=1.5, b=0.75$), Cosine similarity | Text normalization, tokenization, stop-word removal, vocabulary indexing, rule-based intent classification |
| **`document_engine.py`** | Multi-format parsers (PDF, DOCX, TXT, CSV, MD), heading-aware sliding-window chunking, hybrid BM25 + TF-IDF search | Passages extraction, source-grounded Q&A with confidence cutoff, document-based question & flashcard generator |
| **`summarizer.py`** | TextRank graph centrality (PageRank power iteration with $d=0.85$, convergence threshold $10^{-4}$) | Short summaries, detailed thematic summaries, chapter-by-chapter breakdowns, key takeaways, definition lexicon, exam notes |
| **`quiz_flashcards.py`** | Definitional regex mining, distractor generation, Cloze fill-in-the-blank, difficulty calibration | 4-option MCQs with explanations, spaced-repetition flashcards, student exam formatting, auto-grader engine |
| **`study_planner.py`** | Pomodoro time-blocking (25m study / 5m break), Ebbinghaus spaced revision intervals ($D+1, D+3, D+7, D+14, D+30$), topic difficulty multipliers | Personalized daily and weekly timetables, exam countdowns, milestone checklists, dynamic completion tracking |
| **`coding_mentor.py`** | Python `ast` parse tree walker, McCabe cyclomatic complexity, nesting depth calculation, anti-pattern detection | Visual caret error pointer, mutable default & bare except alerts, performance optimization suggestions, verified DSA masterclass |
| **`model_free_agent.py`** | Unified LangChain-compatible `ModelFreeLLM` and `ModelFreeStudyEngine` | Transparent drop-in replacement for LangGraph agent nodes and direct chat invocations |

---

## 🚀 Key Features

### 1. Model-Free Academic Q&A & Socratic Tutoring
- High-yield concept breakdowns with intuitive analogies, mathematical foundations, practical examples, and common pitfalls.
- Deterministic intent classification routes queries to the optimal intelligence module automatically.

### 2. Multi-Format Document Intelligence & RAG
- **File Support**: PDF (PyMuPDF with pure-Python stream fallback), DOCX (python-docx with ZIP/XML fallback), TXT, Markdown, and CSV (formatted tables).
- **Hybrid Retrieval**: Combines Okapi BM25 frequency weighting with sublinear TF-IDF cosine similarity.
- **Strict Anti-Hallucination**: If the document lacks sufficient factual support for a query, the engine explicitly alerts the user rather than fabricating facts.

### 3. TextRank Extractive Summarizer
- Computes sentence saliency graphs using token overlap similarity:
  $$\text{Similarity}(S_i, S_j) = \frac{|S_i \cap S_j|}{\log(|S_i|) + \log(|S_j|)}$$
- Generates executive short summaries, detailed structured takeaways, chapter summaries, and exam-focused revision sheets.

### 4. Interactive Quiz & Flashcard Generator
- Generates 4-option MCQs with plausible distractors mined from document keywords.
- Cloze fill-in-the-blank questions and Anki-ready flashcards.
- Built-in scoring engine evaluates submitted answers and calculates mastery grades ($A$ through $D$).

### 5. Mathematical Study Planner
- Implements Ebbinghaus forgetting curve spaced repetition intervals.
- Computes Pomodoro sessions per day based on available study hours and subject difficulty (1.0x Beginner, 1.3x Intermediate, 1.6x Advanced).
- Tracks progress dynamically with completion status and weekly milestones.

### 6. Senior Python Coding Mentor
- AST static analysis parses Python code and reports exact line and column numbers with visual caret error pointers (`^`).
- Computes McCabe cyclomatic complexity and maximum nesting depth.
- Detects anti-patterns: mutable default arguments (`def f(x=[])`), bare `except:`, and identity comparisons (`x == None`).
- Includes a verified Data Structures and Algorithms (DSA) masterclass covering Binary Search, Two Pointers, Sliding Window, DFS/BFS, Dynamic Programming, and more.

---

## 🛠️ Environment Setup & Installation

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 (64-bit)
- Optional: [FFmpeg and FFprobe](https://ffmpeg.org/download.html) in system PATH (for media studio operations)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/Student_AI_Study_Multi_Assistant.git
cd Student_AI_Study_Multi_Assistant

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration (`.env`)
The system defaults to model-free operation automatically. You can inspect or customize `.env`:
```ini
MODEL_PROVIDER=model_free
MODEL_NAME=model-free-engine-v1
DATABASE_URL=sqlite:///data/app.db
MAX_UPLOAD_SIZE_MB=500
LOG_LEVEL=INFO
```

---

## 🧪 Verification & Automated Testing

### Run Complete System Diagnostics
```bash
# Verify all 6 Model-Free Intelligence Engine subsystems
python scripts/check_intelligence_engine.py

# Verify system environment and optional media dependencies
python scripts/check_environment.py

# Verify LLM compatibility layer
python scripts/check_ollama.py
```

### Run Pytest Test Suite
```bash
pytest tests/
```
**Verified Test Results**:
- `tests/test_model_free_intelligence.py`: **19/19 PASSED** (NLP, BM25, TF-IDF, chunking, grounded QA, TextRank, MCQs, study planner, AST coding mentor).
- `tests/test_three_agents.py`: **12/12 PASSED** (Agent states, study agent, coding agent, exam agent).
- `tests/test_llama32_ollama_integration.py`: **5/5 PASSED** (ModelFreeLLM compatibility, message invocation, streaming).
- `tests/test_document_processor.py`: **9/9 PASSED** (8-stage pipeline, semantic chunking, SQLite records, diff detection).
- `tests/test_ai_chat_assistant.py`: **3/3 PASSED** (Gradio chat handler, session state, clear).
- `tests/test_port_conflict_resolution.py`: **6/6 PASSED** (Socket availability, automatic port fallback).

---

## 🖥️ Launching the Application

### 1. Launch Gradio Dashboard
```bash
python frontend/app.py
```
Open your browser to: **`http://localhost:7860`**
- **Tab 1: AI Multi-Study Assistant**: Socratic tutor, concept explainer, and Q&A.
- **Tab 2: Smart Study Planner**: Personalized Pomodoro schedules and Ebbinghaus revision curves.
- **Tab 3: AI Coding Lab & Mentor**: AST static analysis, syntax debugger, and DSA tutor.
- **Tab 4: Exam & Quiz Generator**: MCQs with distractors, flashcards, and test grader.
- **Tab 5: Document Intelligence**: Grounded multi-format document search and summarization.
- **Tab 6: Social Media Analytics**: Engagement rate formulas and sentiment breakdown.
- **Tab 7: Educational Video & Notes Studio**: Autonomous video reel and notebook generator.

### 2. Launch FastAPI Backend (Optional)
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Access interactive API documentation at: **`http://localhost:8000/docs`**

---

## 📄 License
This project is licensed under the MIT License.
