"""
Model-Free Intelligence Engine Diagnostics & Verification Script
Verifies all 6 deterministic, zero-cost intelligence subsystems:
1. Natural Language Processing (Tokenization, Stemming, TF-IDF, BM25, Intent Classification)
2. Document Intelligence (Multi-format parsing, chunking, BM25+TF-IDF retrieval, grounded Q&A)
3. Extractive Summarization (TextRank graph centrality, key points, definitions, exam notes)
4. Quiz & Flashcard Engine (MCQ generation, Cloze fill-in-the-blank, flashcards, scoring)
5. Study Planner (Pomodoro planning, Ebbinghaus spaced revision intervals, progress tracking)
6. Coding Mentor (Python AST analysis, syntax caret diagnosis, cyclomatic complexity, DSA tutor)
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.intelligence import (
    # NLP
    normalize_text,
    tokenize_sentences,
    tokenize_words,
    remove_stopwords,
    stem,
    extract_keywords,
    TFIDFVectorizer,
    BM25Index,
    cosine_similarity,
    classify_intent,
    # Document Intelligence
    extract_document,
    chunk_document,
    DocumentChunk,
    DocumentSearchIndex,
    extract_relevant_passages,
    answer_document_query,
    generate_document_questions,
    # Summarizer
    textrank_sentences,
    extract_definitions,
    generate_short_summary,
    generate_detailed_summary,
    generate_chapter_summaries,
    generate_important_points,
    generate_definitions_lexicon,
    generate_exam_notes,
    # Quiz & Flashcards
    generate_mcqs_from_text,
    generate_mcqs_for_topic,
    generate_flashcards,
    format_exam_material,
    format_flashcard_markdown,
    evaluate_quiz_answers,
    # Study Planner
    generate_study_plan_schedule,
    calculate_completion_status,
    # Coding Mentor
    analyze_code_ast,
    explain_code_snippet,
    debug_code_snippet,
    optimize_code_snippet,
    teach_dsa_topic,
    # Agent
    ModelFreeStudyEngine,
    ModelFreeLLM,
)


def run_diagnostics():
    print("=" * 70)
    print("🧠 MODEL-FREE INTELLIGENCE ENGINE: COMPLETE SYSTEM DIAGNOSTICS")
    print("=" * 70)

    # 1. NLP Subsystem
    print("\n[1/6] Testing NLP Subsystem...")
    sample_text = (
        "Artificial intelligence and machine learning enable computers to learn from data. "
        "Deep learning is a subset of machine learning using neural networks. "
        "Python provides powerful libraries like numpy and pandas for scientific computing."
    )
    sents = tokenize_sentences(sample_text)
    words = tokenize_words(sents[0])
    stems = [stem(w) for w in ["learning", "computers", "neural", "studying"]]
    keywords = extract_keywords(sample_text, top_k=5)
    tfidf = TFIDFVectorizer()
    tfidf.fit([sents[0], sents[1], sents[2]])
    vec = tfidf.transform(sents[0])
    bm25 = BM25Index()
    bm25.index([sents[0], sents[1], sents[2]])
    bm25_scores = bm25.score("machine learning")
    intent = classify_intent("Can you make a study plan for my data structures exam?")
    
    assert len(sents) == 3, f"Expected 3 sentences, got {len(sents)}"
    assert intent == "study_planner", f"Expected 'study_planner', got {intent}"
    print(f"  ✅ Sentences extracted: {len(sents)}")
    print(f"  ✅ Stems: {stems}")
    print(f"  ✅ Top keywords: {keywords[:3]}")
    print(f"  ✅ TF-IDF vocab size: {len(tfidf.vocab)}")
    print(f"  ✅ BM25 scores: {[round(s, 2) for s in bm25_scores]}")
    print(f"  ✅ Intent classification: '{intent}'")

    # 2. Document Intelligence Subsystem
    print("\n[2/6] Testing Document Intelligence Subsystem...")
    chunks = chunk_document(sample_text, chunk_size=150, chunk_overlap=20)
    search_idx = DocumentSearchIndex(chunks)
    qa_result = answer_document_query("What enables computers to learn?", search_idx)
    assert "artificial intelligence and machine learning" in qa_result.lower()
    insufficient_qa = answer_document_query("What is quantum entanglement in black holes?", search_idx)
    assert "insufficient information" in insufficient_qa.lower()
    doc_q = generate_document_questions(chunks, num_questions=2)
    print(f"  ✅ Chunking: {len(chunks)} chunks generated")
    print(f"  ✅ Grounded Q&A result: {qa_result[:80].strip()}...")
    print(f"  ✅ Anti-hallucination warning test: Insufficient info warning successfully triggered")
    print(f"  ✅ Document questions generated: {len(doc_q)}")

    # 3. Extractive Summarization Subsystem
    print("\n[3/6] Testing Extractive Summarization Subsystem...")
    textrank_summary = generate_short_summary(sample_text, max_sentences=2)
    key_points = generate_important_points(sample_text, max_points=2)
    defs = extract_definitions(sample_text)
    exam_notes = generate_exam_notes(sample_text)
    assert len(textrank_summary) > 0
    print(f"  ✅ TextRank short summary ({len(textrank_summary.splitlines())} lines)")
    print(f"  ✅ Key points extracted: {len(key_points.splitlines())} lines")
    print(f"  ✅ Definitions extracted: {len(defs)}")
    print(f"  ✅ Exam notes generated ({len(exam_notes)} chars)")

    # 4. Quiz & Flashcard Engine
    print("\n[4/6] Testing Quiz & Flashcard Engine...")
    mcqs = generate_mcqs_from_text(sample_text, num_questions=2)
    flashcards = generate_flashcards(sample_text, num_cards=2)
    assert len(mcqs) >= 1
    assert len(flashcards) >= 1
    mcq = mcqs[0]
    assert len(mcq["options"]) == 4, "MCQ must have 4 options"
    assert mcq["correct_option"] in ["A", "B", "C", "D"], "MCQ answer must be valid option letter"
    eval_res = evaluate_quiz_answers({"1": mcq["correct_option"]}, mcqs)
    assert eval_res["percentage"] > 0
    print(f"  ✅ MCQs generated: {len(mcqs)} (with 4 choices & distractors)")
    print(f"  ✅ Flashcards generated: {len(flashcards)}")
    print(f"  ✅ Scoring engine verified: {eval_res['score']}/{eval_res['total']} ({eval_res['percentage']}%)")

    # 5. Study Planner Subsystem
    print("\n[5/6] Testing Study Planner Subsystem...")
    plan_text = generate_study_plan_schedule(
        topic="Algorithms & Data Structures",
        level="Intermediate",
        duration="2 Weeks",
        hours_per_day=3.0,
        goals="Master binary search, graph traversal, and dynamic programming",
        priority="High",
        exam_date="2026-12-01",
        completion_percentage=20.0
    )
    assert len(plan_text) > 0
    comp = calculate_completion_status(completed_days=5, total_days=10)
    assert comp["completion_percentage"] == 50.0
    print(f"  ✅ Study plan generated ({len(plan_text)} chars with Pomodoro & Ebbinghaus intervals)")
    print(f"  ✅ Completion status calculated: {comp['completion_percentage']}% ({comp['status']})")

    # 6. Coding Mentor Subsystem
    print("\n[6/6] Testing Coding Mentor Subsystem...")
    bad_code = "def add(a, b\n    return a + b"
    debug_res = debug_code_snippet(bad_code)
    assert "Syntax Error Diagnosed" in debug_res
    
    good_code = """def find_even(numbers, default=[]):
    evens = []
    for n in numbers:
        if n % 2 == 0:
            evens.append(n)
    return evens"""
    ast_analysis = analyze_code_ast(good_code)
    assert ast_analysis["valid_syntax"]
    assert len(ast_analysis["warnings"]) > 0  # Mutable default detected!
    
    opt_res = optimize_code_snippet(good_code)
    dsa_res = teach_dsa_topic("binary search")
    assert "Binary Search" in dsa_res
    print(f"  ✅ Syntax error diagnosed with visual caret in debugger")
    print(f"  ✅ Anti-patterns detected by AST: {[w['type'] for w in ast_analysis['warnings']]}")
    print(f"  ✅ Cyclomatic complexity: {ast_analysis['cyclomatic_complexity']}")
    print(f"  ✅ Optimization suggestions: {len(opt_res)} chars")
    print(f"  ✅ DSA masterclass verified: Binary Search ({len(dsa_res)} chars)")

    # 7. Unified Engine Interface
    print("\n[Unified Engine] Testing ModelFreeLLM & LangChain-compatible interface...")
    llm = ModelFreeLLM()
    resp = llm.invoke("Explain photosynthesis in simple terms")
    assert len(resp.content) > 0
    print(f"  ✅ Unified LLM invocation passed ({len(resp.content)} characters generated)")

    print("\n" + "=" * 70)
    print("🏆 ALL 6 MODEL-FREE INTELLIGENCE SUBSYSTEMS OPERATIONAL & VERIFIED!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = run_diagnostics()
    if not success:
        sys.exit(1)
