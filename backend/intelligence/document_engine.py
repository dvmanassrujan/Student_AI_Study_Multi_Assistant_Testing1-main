"""
Model-Free Document Intelligence & Grounded Retrieval Engine.
Supports: PDF, DOCX, TXT, CSV, and Markdown files.

Features:
1. Multi-format text and structure extraction with standard library fallbacks.
2. Intelligent semantic and heading-aware chunking with sliding-window overlap.
3. Hybrid search: BM25 ranking + TF-IDF cosine similarity + exact keyword matching.
4. Relevant passage extraction with sentence-level precision.
5. Strictly source-grounded answering (guaranteed zero hallucination).
6. Document-based question generation and flashcards.
"""

import os
import re
import csv
import io
import json
import zlib
import zipfile
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

from backend.intelligence.nlp import (
    normalize_text,
    tokenize_sentences,
    tokenize_words,
    remove_stopwords,
    extract_keywords,
    TFIDFVectorizer,
    BM25Index,
    cosine_similarity
)


# =========================================================================
# 1. Multi-Format Document Parsing (PDF, DOCX, TXT, CSV, Markdown)
# =========================================================================

def parse_pdf(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts text from PDF files using PyMuPDF (fitz) if installed,
    with a pure-Python stream fallback parser that unpacks text objects.
    """
    text_parts = []
    page_count = 0
    tables_found = 0

    # Primary method: PyMuPDF
    try:
        import fitz
        doc = fitz.open(file_path)
        page_count = len(doc)
        for p_idx, page in enumerate(doc):
            p_text = page.get_text()
            if p_text.strip():
                text_parts.append(f"\n--- Page {p_idx + 1} ---\n{p_text}")
                if "\t" in p_text or "   " in p_text:
                    tables_found += 1
        return "\n".join(text_parts).strip(), {
            "parser": "PyMuPDF",
            "pages": page_count,
            "tables_detected": tables_found
        }
    except Exception:
        pass

    # Pure-Python fallback: parse PDF streams without external dependencies
    try:
        with open(file_path, "rb") as f:
            content = f.read()

        # Extract text within stream ... endstream blocks
        stream_pattern = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.DOTALL)
        for match in stream_pattern.finditer(content):
            stream_data = match.group(1)
            # Attempt FlateDecode decompression
            try:
                decompressed = zlib.decompress(stream_data)
            except Exception:
                decompressed = stream_data

            # Look for PDF text objects: BT ... ET
            bt_pattern = re.compile(rb"BT\s*(.*?)\s*ET", re.DOTALL)
            for bt in bt_pattern.finditer(decompressed):
                bt_data = bt.group(1).decode("latin-1", errors="ignore")
                # Extract text within parentheses: (text) Tj or [(text)] TJ
                tj_strings = re.findall(r"\((.*?)\)\s*Tj", bt_data)
                for s in tj_strings:
                    if len(s.strip()) > 1:
                        text_parts.append(s.strip())

        extracted = " ".join(text_parts)
        if len(extracted.strip()) > 50:
            return extracted.strip(), {"parser": "PurePythonStreamParser", "pages": 1, "tables_detected": 0}
    except Exception:
        pass

    # Raw string extraction fallback
    with open(file_path, "rb") as f:
        raw = f.read().decode("utf-8", errors="ignore")
    # Clean non-printable characters
    clean_raw = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]", " ", raw)
    words = [w for w in clean_raw.split() if len(w) > 2 and w.isalnum()]
    return " ".join(words[:5000]), {"parser": "RawFallback", "pages": 1, "tables_detected": 0}


def parse_docx(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts text and table content from DOCX files using python-docx if installed,
    with a pure-Python zipfile + XML fallback parser.
    """
    # Primary method: python-docx
    try:
        import docx
        doc = docx.Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        table_lines = []
        for t in doc.tables:
            for row in t.rows:
                cells = [c.text.strip() for c in row.cells if c.text.strip()]
                if cells:
                    table_lines.append(" | ".join(cells))
        combined = "\n\n".join(paragraphs + table_lines)
        return combined.strip(), {
            "parser": "python-docx",
            "paragraphs": len(paragraphs),
            "tables": len(doc.tables)
        }
    except Exception:
        pass

    # Pure-Python fallback: DOCX is a zip archive with word/document.xml
    try:
        import xml.etree.ElementTree as ET
        with zipfile.ZipFile(file_path, "r") as z:
            xml_bytes = z.read("word/document.xml")
        root = ET.fromstring(xml_bytes)
        # XML namespace for WordprocessingML
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        text_elements = root.findall(".//w:t", ns)
        extracted = "".join(elem.text for elem in text_elements if elem.text)
        # Separate paragraphs by finding all w:p tags
        paras = []
        for p in root.findall(".//w:p", ns):
            p_text = "".join(t.text for t in p.findall(".//w:t", ns) if t.text)
            if p_text.strip():
                paras.append(p_text.strip())
        final_text = "\n\n".join(paras) if paras else extracted
        return final_text.strip(), {"parser": "PurePythonZipXml", "paragraphs": len(paras), "tables": 0}
    except Exception as e:
        # Ultimate fallback
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), {"parser": "RawFallback", "paragraphs": 0, "tables": 0, "error": str(e)}


