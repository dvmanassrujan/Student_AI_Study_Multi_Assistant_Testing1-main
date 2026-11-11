"""
Model-Free Extractive Summarization Engine.
Implements the TextRank graph centrality algorithm and deterministic pattern extractors.

Supported summary modes:
1. Short Summaries (2-3 salient sentences, chronologically aligned)
2. Detailed Summaries (7-10 high-centrality sentences with thematic grouping)
3. Chapter / Section Summaries (per-heading localized TextRank)
4. Important Points (bulleted key propositions with entity highlighting)
5. Key Definitions (definitional pattern recognition and term dictionary)
6. Exam-Focused Notes (high-yield formulas, core definitions, and revision checklist)
"""

import re
import math
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple, Optional

from backend.intelligence.nlp import (
    normalize_text,
    tokenize_sentences,
    tokenize_words,
    remove_stopwords,
    extract_keywords,
    stem
)


# =========================================================================
# 1. TextRank Graph-Based Centrality Algorithm
# =========================================================================

def _sentence_similarity(s1_tokens: List[str], s2_tokens: List[str]) -> float:
    """
    Computes normalized token overlap similarity between two sentences.
    Formula: |S1 n S2| / (log(|S1|) + log(|S2|) + 1e-6)
    """
    if not s1_tokens or not s2_tokens:
        return 0.0

    set1 = set(s1_tokens)
    set2 = set(s2_tokens)
    intersection = len(set1 & set2)

    if intersection == 0:
        return 0.0

    len1 = max(1, len(set1))
    len2 = max(1, len(set2))
    # Logarithmic length dampening prevents bias towards overly long sentences
    denom = math.log(len1 + 1.0) + math.log(len2 + 1.0)
    return intersection / denom if denom > 0 else 0.0


def textrank_sentences(
    sentences: List[str],
    damping: float = 0.85,
    max_iter: int = 80,
    epsilon: float = 1e-4
) -> List[Tuple[int, str, float]]:
    """
    Applies the PageRank algorithm on a fully connected sentence similarity graph.
    Returns: list of (original_index, sentence, textrank_score) sorted by original order or score.
    """
    n = len(sentences)
    if n == 0:
        return []
    if n == 1:
        return [(0, sentences[0], 1.0)]

    # Pre-process tokens for all sentences
    processed_sentences = []
    for s in sentences:
        tokens = [stem(t) for t in remove_stopwords(tokenize_words(s, lower=True))]
        processed_sentences.append(tokens)

    # Build weighted similarity matrix
    weights = [[0.0] * n for _ in range(n)]
    out_degree = [0.0] * n

    for i in range(n):
        for j in range(i + 1, n):
            sim = _sentence_similarity(processed_sentences[i], processed_sentences[j])
            if sim > 0:
                weights[i][j] = sim
                weights[j][i] = sim
                out_degree[i] += sim
                out_degree[j] += sim

    # Power Iteration: PR(i) = (1 - d)/N + d * sum(W_ji / Out(j) * PR(j))
    pr = [1.0 / n] * n

    for _ in range(max_iter):
        new_pr = [0.0] * n
        diff = 0.0

        for i in range(n):
            rank_sum = 0.0
            for j in range(n):
                if i != j and weights[j][i] > 0 and out_degree[j] > 0:
                    rank_sum += (weights[j][i] / out_degree[j]) * pr[j]
            new_pr[i] = ((1.0 - damping) / n) + (damping * rank_sum)
            diff += abs(new_pr[i] - pr[i])

        pr = new_pr
        if diff < epsilon:
            break

    # Add position bonus (sentences at beginning of text often contain thesis statements)
    scored = []
    for i, s in enumerate(sentences):
        pos_factor = 1.0 + (0.2 * (1.0 - (i / max(1, n))))
        final_score = pr[i] * pos_factor
        scored.append((i, s, final_score))

    return scored


# =========================================================================
# 2. Key Definition Extractor (Pattern Recognition)
# =========================================================================

