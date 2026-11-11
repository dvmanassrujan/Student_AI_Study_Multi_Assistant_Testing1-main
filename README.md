<<<<<<< HEAD
---
title: Student AI Assistant
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# 🎓 AI Multi-Study Assistant & Autonomous Educational Production Platform

Enterprise Multi-Agent Student AI Assistant, 16-Stage Autonomous Educational Video Editing Studio, Multilingual Subtitles/Dubbing, and Real-Time Document Intelligence Pipeline powered by local **Meta Llama 3.2 (`llama3.2:latest`)** using **Ollama**.

---

## 🏛️ System Architecture Overview

The platform operates two core divisions alongside the full existing educational multi-agent suite:

```
                                  [ User Interface: Gradio Blocks ]
                                                  │
                 ┌────────────────────────────────┴────────────────────────────────┐
                 │                                                                 │
     [ Division A: Educational Study Multi-Assistant ]          [ Division B: Video Production Studio ]
                 │                                                                 │
   ┌─────────────┼─────────────┐                             ┌─────────────────────┼─────────────────────┐
   ▼             ▼             ▼                             ▼                     ▼                     ▼
[Study Planner] [Coding Lab]  [Exam Prep]               [16-Stage Editor]      [Cover Generator]    [Handwritten Notes]
- LangGraph     - DSA Tutor   - Mock Tests              - Silence Removal      - 1080x1920 Vertical  - Ruled A4 Pages
- Socratic      - Debugger    - Flashcards              - Multilingual Subs    - Safe Zone Compliant - Formula Formatting
- Roadmaps      - Optimization- Feedback                - 9:16 Reel (<=60s)    - Dynamic Gradients   - Multi-Page PDF
```

### 16-Agent Modular Architecture
1. **Orchestrator Agent**: Master task scheduler and stage dependency resolver with Meta Llama 3.2 JSON routing.
2. **Study Agent**: Socratic teaching, concept breakdowns, and personalized curriculum schedules.
3. **Coding Agent**: Senior code mentor, debugging, algorithmic complexity analysis, and DSA tutor.
4. **Exam Agent**: Mock tests, quizzes, and predicted high-yield examination questions.
5. **Project Agent**: Architecture blueprints, system schemas, and step-by-step engineering plans.
6. **Document Agent**: 8-stage document parser, semantic chunker, and dense vector retrieval (RAG).
7. **Audio Agent**: Multilingual Edge-TTS voice synthesis engine.
8. **Video Understanding Agent**: FFprobe media stream inspection and scene transition detection.
9. **Editing Planner Agent**: Validated Edit Decision List (EDL) generator.
10. **Caption Translation Agent**: Multilingual subtitle generator across 12 languages.
11. **TTS Agent**: Multilingual speech dubbing engine.
12. **Animation Agent**: Contextual educational badges and diagrams.
13. **Cover Generator Agent**: 1080×1920 vertical Reel cover compositor with safe zone margins.
14. **Study Notes Agent**: Authentic cream-ruled A4 notebook notes generator with multi-page PDF compilation.
15. **Reel Generation Agent**: Vertical 9:16 Instagram Reel generator strictly validated to $\le 60.0$ seconds.
16. **Quality Assurance Agent**: Pre-export media and duration verification engine.

---

## 🚀 Key Features

### Division A — Educational Multi-Study Assistant & Social Media Intelligence
- **Meta Llama 3.2:latest via Ollama**: Low-latency, high-accuracy inference running locally at `http://localhost:11434`.
- **AI Study Planner & Exam Prep**: Dynamic daily/weekly schedules, flashcards, quizzes, and mock tests with instant score prediction.
- **AI Coding Lab & DSA Mentor**: In-depth debugging, code optimization, and algorithmic explanations.
- **Strict Social Media Metric Calculations**:
  - Like Rate = $\frac{\text{likes}}{\text{reach}} \times 100$
  - Comment Rate = $\frac{\text{comments}}{\text{reach}} \times 100$
  - Save Rate = $\frac{\text{saves}}{\text{reach}} \times 100$
  - Share Rate = $\frac{\text{shares}}{\text{reach}} \times 100$
  - Overall Engagement Rate = $\frac{\text{likes} + \text{comments} + \text{shares} + \text{saves}}{\text{reach}} \times 100$
- **3-Class Comment Sentiment Classification**: Classifies audience comments into **Positive**, **Negative**, and **Neutral** categories with percentage distribution.
- **Audience Feedback Intelligence**: Highlights top praised elements, audio/caption complaints, pacing issues, and tutorial requests.

---

## 🛠️ Environment Setup & Installation

