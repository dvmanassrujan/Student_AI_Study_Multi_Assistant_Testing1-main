---
title: Student AI Study Assistant - DeepSeek-Coder & Hybrid Intelligence
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# 🎓 AI Multi-Study Assistant & Educational Production Platform
### ⚡ Powered by DeepSeek-Coder:1.3b (Local Ollama) & Hybrid Deterministic Engine
### 🎨 Refined Professional Medium-Dark Blue UI/UX Theme

A state-of-the-art educational study platform and autonomous coding laboratory featuring a **Modern Medium-Dark Blue Design System**, native **DeepSeek-Coder:1.3b** local Ollama inference, a deterministic fallback intelligence engine, a multi-agent orchestrator, grounded document intelligence, and an educational production studio.

---

## 🎨 Professional Medium-Dark Blue UI/UX Design System

The user interface has been transformed into an accessible, sleek **Medium-Dark Blue Theme** engineered for optimal legibility and high contrast:

| Layer / Element | Color Code | Purpose & Accessibility |
| :--- | :--- | :--- |
| **App Canvas Background** | `#0c1526` | Deep navy base providing calm, fatigue-free study sessions |
| **Card / Panel Surfaces** | `#13223f` / `#111f35` | Elevated container cards with soft drop shadows |
| **Component Borders** | `#274170` | Crisp 1px structural separation between panels |
| **Primary Headings & Titles** | `#FFFFFF` | Maximum contrast crisp white typography |
| **Subheadings & Labels** | `#F8FAFC` / `#E2E8F0` | High-visibility text with zero overlapping |
| **Muted & Meta Info** | `#CBD5E1` / `#94A3B8` | Accessible secondary text meeting WCAG AAA contrast |
| **Primary Action Accent** | `#2563eb` / `#1d4ed8` | Vibrant royal blue interactive buttons |
| **Telemetry & Live Badges** | `#38bdf8` / `#10B981` | Electric cyan highlights and glowing status pulses |

---

## ⚡ Dual-Engine Intelligence Architecture

The platform operates on a **zero-risk dual-engine architecture**:
1. **Primary Model**: **`deepseek-coder:1.3b`** running on your local Ollama server (`http://localhost:11434`):
   - Fast, local, private, and 100% cost-free inference.
   - Specialized in Python code analysis, Data Structures & Algorithms, and step-by-step academic problem solving.
2. **Instant Fallback Engine**: **Deterministic Python Intelligence Engine**:
   - If Ollama is offline or stopped, the system automatically routes to pure Python algorithms without crashing or throwing errors.
   - TextRank graph summarization (PageRank power iteration), Okapi BM25 + TF-IDF information retrieval, AST static code analysis, and Ebbinghaus study scheduling.

```
                              [ User Interface: Medium-Dark Blue Gradio Blocks ]
                                                      │
                                          [ Dual-Engine Orchestrator ]
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
            [ Local Ollama Server ]                                     [ Local Fallback Engine ]
          - Model: deepseek-coder:1.3b                                - 100% Offline Python NLP
          - Port: http://localhost:11434                             - Sub-millisecond Execution
          - Zero Cloud API Dependency                                 - AST Analysis & BM25 Search
```

---

## 🏛️ Comprehensive Feature Modules

### 1. 🏠 Neural Nexus – AI Command Center
- Live telemetry pill displaying real-time engine health, active port, and loaded model (`deepseek-coder:1.3b`).
- Instant quick-action launchpad for rapid conceptual breakdown, study schedule generation, and code reviews.

### 2. 📚 Academic Tutor & Socratic Explainer
- Deep conceptual tutorials structured with pedagogical intuition, core mechanisms, verified examples, and summary takeaways.
- Natural language intent classification automatically routes complex questions.

### 3. 💻 Senior Python Coding Lab & AST Mentor
- Static syntax validation using Python's `ast` parser with visual error pointers (`^`).
- Cyclomatic complexity calculation and anti-pattern alerts (mutable default arguments, bare `except:`, identity checks).
- Full Data Structures & Algorithms (DSA) masterclass spanning Binary Search, Two Pointers, Dynamic Programming, and Graph Traversals.

### 4. 📝 Grounded Document Intelligence (PDF, DOCX, TXT, CSV, MD)
- Multi-format document parser with sliding-window chunking.
- Hybrid BM25 + TF-IDF ranking with cosine similarity.
- **Strict Anti-Hallucination**: Answers are strictly grounded in retrieved passages; explicitly signals when document context is insufficient.

### 5. 🎯 Exam Coach & Spaced-Repetition Flashcards
- Automatic 4-option MCQ generator with plausible distractors mined from source keywords.
- Cloze fill-in-the-blank assessment templates and interactive answer grading ($A$ through $D$).
- Anki-compatible flashcard extraction for rapid revision.

### 6. 📅 Intelligent Study Planner
- Implements Ebbinghaus forgetting curve spaced intervals ($D+1, D+3, D+7, D+14, D+30$).
- Pomodoro time-blocking (25m study / 5m break) with subject difficulty multipliers.
- Dynamic completion tracking and milestone checklists.

### 7. 🎬 Educational Production Studio
- Auto-EDL generation for 9:16 vertical video reels (1080x1920) with subtitle burn-in.
- Multi-concept thumbnail generation and social media analytics dashboard.

---

## 🛠️ Quick Start & Installation

### 1. Prerequisites
- Python 3.10 - 3.14 (64-bit)
- [Ollama](https://ollama.com/) (for running `deepseek-coder:1.3b`)

### 2. Pull the DeepSeek-Coder Model
```bash
ollama pull deepseek-coder:1.3b
ollama serve
```

### 3. Clone & Install Dependencies
```bash
git clone https://github.com/dvmanassrujan/Student_AI_Study_Multi_Assistant_Testing1-main.git
cd Student_AI_Study_Multi_Assistant_Testing1-main

python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # Linux/macOS

pip install -r requirements.txt
```

### 4. Environment Configuration (`.env`)
```ini
MODEL_PROVIDER=ollama
MODEL_NAME=deepseek-coder:1.3b
OLLAMA_MODEL=deepseek-coder:1.3b
OLLAMA_BASE_URL=http://localhost:11434
```

### 5. Run the Application
```bash
python app.py
```
Open your browser to: **`http://localhost:7860`**

---

## 🧪 Verification & Diagnostics

```bash
# Verify Ollama server and deepseek-coder:1.3b inference
python scripts/check_ollama.py

# Run complete unit and integration test suite
python -m unittest discover tests
```

---

## 📄 License
This project is licensed under the MIT License.