def extract_definitions(text: str) -> List[Dict[str, str]]:
    """
    Identifies terms and their explicit definitions using linguistic pattern matching:
    - "X is defined as Y"
    - "X refers to Y"
    - "X is a/an Y that/which ..."
    - "X means Y"
    - "X represents Y"
    """
    if not text:
        return []

    definitions = []
    seen_terms = set()

    patterns = [
        # X is defined as Y
        r"\b([A-Z][a-zA-Z0-9_\s-]{2,35}?)\s+is\s+defined\s+as\s+([^.!?\n]{15,200})[.!?]",
        # X refers to Y
        r"\b([A-Z][a-zA-Z0-9_\s-]{2,35}?)\s+refers\s+to\s+([^.!?\n]{15,200})[.!?]",
        # X is an/a Y that/which Z
        r"\b([A-Z][a-zA-Z0-9_\s-]{2,35}?)\s+is\s+(?:an?|the)\s+([a-zA-Z0-9_\s-]{4,35}?\s+(?:that|which|used\s+to|responsible\s+for)\s+[^.!?\n]{15,180})[.!?]",
        # X means Y
        r"\b([A-Z][a-zA-Z0-9_\s-]{2,35}?)\s+means\s+([^.!?\n]{15,200})[.!?]",
        # Term: Definition (markdown or glossaries)
        r"^[-*•]?\s*\*\*([a-zA-Z0-9_\s-]{2,35}?)\*\*:\s*([^.!?\n]{15,200})[.!?]"
    ]

    for p in patterns:
        matches = re.finditer(p, text, flags=re.MULTILINE)
        for m in matches:
            term = m.group(1).strip()
            defn = m.group(2).strip()

            if term.lower() not in seen_terms and len(term.split()) <= 5:
                seen_terms.add(term.lower())
                definitions.append({
                    "term": term,
                    "definition": defn,
                    "full_sentence": m.group(0).strip()
                })

    return definitions


# =========================================================================
# 3. Summary Mode Generators
# =========================================================================

def generate_short_summary(text: str, max_sentences: int = 3) -> str:
    """
    Generates a concise 2-3 sentence executive summary preserving chronological order.
    """
    sentences = tokenize_sentences(text)
    if len(sentences) <= max_sentences:
        return text.strip()

    scored = textrank_sentences(sentences)
    # Pick top scoring sentences
    top_scored = sorted(scored, key=lambda x: x[2], reverse=True)[:max_sentences]
    # Re-order chronologically by original index
    top_scored.sort(key=lambda x: x[0])

    summary_text = " ".join(s for _, s, _ in top_scored)
    return (
        f"### 📌 Short Summary (Extractive TextRank)\n\n"
        f"{summary_text}\n\n"
        f"---\n*Extractive summary generated deterministically via TextRank. No generative hallucinations.*"
    )


def generate_detailed_summary(text: str, target_sentences: int = 7) -> str:
    """
    Generates a structured, in-depth summary with thematic takeaways.
    """
    sentences = tokenize_sentences(text)
    if len(sentences) <= target_sentences:
        return text.strip()

    scored = textrank_sentences(sentences)
    top_scored = sorted(scored, key=lambda x: x[2], reverse=True)[:target_sentences]
    top_scored.sort(key=lambda x: x[0])

    keywords = extract_keywords(text, top_k=6)
    kw_str = ", ".join(f"`{k}`" for k in keywords)

    # Format structured detailed summary
    lines = [
        f"### 📋 Comprehensive Detailed Summary",
        f"**Core Subject Keywords:** {kw_str}\n",
        f"#### 💡 Key Thematic Highlights:"
    ]

    for idx, (_, s, _) in enumerate(top_scored, 1):
        lines.append(f"{idx}. {s}")

    lines.extend([
        "\n#### 🔍 Methodological Transparency:",
        "- **Algorithm:** TextRank PageRank graph centrality with sentence length dampening ($d=0.85$).",
        "- **Coverage:** Ranked from across the full body of source sentences.",
        "- **Factuality:** 100% extractive and grounded strictly in the source text."
    ])

    return "\n".join(lines)


def generate_chapter_summaries(text: str) -> str:
    """
    Detects document chapters/sections and runs localized TextRank per section.
    """
    lines = text.splitlines()
    sections: List[Tuple[str, List[str]]] = []
    current_title = "Introduction / Overview"
    current_lines = []

    for l in lines:
        stripped = l.strip()
        # Heading marker
        if re.match(r"^#{1,3}\s+(.+)", stripped):
            if current_lines:
                sections.append((current_title, current_lines))
                current_lines = []
            current_title = re.sub(r"^#{1,3}\s+", "", stripped)
        elif len(stripped) < 60 and stripped.isupper() and len(stripped) > 4:
            if current_lines:
                sections.append((current_title, current_lines))
                current_lines = []
            current_title = stripped
        else:
            if stripped:
                current_lines.append(stripped)

    if current_lines:
        sections.append((current_title, current_lines))

    if not sections:
        return generate_detailed_summary(text)

    output_lines = ["### 📑 Section-by-Section Chapter Summaries\n"]

    for title, sec_lines in sections:
        sec_text = " ".join(sec_lines)
        sents = tokenize_sentences(sec_text)
        if not sents:
            continue

        output_lines.append(f"#### 📖 {title}")
        if len(sents) <= 2:
            output_lines.append(f"{sec_text}\n")
        else:
            scored = textrank_sentences(sents)
            top = sorted(scored, key=lambda x: x[2], reverse=True)[:2]
            top.sort(key=lambda x: x[0])
            output_lines.append(" ".join(s for _, s, _ in top) + "\n")

    return "\n".join(output_lines)