### 1. Prerequisites
- Python 3.11, 3.12, or 3.13 (64-bit)
- [Ollama](https://ollama.ai) installed and running locally
- [FFmpeg and FFprobe](https://ffmpeg.org/download.html) in system PATH (recommended for full video encoding)

### 2. Pull Required Ollama LLM
```bash
ollama pull llama3.2:latest
ollama serve
```

### 3. Install Dependencies
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configuration (`.env`)
Create `.env` using `.env.example`:
```ini
MODEL_NAME=llama3.2:latest
OLLAMA_MODEL=llama3.2:latest
OLLAMA_BASE_URL=http://localhost:11434

LLM_TEMPERATURE=0.3
LLM_TOP_P=0.9
LLM_REPEAT_PENALTY=1.1
LLM_NUM_CTX=8192
LLM_SEED=42
LLM_TIMEOUT=300

YOUTUBE_API_KEY=
DATABASE_URL=sqlite:///data/app.db
MAX_UPLOAD_SIZE_MB=500
MAX_VIDEO_DURATION_MINUTES=120
MAX_CONCURRENT_JOBS=1
DEFAULT_OUTPUT_LANGUAGE=en
LOG_LEVEL=INFO
```

---

## 🧪 Diagnostic Scripts & Automated Testing

### Diagnostic Scripts
```bash
# Verify system environment and Python libraries
python scripts/check_environment.py

# Verify Ollama server connectivity and llama3.2:latest model
python scripts/check_ollama.py

# Verify FFmpeg and FFprobe binaries
python scripts/check_ffmpeg.py
```

### Running the Test Suite
```bash
pytest tests/
```
**Verified Test Results**:
- `tests/test_llama32_ollama_integration.py`: 6/6 passed (Ollama server connection, ChatOllama instantiation, live inference, LangGraph router node, agent synthesis).
- `tests/test_document_processor.py`: 9/9 passed (8-stage monotonic progress bar, status monitor card rendering, semantic chunking, dense vector embeddings, versioned editing & diff detection, safe cancellation, FastAPI endpoints).
- `tests/test_youtube_analyzer.py`: 10/10 passed (oEmbed extraction, duration parsing, sentiment breakdown, report export).
- `tests/test_video_editor_studio.py`: 6/6 passed (video inspection, pause detection, thumbnail rendering, EDL generation).

---

## 📑 Section 26: Document Processing Progress Bar & Real-Time Status Monitor

The platform provides a high-reliability, asynchronous **Document Intelligence Workspace** integrated into Tab 7 of the Gradio application and backed by FastAPI background endpoints.

### 1. 8-Stage Monotonic Processing Pipeline
Every document undergoes a measurable, non-fabricated 8-stage intelligence workflow:
1. **Uploading & Validating Document Format/Size (10%)**: Validates file integrity, magic bytes, and size bounds (PDF, DOCX, PPTX, TXT).
2. **Extracting Text, Structure, and Tables (25%)**: Multimodal text extraction parsing headers, paragraphs, and tabular structures.
3. **Cleaning, Normalizing, and Deduplicating (35%)**: Removes irregular line breaks, excessive whitespace, and repetitive segments.
4. **Splitting into Semantic Chunks with Overlap (45%)**: Generates semantic paragraph chunks with 10% character overlap to preserve context across boundaries.
5. **Generating Vector Embeddings (60%)**: Produces dense vector representations (384-dim sample vectors with model metadata).
6. **Updating Search Index and Metadata Catalog (75%)**: Persists document catalog entries and versioned snapshots in SQLite WAL storage (`document_records` and `document_versions`).
7. **Validating Citations, Metadata, and References (90%)**: Cross-verifies chunk counts, cryptographic content SHA-256 hashes, and reference integrity.
8. **Finalizing AI Analysis, Summary, and Results (100%)**: Executes prompt-engineered local LLM reasoning (llama3.2:latest) for summarization, key takeaways, structured tables, comparison, or RAG queries.

### 2. Supported Status Monitor States
- `Pending`: Job is registered in the queue awaiting worker allocation.
- `Uploading`: File format and size verification in progress.
- `Extracting`: Multimodal text and table parsing.
- `Editing`: Versioned delta modification and diff computation.
- `Analyzing`: LLM reasoning and prompt inference.
- `Summarizing`: Executive summary compilation.
- `Comparing`: Multi-document or multi-version comparative diff analysis.
- `Extracting structured data`: Tabular entity normalization.
- `Generating embeddings`: Dense vector chunk indexing.
- `Indexing`: Search index and database catalog synchronization.
- `Validating`: Cryptographic SHA-256 and citation validation.
- `Completed`: All 8 stages completed successfully (100%).
- `Completed with warnings`: All stages finished but non-fatal notices were logged.
- `Failed`: Precise failure stage captured; recoverable work preserved.
- `Cancelled`: Job cancelled safely via cancellation token without data corruption.

### 3. Document Editing & Incremental Versioning
- **Non-Destructive Versioning**: Original versions are permanently preserved in `document_versions`. When edits are submitted, the version increments atomically ($v1 \rightarrow v2 \rightarrow v3$).
- **Granular Diff Detection**: `detect_document_diff` calculates lines added, lines removed, total character delta, and identifies whether changes are substantive.
- **Atomic Rollback & Recovery**: In case downstream validation fails during editing, the previous document version remains intact and active.

### 4. Background Processing & FastAPI Endpoints
- `GET /api/documents`: Lists all indexed documents, version numbers, and chunk statistics.
- `GET /api/documents/{document_id}`: Retrieves specific document record and version history.
- `POST /api/documents/{document_id}/edit`: Asynchronously triggers a versioned document edit pipeline.
- `POST /api/documents/{document_id}/reindex`: Rebuilds chunks and embeddings for an existing document.
- `GET /api/jobs`: Lists all recent background jobs with progress percentages.
- `GET /api/jobs/{job_id}`: Polls real-time job status, stage index, and timestamps.
- `GET /api/jobs/{job_id}/events`: Real-time Server-Sent Events (SSE) stream broadcasting live progress updates.
- `POST /api/jobs/{job_id}/cancel`: Safely signals job cancellation.

---

## 🖥️ Launching the Application

### Launch Gradio Dashboard
```bash
python frontend/app.py
```
Open your browser to: **`http://localhost:7860`** (Navigate to **Tab 7: Document Processing & Real-Time Status Monitor**)

### Launch FastAPI Backend
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Open API docs at: **`http://localhost:8000/docs`**
=======
# Student_AI_Study_Multi_Assistant_Testing1-main
>>>>>>> f0df8d240a8b405dcb9d3de2dd3c859993a2cd28
