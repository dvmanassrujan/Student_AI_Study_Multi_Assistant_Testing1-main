"""
Comprehensive Test Suite for Model-Free Intelligence Engine.
Tests:
1. Natural Language Processing (Normalization, Tokenization, Stemming, TF-IDF, BM25, Cosine Similarity, Intent)
2. Document Intelligence (Parsing, Chunking, Retrieval, Anti-Hallucination Grounding, Question Gen)
3. Extractive Summarization (TextRank, Short/Detailed Summaries, Important Points, Definitions, Exam Notes)
4. Quiz & Flashcard Engine (MCQs, Distractors, Cloze, Flashcards, Scoring)
5. Study Planner (Duration, Hours, Difficulty Multiplier, Spaced Revision, Progress)
6. Coding Mentor (AST Analysis, Syntax Diagnosis, Complexity, Anti-Patterns, DSA Coach)
7. Model-Free Agent Orchestrator (Unified Dispatch & LangChain compatibility)
"""

import os
import unittest
from pathlib import Path

from backend.intelligence import (
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
    chunk_document,
    DocumentSearchIndex,
    answer_document_query,
    generate_document_questions,
    textrank_sentences,
    extract_definitions,
    generate_short_summary,
    generate_detailed_summary,
    generate_important_points,
    generate_definitions_lexicon,
    generate_exam_notes,
    generate_mcqs_from_text,
    generate_mcqs_for_topic,
    generate_flashcards,
    format_exam_material,
    format_flashcard_markdown,
    evaluate_quiz_answers,
    generate_study_plan_schedule,
    calculate_completion_status,
    analyze_code_ast,
    explain_code_snippet,
    debug_code_snippet,
    optimize_code_snippet,
    teach_dsa_topic,
    ModelFreeStudyEngine,
    ModelFreeLLM
)