def generate_important_points(text: str, max_points: int = 8) -> str:
    """
    Extracts the most salient proposition sentences formatted as bullet points.
    """
    sentences = tokenize_sentences(text)
    if not sentences:
        return "⚠️ No content provided to extract important points."

    scored = textrank_sentences(sentences)
    top_scored = sorted(scored, key=lambda x: x[2], reverse=True)[:max_points]
    top_scored.sort(key=lambda x: x[0])

    lines = [
        "### 🎯 Key Takeaways & Important Points\n",
        "The following propositions represent the highest-saliency concepts extracted from the text:\n"
    ]

    for _, s, score in top_scored:
        lines.append(f"- **{s}** *(Centrality: `{score:.3f}`)*")

    lines.append("\n*Extracted via deterministic TextRank scoring.*")
    return "\n".join(lines)


def generate_definitions_lexicon(text: str) -> str:
    """
    Constructs a glossary table of terms and their explicit definitions.
    """
    defs = extract_definitions(text)
    if not defs:
        # Fallback to keyword-based sentence extraction
        keywords = extract_keywords(text, top_k=5)
        return (
            "### 📖 Key Terms & Lexicon\n\n"
            "*(No explicit 'X is defined as Y' patterns detected. Showing core domain terms)*\n\n"
            + "\n".join(f"- **{k.capitalize()}**: Prominent concept in this text." for k in keywords)
        )

    lines = [
        "### 📖 Key Definitions & Terminology Lexicon\n",
        "| Term | Definitional Meaning |",
        "| :--- | :--- |"
    ]
    for d in defs:
        clean_def = d['definition'].replace("|", "-")
        lines.append(f"| **{d['term']}** | {clean_def} |")

    return "\n".join(lines)


def generate_exam_notes(text: str) -> str:
    """
    Compiles high-yield exam-focused study notes:
    - High-Yield Concept Checklist
    - Key Definitions Table
    - Core Principles & Formulas/Metrics
    - Quick Revision Checklist
    """
    sentences = tokenize_sentences(text)
    keywords = extract_keywords(text, top_k=8)
    defs = extract_definitions(text)
    scored = textrank_sentences(sentences)

    top_propositions = sorted(scored, key=lambda x: x[2], reverse=True)[:5]
    top_propositions.sort(key=lambda x: x[0])

    # Detect numerical / formula metrics: e.g. "O(N)", "95%", "3.14", "f(x)"
    metric_sentences = []
    for s in sentences:
        if re.search(r"(\bO\(|\b\d+[\.%]|\bformula\b|\bequation\b)", s, re.IGNORECASE):
            metric_sentences.append(s)

    lines = [
        "### 🎓 High-Yield Exam Preparation Notes",
        f"**Target Revision Topics:** {', '.join(f'`{k}`' for k in keywords[:6])}\n",
        "#### 🧠 1. Core Principles & Propositions:"
    ]

    for _, s, _ in top_propositions:
        lines.append(f"- **{s}**")

    if defs:
        lines.extend([
            "\n#### 📚 2. Essential Definitions to Memorize:",
            "| Term | Exam Definition |",
            "| :--- | :--- |"
        ])
        for d in defs[:6]:
            lines.append(f"| **{d['term']}** | {d['definition'].replace('|', '-')} |")

    if metric_sentences:
        lines.extend([
            "\n#### 🔢 3. Formulas, Bounds & Numerical Facts:"
        ])
        for ms in metric_sentences[:4]:
            lines.append(f"- `{ms}`")

    lines.extend([
        "\n#### ✅ 4. Quick Self-Assessment Checklist:",
        *[f"- [ ] Can you define and explain **{k.capitalize()}** from memory?" for k in keywords[:5]],
        "- [ ] Can you explain the relationship between these core concepts?",
        "- [ ] Have you practiced solving problems based on these principles?",
        "\n---\n*Exam notes generated deterministically from source material.*"
    ])

    return "\n".join(lines)

