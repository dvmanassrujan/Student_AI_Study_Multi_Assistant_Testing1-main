"""
Model-Free Intelligence Engine for AI Multi-Study Assistant.
Exposes zero-cost, API-free, local Python algorithmic intelligence modules.
"""

from backend.intelligence.nlp import (
    normalize_text,
    tokenize_sentences,
    tokenize_words,
    remove_stopwords,
    stem,
    lemmatize_tokens,
    extract_keywords,
    TFIDFVectorizer,
    BM25Index,
    cosine_similarity,
    classify_intent
)
from backend.intelligence.document_engine import (
    extract_document,
    chunk_document,
    DocumentChunk,
    DocumentSearchIndex,
    extract_relevant_passages,
    answer_document_query,
    generate_document_questions
)
from backend.intelligence.summarizer import (
    textrank_sentences,
    extract_definitions,
    generate_short_summary,
    generate_detailed_summary,
    generate_chapter_summaries,
    generate_important_points,
    generate_definitions_lexicon,
    generate_exam_notes
)
from backend.intelligence.quiz_flashcards import (
    generate_mcqs_from_text,
    generate_mcqs_for_topic,
    generate_flashcards,
    format_exam_material,
    format_flashcard_markdown,
    evaluate_quiz_answers
)
from backend.intelligence.study_planner import (
    generate_study_plan_schedule,
    calculate_completion_status
)
from backend.intelligence.coding_mentor import (
    analyze_code_ast,
    explain_code_snippet,
    debug_code_snippet,
    optimize_code_snippet,
    teach_dsa_topic
)
from backend.intelligence.model_free_agent import (
    ModelFreeStudyEngine,
    ModelFreeLLM,
    ModelFreeMessage,
    study_engine
)

__all__ = [
    "normalize_text",
    "tokenize_sentences",
    "tokenize_words",
    "remove_stopwords",
    "stem",
    "lemmatize_tokens",
    "extract_keywords",
    "TFIDFVectorizer",
    "BM25Index",
    "cosine_similarity",
    "classify_intent",
    "extract_document",
    "chunk_document",
    "DocumentChunk",
    "DocumentSearchIndex",
    "extract_relevant_passages",
    "answer_document_query",
    "generate_document_questions",
    "textrank_sentences",
    "extract_definitions",
    "generate_short_summary",
    "generate_detailed_summary",
    "generate_chapter_summaries",
    "generate_important_points",
    "generate_definitions_lexicon",
    "generate_exam_notes",
    "generate_mcqs_from_text",
    "generate_mcqs_for_topic",
    "generate_flashcards",
    "format_exam_material",
    "format_flashcard_markdown",
    "evaluate_quiz_answers",
    "generate_study_plan_schedule",
    "calculate_completion_status",
    "analyze_code_ast",
    "explain_code_snippet",
    "debug_code_snippet",
    "optimize_code_snippet",
    "teach_dsa_topic",
    "ModelFreeStudyEngine",
    "ModelFreeLLM",
    "ModelFreeMessage",
    "study_engine"
]