def parse_csv(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parses CSV files into clean tabular representation and markdown summary.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except Exception:
            dialect = csv.excel

        reader = csv.reader(f, dialect)
        rows = list(reader)

    if not rows:
        return "", {"parser": "csv", "rows": 0, "columns": 0}

    header = rows[0]
    data_rows = rows[1:]

    # Format into markdown table
    md_lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |"
    ]
    for r in data_rows[:100]: # Preview up to 100 rows
        padded = r + [""] * (len(header) - len(r))
        md_lines.append("| " + " | ".join(padded[:len(header)]) + " |")

    # Also build natural language records for semantic retrieval
    record_descriptions = []
    for r in data_rows[:200]:
        parts = [f"{header[i]}: {r[i]}" for i in range(min(len(header), len(r))) if r[i].strip()]
        if parts:
            record_descriptions.append(", ".join(parts))

    combined = "\n".join(md_lines) + "\n\n### Record Details:\n" + "\n".join(record_descriptions)
    return combined, {
        "parser": "csv",
        "rows": len(rows),
        "columns": len(header),
        "headers": header
    }


def parse_markdown_or_txt(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Reads plain text or Markdown files supporting multiple character encodings.
    """
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]
    content = ""
    used_enc = "utf-8"

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
            used_enc = enc
            break
        except Exception:
            continue

    if not content:
        with open(file_path, "rb") as f:
            content = f.read().decode("utf-8", errors="ignore")

    lines = content.splitlines()
    headings = [l.strip() for l in lines if l.strip().startswith(("#", "===", "---"))]

    return content.strip(), {
        "parser": "text/markdown",
        "encoding": used_enc,
        "line_count": len(lines),
        "headings_detected": len(headings)
    }


def extract_document(file_path_or_obj) -> Tuple[str, Dict[str, Any]]:
    """
    Unified multi-format parser for PDF, DOCX, TXT, CSV, and Markdown.
    Returns (extracted_text, metadata).
    """
    if file_path_or_obj is None:
        return "", {}

    path_str = file_path_or_obj.name if hasattr(file_path_or_obj, "name") else str(file_path_or_obj)
    path_obj = Path(path_str)
    ext = path_obj.suffix.lower()

    if ext == ".pdf":
        text, meta = parse_pdf(path_str)
    elif ext == ".docx":
        text, meta = parse_docx(path_str)
    elif ext == ".csv":
        text, meta = parse_csv(path_str)
    elif ext in [".md", ".markdown", ".txt", ".py", ".json", ".log"]:
        text, meta = parse_markdown_or_txt(path_str)
    else:
        # Default text fallback
        text, meta = parse_markdown_or_txt(path_str)

    meta["filename"] = path_obj.name
    meta["extension"] = ext
    meta["file_size_bytes"] = os.path.getsize(path_str) if os.path.exists(path_str) else len(text.encode("utf-8"))
    meta["char_count"] = len(text)
    meta["word_count"] = len(text.split())

    return text, meta


# =========================================================================
# 2. Intelligent Text Chunking (Section-Aware + Semantic Overlap)
# =========================================================================

class DocumentChunk:
    """Represents a structured semantic chunk of a document."""
    def __init__(
        self,
        chunk_id: str,
        chunk_index: int,
        text: str,
        start_char: int,
        end_char: int,
        section_heading: str = "",
        keywords: Optional[List[str]] = None
    ):
        self.chunk_id = chunk_id
        self.chunk_index = chunk_index
        self.text = text
        self.start_char = start_char
        self.end_char = end_char
        self.section_heading = section_heading
        self.keywords = keywords or []
        self.word_count = len(text.split())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "chunk_index": self.chunk_index,
            "text": self.text,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "section_heading": self.section_heading,
            "keywords": self.keywords,
            "word_count": self.word_count
        }


def chunk_document(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> List[DocumentChunk]:
    """
    Intelligently chunks text by heading, paragraph, and sentence boundaries
    with a sliding window overlap to preserve semantic continuity.
    """
    if not text or not text.strip():
        return []

    cleaned = normalize_text(text)
    chunks: List[DocumentChunk] = []

    # Detect major section headings (markdown '# ...' or capitalized lines)
    lines = cleaned.split("\n")
    current_heading = "General Overview"
    annotated_segments = []

    for line in lines:
        stripped = line.strip()
        if re.match(r"^#{1,4}\s+(.+)", stripped):
            current_heading = re.sub(r"^#{1,4}\s+", "", stripped)
        elif len(stripped) < 60 and stripped.isupper() and len(stripped) > 4:
            current_heading = stripped
        annotated_segments.append((line, current_heading))

    # Reconstruct text with tracked headings
    total_len = len(cleaned)
    start = 0
    chunk_idx = 0

    while start < total_len:
        end = min(start + chunk_size, total_len)

        # Look for natural breakpoint: double newline, single newline, or sentence end
        if end < total_len:
            break_pt = cleaned.rfind("\n\n", start, end)
            if break_pt == -1 or break_pt < start + (chunk_size // 2):
                break_pt = cleaned.rfind("\n", start, end)
            if break_pt == -1 or break_pt < start + (chunk_size // 2):
                break_pt = cleaned.rfind(". ", start, end)
                if break_pt != -1:
                    break_pt += 1 # Include period

            if break_pt != -1 and break_pt > start + (chunk_size // 2):
                end = break_pt

        chunk_text = cleaned[start:end].strip()
        if chunk_text:
            chunk_hash = hashlib.md5(chunk_text.encode("utf-8")).hexdigest()[:8]
            cid = f"chk_{chunk_idx}_{chunk_hash}"
            kw = extract_keywords(chunk_text, top_k=5)

            chunks.append(DocumentChunk(
                chunk_id=cid,
                chunk_index=chunk_idx,
                text=chunk_text,
                start_char=start,
                end_char=end,
                section_heading=current_heading,
                keywords=kw
            ))
            chunk_idx += 1

        if end >= total_len:
            break
        # Slide forward with overlap
        start = max(start + 1, end - chunk_overlap)

    return chunks


# =========================================================================
# 3. Hybrid Search Index (BM25 + TF-IDF + Keyword Match)
# =========================================================================

class DocumentSearchIndex:
    """
    Zero-Model Hybrid Document Search Index combining:
    1. Okapi BM25 Ranking
    2. TF-IDF Cosine Similarity
    3. Exact Keyword Matching Bonus
    """

    def __init__(self, chunks: List[DocumentChunk]):
        self.chunks = chunks
        self.chunk_texts = [c.text for c in chunks]

        # Initialize TF-IDF
        self.tfidf = TFIDFVectorizer()
        self.tfidf_vectors = self.tfidf.fit_transform(self.chunk_texts) if self.chunk_texts else []

        # Initialize Okapi BM25
        self.bm25 = BM25Index(k1=1.5, b=0.75)
        self.bm25.index(self.chunk_texts)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[DocumentChunk, float, Dict[str, Any]]]:
        """
        Executes hybrid search and returns scored chunks with granular scoring metrics.
        Returns: list of (DocumentChunk, combined_score, score_breakdown).
        """
        if not self.chunks or not query.strip():
            return []

        # 1. Okapi BM25 scores
        bm25_raw = self.bm25.score(query)
        max_bm25 = max(bm25_raw) if bm25_raw and max(bm25_raw) > 0 else 1.0
        bm25_norm = [s / max_bm25 for s in bm25_raw]

        # 2. TF-IDF Cosine similarity
        q_vec = self.tfidf.transform(query)
        tfidf_scores = [cosine_similarity(q_vec, d_vec) for d_vec in self.tfidf_vectors]

        # 3. Exact query token matches
        q_tokens = set(remove_stopwords(tokenize_words(query, lower=True)))
        results = []

        for idx, chunk in enumerate(self.chunks):
            c_text_lower = chunk.text.lower()
            exact_hits = sum(1 for t in q_tokens if t in c_text_lower)
            exact_ratio = exact_hits / max(1, len(q_tokens))

            b_score = bm25_norm[idx] if idx < len(bm25_norm) else 0.0
            t_score = tfidf_scores[idx] if idx < len(tfidf_scores) else 0.0

            # Weighted Hybrid Score: 45% BM25 + 35% TF-IDF + 20% Exact Match
            combined = (b_score * 0.45) + (t_score * 0.35) + (exact_ratio * 0.20)

            if combined > 0.05 or exact_hits > 0:
                breakdown = {
                    "bm25_score": round(b_score, 4),
                    "tfidf_score": round(t_score, 4),
                    "exact_matches": exact_hits,
                    "combined_score": round(combined, 4)
                }
                results.append((chunk, combined, breakdown))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]


# =========================================================================
# 4. Passage & Grounded Sentence Extraction
# =========================================================================

def extract_relevant_passages(
    query: str,
    top_chunks: List[Tuple[DocumentChunk, float, Dict[str, Any]]],
    max_sentences: int = 5
) -> List[Dict[str, Any]]:
    """
    Extracts the highest-relevance individual sentences from the top retrieved chunks.
    Ensures answers are grounded directly in verifiable document statements.
    """
    q_tokens = set(remove_stopwords(tokenize_words(query, lower=True)))
    candidate_sentences = []

    for chunk, chunk_score, _ in top_chunks:
        sentences = tokenize_sentences(chunk.text)
        for s in sentences:
            s_tokens = set(remove_stopwords(tokenize_words(s, lower=True)))
            overlap = len(q_tokens & s_tokens)
            if overlap > 0:
                s_score = (overlap / max(1, len(q_tokens))) * 0.7 + chunk_score * 0.3
                candidate_sentences.append({
                    "sentence": s,
                    "score": round(s_score, 4),
                    "chunk_id": chunk.chunk_id,
                    "section": chunk.section_heading,
                    "overlap_terms": list(q_tokens & s_tokens)
                })

    candidate_sentences.sort(key=lambda x: x["score"], reverse=True)
    return candidate_sentences[:max_sentences]


# =========================================================================
# 5. Grounded Q&A Generator (Strict Anti-Hallucination)
# =========================================================================

def answer_document_query(
    query: str,
    index: DocumentSearchIndex,
    min_confidence_threshold: float = 0.15
) -> str:
    """
    Synthesizes a strictly source-grounded response to a user query.
    If the document does not contain sufficient facts to answer,
    it explicitly states so without inventing facts or citations.
    """
    clean_q = query.strip()
    if not clean_q:
        return "⚠️ Please provide a question or topic to search within the document."

    top_chunks = index.search(clean_q, top_k=4)

    # Check confidence threshold
    if not top_chunks or top_chunks[0][1] < min_confidence_threshold:
        return (
            f"### ⚠️ Insufficient Information in Document\n\n"
            f"The provided document **does not contain enough information** to answer the question:\n"
            f"> *\"{clean_q}\"*\n\n"
            f"**Details:**\n"
            f"- Search confidence score: `{top_chunks[0][1] if top_chunks else 0.0:.3f}` (Threshold: `{min_confidence_threshold}`)\n"
            f"- No direct passages or verified facts matching the query terms were found in the uploaded text.\n"
            f"- *Note: In accordance with model-free safety protocols, citations and answers are never fabricated.*"
        )

    passages = extract_relevant_passages(clean_q, top_chunks, max_sentences=4)
    best_chunk, top_score, breakdown = top_chunks[0]

    # Format grounded answer
    answer_lines = [
        f"### 📄 Grounded Document Answer",
        f"**Question:** *\"{clean_q}\"*\n",
        f"**Confidence Score:** `{top_score * 100:.1f}%` (BM25: `{breakdown['bm25_score']:.2f}`, TF-IDF: `{breakdown['tfidf_score']:.2f}`, Matched Terms: `{breakdown['exact_matches']}`)\n",
        f"#### 🔍 Key Findings from Document:"
    ]

    if passages:
        for p in passages:
            answer_lines.append(f"- **{p['sentence']}** *(Section: `{p['section']}`, Chunk: `{p['chunk_id']}`)*")
    else:
        answer_lines.append(f"> {best_chunk.text[:400]}...")

    answer_lines.extend([
        f"\n#### 📑 Source Reference & Context (Chunk `{best_chunk.chunk_id}`):",
        f"```text\n{best_chunk.text}\n```\n",
        f"*Source Section:* **{best_chunk.section_heading}** | *Character Span:* `{best_chunk.start_char} - {best_chunk.end_char}`",
        f"\n---\n*Verified strictly against uploaded content. No generative hallucinations or invented citations.*"
    ])

    return "\n".join(answer_lines)


# =========================================================================
# 6. Document-Based Question & Flashcard Generator
# =========================================================================

def generate_document_questions(
    chunks: List[DocumentChunk],
    num_questions: int = 5
) -> List[Dict[str, Any]]:
    """
    Extracts important sentences and definitions across document chunks
    to generate grounded review questions and flashcard pairs.
    """
    questions = []
    seen_answers = set()

    # Definition patterns: "X is defined as Y", "X refers to Y", "X is a Y"
    def_pattern = re.compile(
        r"\b([A-Z][a-zA-Z0-9_\s]{2,30}?)\s+(?:is defined as|refers to|is an?|denotes|represents)\s+([^.!?\n]{15,150})[.!?]",
        re.IGNORECASE
    )

    for chunk in chunks:
        # Check definitions
        for match in def_pattern.finditer(chunk.text):
            term = match.group(1).strip()
            definition = match.group(2).strip()

            if term.lower() not in seen_answers and len(term.split()) <= 4:
                seen_answers.add(term.lower())
                questions.append({
                    "type": "Definition",
                    "question": f"What is defined as: \"{definition}\"?",
                    "answer": term,
                    "explanation": f"According to chunk {chunk.chunk_id} ({chunk.section_heading}): \"{match.group(0)}\"",
                    "chunk_id": chunk.chunk_id
                })
                if len(questions) >= num_questions:
                    return questions

        # Cloze (Fill-in-the-blank) from salient keyword sentences
        sentences = tokenize_sentences(chunk.text)
        for s in sentences:
            if 30 < len(s) < 180 and len(chunk.keywords) > 0:
                for kw in chunk.keywords:
                    if kw.lower() in s.lower() and kw.lower() not in seen_answers and len(kw) > 3:
                        seen_answers.add(kw.lower())
                        cloze_sentence = re.sub(
                            re.escape(kw),
                            "__________",
                            s,
                            count=1,
                            flags=re.IGNORECASE
                        )
                        questions.append({
                            "type": "Fill-in-the-Blank",
                            "question": f"Complete the statement:\n> {cloze_sentence}",
                            "answer": kw,
                            "explanation": f"Source context: \"{s}\" [Chunk: {chunk.chunk_id}]",
                            "chunk_id": chunk.chunk_id
                        })
                        if len(questions) >= num_questions:
                            return questions
                        break

    return questions