class TestModelFreeIntelligenceEngine(unittest.TestCase):

    # =========================================================================
    # 1. NLP Tests
    # =========================================================================

    def test_01_text_normalization(self):
        raw = "It’s a test—don’t forget ‘smart quotes’ and   extra   spaces.\r\nNext line."
        norm = normalize_text(raw)
        self.assertIn("It is", norm)
        self.assertIn("do not", norm)
        self.assertNotIn("’", norm)
        self.assertNotIn("   ", norm)

    def test_02_sentence_segmentation(self):
        text = "Dr. Alan Turing, e.g., introduced the Turing Machine in 1936. The speedup was 3.14x! Isn't that great?"
        sents = tokenize_sentences(text)
        self.assertEqual(len(sents), 3)
        self.assertTrue(sents[0].startswith("Dr. Alan Turing"))
        self.assertTrue(sents[1].startswith("The speedup was 3.14x"))
        self.assertTrue(sents[2].startswith("Isn't that great"))

    def test_03_stemming(self):
        self.assertEqual(stem("studying"), "study")
        self.assertEqual(stem("matrices"), "matrix")
        self.assertEqual(stem("faster"), "faster")
        self.assertEqual(stem("educational"), "educate")

    def test_04_keyword_extraction(self):
        text = (
            "Machine learning algorithms build a mathematical model based on training data. "
            "Supervised learning algorithms and unsupervised learning algorithms are core paradigms in machine learning."
        )
        keywords = extract_keywords(text, top_k=5)
        self.assertIn("learning", [k.lower() for k in keywords])
        self.assertIn("algorithms", [k.lower() for k in keywords])

    def test_05_tfidf_and_cosine_similarity(self):
        docs = [
            "Binary search is an efficient search algorithm on sorted arrays.",
            "Merge sort divides the array into two halves and merges them.",
            "Calculus investigates continuous change through derivatives and integrals."
        ]
        tfidf = TFIDFVectorizer()
        vecs = tfidf.fit_transform(docs)
        self.assertEqual(len(vecs), 3)

        q_vec = tfidf.transform("search algorithm array")
        sim_doc0 = cosine_similarity(q_vec, vecs[0])
        sim_doc2 = cosine_similarity(q_vec, vecs[2])
        self.assertGreater(sim_doc0, sim_doc2)
        self.assertEqual(sim_doc2, 0.0)

    def test_06_bm25_ranking(self):
        docs = [
            "Python programming language supports functional and object oriented paradigms.",
            "JavaScript is primarily used for frontend browser web development.",
            "Python data science utilizes NumPy and Pandas for data manipulation."
        ]
        bm25 = BM25Index()
        bm25.index(docs)
        top = bm25.rank("Python data", top_k=2)
        self.assertTrue(len(top) >= 1)
        # Doc 2 contains both 'Python' and 'data'
        self.assertEqual(top[0][0], 2)

    def test_07_intent_classification(self):
        self.assertEqual(classify_intent("create a 2 week study timetable for exams"), "study_planner")
        self.assertEqual(classify_intent("give me a 10 question multiple choice mock quiz"), "exam")
        self.assertEqual(classify_intent("def binary_search(arr, target): syntax error on line 4"), "coding")
        self.assertEqual(classify_intent("summarize this pdf notes and extract passages"), "document")
        self.assertEqual(classify_intent("build an e-commerce project architecture and schema"), "project")

    # =========================================================================
    # 2. Document Intelligence Tests
    # =========================================================================

    def test_08_chunking_and_grounded_answer(self):
        doc = (
            "# Artificial Intelligence Principles\n"
            "Supervised learning is defined as an algorithm trained on labeled inputs to predict target outputs.\n"
            "Linear regression and support vector machines are classic examples of supervised learning.\n\n"
            "# Deep Learning Architecture\n"
            "Convolutional Neural Networks (CNNs) are specialized neural networks used primarily for image recognition.\n"
            "Recurrent Neural Networks (RNNs) are designed for sequential time-series and natural language data.\n"
        )
        chunks = chunk_document(doc, chunk_size=200, chunk_overlap=40)
        self.assertGreaterEqual(len(chunks), 2)

        index = DocumentSearchIndex(chunks)

        # Grounded answer when information exists
        ans1 = answer_document_query("What is supervised learning?", index)
        self.assertIn("Grounded Document Answer", ans1)
        self.assertIn("supervised learning", ans1.lower())

        # Anti-hallucination test: strictly declines when query is absent from document
        ans_absent = answer_document_query("What is quantum string theory in astrophysics?", index)
        self.assertIn("Insufficient Information", ans_absent)
        self.assertNotIn("quantum string theory is", ans_absent.lower())

    def test_09_document_question_generation(self):
        doc = (
            "Overfitting refers to a modeling error where an algorithm fits training noise rather than true underlying patterns. "
            "Regularization is defined as a technique used to penalize complex model parameters and mitigate overfitting."
        )
        chunks = chunk_document(doc)
        qs = generate_document_questions(chunks, num_questions=2)
        self.assertGreaterEqual(len(qs), 1)
        q1 = qs[0]
        self.assertIn("question", q1)
        self.assertIn("answer", q1)

    # =========================================================================
    # 3. Extractive Summarization Tests
    # =========================================================================

    def test_10_textrank_and_summaries(self):
        text = (
            "Machine learning is a subset of artificial intelligence. "
            "It focuses on building applications that learn from data and improve their accuracy over time without being programmed to do so. "
            "In data science, an algorithm is a sequence of statistical processing steps. "
            "Supervised learning algorithms are trained using labeled examples. "
            "Deep learning algorithms use multi-layered artificial neural networks. "
            "Overfitting occurs when a model fits training noise."
        )
        short_sum = generate_short_summary(text, max_sentences=2)
        self.assertIn("Short Summary", short_sum)
        self.assertIn("learning", short_sum.lower())

        detailed_sum = generate_detailed_summary(text, target_sentences=3)
        self.assertIn("Comprehensive Detailed Summary", detailed_sum)
        self.assertIn("Machine learning", detailed_sum)

        points = generate_important_points(text, max_points=3)
        self.assertIn("Key Takeaways", points)

        exam_notes = generate_exam_notes(text)
        self.assertIn("High-Yield Exam Preparation Notes", exam_notes)

    def test_11_definition_extraction(self):
        text = (
            "A Queue is defined as a linear data structure following the First-In First-Out principle. "
            "A Stack refers to a collection that follows Last-In First-Out ordering."
        )
        lexicon = generate_definitions_lexicon(text)
        self.assertIn("Queue", lexicon)
        self.assertIn("Stack", lexicon)

    # =========================================================================
    # 4. Quiz & Flashcard Tests
    # =========================================================================

    def test_12_mcq_generation_and_scoring(self):
        doc = (
            "Photosynthesis is defined as the biological process of converting light energy into chemical sugars. "
            "Chloroplasts are the cellular organelles responsible for capturing sunlight during photosynthesis. "
            "Mitochondria generate cellular ATP through cellular respiration."
        )
        mcqs = generate_mcqs_from_text(doc, num_questions=2)
        self.assertEqual(len(mcqs), 2)
        self.assertEqual(len(mcqs[0]["options"]), 4)
        self.assertIn(mcqs[0]["correct_option"], ["A", "B", "C", "D"])

        formatted = format_exam_material(mcqs, "Cell Biology")
        self.assertIn("Examination Questions", formatted)
        self.assertIn("Answer Key", formatted)

        # Evaluate scoring
        eval_res = evaluate_quiz_answers({"1": mcqs[0]["correct_option"], "2": "WRONG"}, mcqs)
        self.assertEqual(eval_res["score"], 1)
        self.assertEqual(eval_res["percentage"], 50.0)

    def test_13_flashcards(self):
        cards = generate_flashcards("Binary Search", num_cards=3, is_raw_text=False)
        self.assertGreaterEqual(len(cards), 1)
        md = format_flashcard_markdown(cards, "Algorithms")
        self.assertIn("Active Recall Flashcards", md)
        self.assertIn("Front:", md)

    # =========================================================================
    # 5. Study Planner Tests
    # =========================================================================

    def test_14_study_plan_generation(self):
        plan = generate_study_plan_schedule(
            topic="Python Programming",
            level="Beginner",
            duration="1 Week",
            hours_per_day=2.0,
            goals="Master functions and loops"
        )
        self.assertIn("Intelligent Academic Study Plan", plan)
        self.assertIn("Day 1", plan)
        self.assertIn("Day 7", plan)
        self.assertIn("Pomodoro", plan)

        progress = calculate_completion_status(completed_days=3, total_days=7)
        self.assertAlmostEqual(progress["completion_percentage"], 42.9, places=1)

    # =========================================================================
    # 6. Coding Mentor Tests
    # =========================================================================

    def test_15_ast_syntax_diagnosis(self):
        bad_code = "def add(a, b)\n    return a + b"
        analysis = analyze_code_ast(bad_code)
        self.assertFalse(analysis["valid_syntax"])
        self.assertEqual(analysis["error_type"], "SyntaxError")
        self.assertIn(":", analysis["fix_suggestion"])

        debug_res = debug_code_snippet(bad_code)
        self.assertIn("Syntax Error Diagnosed", debug_res)

    def test_16_ast_anti_patterns_and_complexity(self):
        code_with_warning = (
            "def process_data(items, cache=[]):\n"
            "    if items == None:\n"
            "        return None\n"
            "    for i in range(len(items)):\n"
            "        if items[i] > 0:\n"
            "            cache.append(items[i])\n"
            "    return cache\n"
        )
        analysis = analyze_code_ast(code_with_warning)
        self.assertTrue(analysis["valid_syntax"])
        self.assertGreaterEqual(analysis["cyclomatic_complexity"], 2)

        warning_types = [w["type"] for w in analysis["warnings"]]
        self.assertIn("Mutable Default Argument", warning_types)
        self.assertIn("Identity Comparison Anti-Pattern", warning_types)

    def test_17_dsa_coach(self):
        dsa = teach_dsa_topic("Binary Search")
        self.assertIn("DSA Masterclass: Binary Search", dsa)
        self.assertIn("O(log N)", dsa)
        self.assertIn("def binary_search", dsa)

    # =========================================================================
    # 7. Model-Free Orchestrator Tests
    # =========================================================================

    def test_18_model_free_study_engine(self):
        engine = ModelFreeStudyEngine()
        res_planner = engine.process_prompt("Create a study schedule for Biology", task_type="study_planner")
        self.assertIn("Intelligent Academic Study Plan", res_planner)

        res_exam = engine.process_prompt("Give me mock test on Data Structures", task_type="exam")
        self.assertIn("Mock Test", res_exam)

        res_coding = engine.process_prompt("Explain binary search", task_type="coding")
        self.assertIn("Code Walkthrough", res_coding)

    def test_19_model_free_llm_adapter(self):
        llm = ModelFreeLLM()
        res = llm.invoke("What is calculus?")
        self.assertEqual(res.type, "ai")
        self.assertIn("Academic Concept Guide", res.content)


if __name__ == "__main__":
    unittest.main()
