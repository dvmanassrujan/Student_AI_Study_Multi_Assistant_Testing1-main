"""
Model-Free Natural Language Processing Engine.
Provides deterministic, algorithm-based NLP capabilities:
1. Text Preprocessing & Normalization
2. Tokenization & Sentence Segmentation
3. Stop-Word Removal & Vocabulary Filtering
4. Morphological Stemming & Lemmatization
5. Keyword Extraction (Frequency, Position, RAKE-inspired co-occurrence)
6. TF-IDF Vectorization with sublinear scaling & L2 normalization
7. Okapi BM25 Ranking with document length normalization
8. Cosine Similarity Computation
9. Rule-Based Intent Classification
"""

import re
import math
import unicodedata
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set, Optional, Any

# =========================================================================
# 1. Comprehensive English Stop-Words (Model-Free Standard Lexicon)
# =========================================================================

STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
    "your", "yours", "yourself", "yourselves", "also", "just", "like", "will"
}

# English Contractions Expansion Map
CONTRACTIONS: Dict[str, str] = {
    "can't": "cannot",
    "won't": "will not",
    "shan't": "shall not",
    "n't": " not",
    "'re": " are",
    "'s": " is",
    "'d": " would",
    "'ll": " will",
    "'ve": " have",
    "'m": " am",
}

# Irregular Lemmatization Dictionary
IRREGULAR_LEMMAS: Dict[str, str] = {
    "children": "child", "men": "man", "women": "woman", "people": "person",
    "mice": "mouse", "feet": "foot", "teeth": "tooth", "geese": "goose",
    "matrices": "matrix", "indices": "index", "vertices": "vertex",
    "criteria": "criterion", "phenomena": "phenomenon", "data": "datum",
    "analyses": "analysis", "hypotheses": "hypothesis", "diagnoses": "diagnosis",
    "theses": "thesis", "crises": "crisis",
    "was": "be", "were": "be", "is": "be", "are": "be", "am": "be", "been": "be",
    "has": "have", "had": "have", "having": "have",
    "does": "do", "did": "do", "done": "do", "doing": "do",
    "went": "go", "gone": "go", "goes": "go",
    "wrote": "write", "written": "write", "writes": "write",
    "ran": "run", "running": "run", "runs": "run",
    "better": "good", "best": "good", "worse": "bad", "worst": "bad"
}

# Common abbreviations to prevent false sentence splits
ABBREVIATIONS: Set[str] = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "vs", "etc", "e.g", "i.e",
    "fig", "vol", "no", "dept", "univ", "u.s", "u.k", "approx", "est", "al"
}


# =========================================================================
# 2. Text Normalization & Preprocessing
# =========================================================================

def normalize_text(text: str, expand_contractions: bool = True) -> str:
    """
    Normalizes text by standardizing unicode, expanding contractions,
    converting smart quotes/dashes, and cleaning irregular whitespace.
    """
    if not text:
        return ""

    # Normalize unicode characters (NFKD)
    normalized = unicodedata.normalize("NFKD", text)

    # Standardize curly quotes and apostrophes
    normalized = normalized.replace("’", "'").replace("‘", "'")
    normalized = normalized.replace("“", '"').replace("”", '"')
    normalized = normalized.replace("—", " - ").replace("–", " - ")

    # Expand common contractions if requested
    if expand_contractions:
        for contr, full in CONTRACTIONS.items():
            normalized = re.sub(re.escape(contr), full, normalized, flags=re.IGNORECASE)

    # Collapse multiple whitespaces and tabs (preserve newlines for structure)
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\r\n|\r", "\n", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)

    return normalized.strip()


# =========================================================================
# 3. Tokenization & Sentence Segmentation
# =========================================================================

def tokenize_sentences(text: str) -> List[str]:
    """
    Splits text into coherent sentences using an intelligent rule-based boundary
    detector that protects abbreviations, decimals, bullet points, and acronyms.
    """
    if not text or not text.strip():
        return []

    cleaned = normalize_text(text, expand_contractions=False)

    # Protect decimals: replace '3.14' with '3<DECIMAL>14'
    protected = re.sub(r"(\d+)\.(\d+)", r"\1<DECIMAL>\2", cleaned)

    # Protect common abbreviations: replace 'Dr.' with 'Dr<DOT>'
    def protect_abbr(match):
        token = match.group(0)
        return token.replace(".", "<DOT>")

    pattern = r"\b(" + "|".join(re.escape(a) for a in ABBREVIATIONS) + r")\."
    protected = re.sub(pattern, protect_abbr, protected, flags=re.IGNORECASE)

    # Protect ellipses
    protected = re.sub(r"\.{3,}", "<ELLIPSIS>", protected)

    # Protect URLs and emails
    protected = re.sub(r"(https?://\S+)", lambda m: m.group(0).replace(".", "<DOT>"), protected)
    protected = re.sub(r"(\b[\w.-]+@[\w.-]+\.\w+\b)", lambda m: m.group(0).replace(".", "<DOT>"), protected)

    # Sentence boundary regex: split on period/question/exclamation followed by whitespace or line break
    sentence_delimiters = re.compile(r"(?<=[.!?])(?:\s+|\n+)(?=[A-Z0-9\"'(\[])")
    raw_sentences = sentence_delimiters.split(protected)

    sentences = []
    for s in raw_sentences:
        # Also split on paragraph double-newlines if multiple statements are on separate lines
        line_splits = s.split("\n\n")
        for chunk in line_splits:
            restored = (
                chunk.replace("<DECIMAL>", ".")
                .replace("<DOT>", ".")
                .replace("<ELLIPSIS>", "...")
                .strip()
            )
            # Remove stray markdown bullet indicators at sentence start
            clean_s = re.sub(r"^(?:[-*•]|\d+\.)\s+", "", restored).strip()
            if clean_s and len(clean_s) > 3:
                sentences.append(clean_s)

    # Fallback if no sentences detected
    if not sentences and cleaned:
        sentences = [cleaned]

    return sentences


def tokenize_words(text: str, lower: bool = True, strip_punct: bool = True) -> List[str]:
    """
    Splits text into words/tokens using deterministic regular expression extraction.
    """
    if not text:
        return []

    norm = normalize_text(text)
    if lower:
        norm = norm.lower()

    if strip_punct:
        # Extract alphanumeric words and hyphenated compound terms
        tokens = re.findall(r"\b[a-zA-Z0-9]+(?:'[a-zA-Z]+)?\b", norm)
    else:
        tokens = re.findall(r"\w+|[^\w\s]", norm)

    return tokens


def remove_stopwords(tokens: List[str], custom_stopwords: Optional[Set[str]] = None) -> List[str]:
    """Filters out stop-words and single-character noise tokens."""
    stop_set = STOPWORDS if custom_stopwords is None else (STOPWORDS | custom_stopwords)
    return [t for t in tokens if t.lower() not in stop_set and (len(t) > 1 or t.isalnum())]


# =========================================================================
# 4. Morphological Stemming & Lemmatization
# =========================================================================

def stem(word: str) -> str:
    """
    Fast, deterministic Porter-style suffix stripping stemmer implemented in pure Python.
    Normalizes plurals, verb conjugations, and common derivational affixes.
    """
    w = word.lower().strip()
    if len(w) <= 3:
        return w

    # Check irregular lemma dictionary first
    if w in IRREGULAR_LEMMAS:
        return IRREGULAR_LEMMAS[w]

    # Step 1: Plurals and past tense
    if w.endswith("sses"):
        w = w[:-2]
    elif w.endswith("ies") and len(w) > 4:
        w = w[:-3] + "y"
    elif w.endswith("ss"):
        pass
    elif w.endswith("s") and not w.endswith("us") and not w.endswith("is"):
        w = w[:-1]

    # Step 2: Past tense and progressive
    if w.endswith("eed") and len(w) > 4:
        w = w[:-1]
    elif (w.endswith("ed") or w.endswith("ing")) and len(w) > 4:
        stem_base = w[:-2] if w.endswith("ed") else w[:-3]
        # Double consonant reduction (e.g. running -> run, stopped -> stop)
        if len(stem_base) >= 3 and stem_base[-1] == stem_base[-2] and stem_base[-1] not in "lsz":
            stem_base = stem_base[:-1]
        w = stem_base

    # Step 3: Derivational suffixes
    suffixes = [
        ("ational", "ate"), ("tional", "tion"), ("ization", "ize"),
        ("ation", "ate"), ("ator", "ate"), ("alism", "al"),
        ("iveness", "ive"), ("ful", ""), ("ness", ""),
        ("ment", ""), ("able", ""), ("ible", ""), ("ance", ""),
        ("ence", ""), ("ity", "")
    ]
    for suf, repl in suffixes:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            w = w[:-len(suf)] + repl
            break

    return w


def lemmatize_tokens(tokens: List[str]) -> List[str]:
    """Applies stemming/lemmatization across a list of tokens."""
    return [stem(t) for t in tokens]


# =========================================================================
# 5. Keyword Extraction (Frequency + Position + Co-occurrence)
# =========================================================================

def extract_keywords(
    text: str,
    top_k: int = 10,
    min_word_len: int = 3,
    include_scores: bool = False
) -> Any:
    """
    Extracts the most salient keywords using:
    - Term frequency
    - Sentence position weighting (earlier sentences often contain core thesis)
    - Length bonus for domain-specific technical vocabulary
    - Word co-occurrence / degree scoring (RAKE-inspired)
    """
    if not text:
        return []

    sentences = tokenize_sentences(text)
    words_by_sentence = []
    all_content_words = []

    for s_idx, s in enumerate(sentences):
        tokens = tokenize_words(s, lower=True)
        content_words = [
            t for t in tokens
            if t not in STOPWORDS and len(t) >= min_word_len and not t.isdigit()
        ]
        words_by_sentence.append((s_idx, content_words))
        all_content_words.extend(content_words)

    if not all_content_words:
        return []

    word_freq = Counter(all_content_words)
    total_words = len(all_content_words)
    total_sentences = max(1, len(sentences))

    # Co-occurrence graph (degree calculation)
    co_occurrences: Dict[str, Set[str]] = defaultdict(set)
    for _, s_words in words_by_sentence:
        for i, w1 in enumerate(s_words):
            for j in range(max(0, i - 2), min(len(s_words), i + 3)):
                if i != j:
                    co_occurrences[w1].add(s_words[j])

    scores: Dict[str, float] = {}
    for word, freq in word_freq.items():
        # Frequency component
        tf_score = 1.0 + math.log(freq)

        # Degree component (RAKE metric: degree / frequency)
        degree = len(co_occurrences[word]) + freq
        rake_score = degree / (freq + 0.1)

        # Position weighting: bonus for words appearing in the first 25% of text
        pos_bonus = 0.0
        for s_idx, s_words in words_by_sentence:
            if word in s_words:
                rel_pos = s_idx / total_sentences
                if rel_pos <= 0.25:
                    pos_bonus += 0.35
                elif rel_pos <= 0.5:
                    pos_bonus += 0.15

        # Length bonus (longer technical terms like 'backpropagation', 'polymorphism')
        len_bonus = min(0.3, len(word) * 0.02)

        total_score = (tf_score * 0.45) + (rake_score * 0.35) + pos_bonus + len_bonus
        scores[word] = round(total_score, 4)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    if include_scores:
        return ranked
    return [word for word, _ in ranked]


# =========================================================================
# 6. TF-IDF Vectorizer (Sublinear Scaling + L2 Normalization)
# =========================================================================

class TFIDFVectorizer:
    """
    Deterministic Model-Free TF-IDF Vectorizer.
    Transforms document collections into sparse normalized feature vectors.
    """

    def __init__(self, min_df: int = 1, max_df_ratio: float = 0.95):
        self.min_df = min_df
        self.max_df_ratio = max_df_ratio
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_count: int = 0

    def fit(self, documents: List[str]) -> "TFIDFVectorizer":
        """Builds vocabulary and computes smoothed inverse document frequencies."""
        self.doc_count = len(documents)
        if self.doc_count == 0:
            return self

        doc_frequencies: Counter = Counter()

        for doc in documents:
            tokens = set(remove_stopwords(tokenize_words(doc, lower=True)))
            for token in tokens:
                doc_frequencies[token] += 1

        # Filter by min_df and max_df_ratio
        max_df = max(1, int(self.doc_count * self.max_df_ratio))
        valid_words = [
            w for w, df in doc_frequencies.items()
            if df >= self.min_df and (self.doc_count <= 2 or df <= max_df)
        ]

        valid_words.sort()
        self.vocab = {w: idx for idx, w in enumerate(valid_words)}

        # Smoothed BM25/Lucene style IDF
        N = self.doc_count
        for word in self.vocab:
            df = doc_frequencies[word]
            # idf = ln(1 + (N - df + 0.5) / (df + 0.5)) + 1
            self.idf[word] = math.log(1.0 + (N - df + 0.5) / (df + 0.5)) + 1.0

        return self

    def transform(self, document: str) -> Dict[str, float]:
        """
        Transforms a document into a sparse L2-normalized TF-IDF dictionary.
        Returns {term: normalized_weight}.
        """
        tokens = remove_stopwords(tokenize_words(document, lower=True))
        if not tokens:
            return {}

        tf_counts = Counter(tokens)
        vector: Dict[str, float] = {}

        for word, count in tf_counts.items():
            if word in self.vocab:
                # Sublinear term frequency scaling
                tf_val = 1.0 + math.log(count)
                vector[word] = tf_val * self.idf[word]

        # L2-normalize vector: sum(v^2) = 1.0
        norm_sq = sum(val * val for val in vector.values())
        if norm_sq > 0:
            norm = math.sqrt(norm_sq)
            vector = {k: v / norm for k, v in vector.items()}

        return vector

    def fit_transform(self, documents: List[str]) -> List[Dict[str, float]]:
        self.fit(documents)
        return [self.transform(doc) for doc in documents]


# =========================================================================
# 7. Okapi BM25 Ranking Engine
# =========================================================================

class BM25Index:
    """
    Okapi BM25 ranking algorithm with document length normalization.
    Parameters:
        k1: Controls term frequency saturation (default 1.5)
        b:  Controls degree of document length penalty (default 0.75)
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size: int = 0
        self.avg_doc_len: float = 0.0
        self.doc_lengths: List[int] = []
        self.doc_token_counts: List[Counter] = []
        self.idf: Dict[str, float] = {}

    def index(self, documents: List[str]):
        """Indexes raw document texts for BM25 retrieval."""
        self.corpus_size = len(documents)
        if self.corpus_size == 0:
            return

        self.doc_lengths = []
        self.doc_token_counts = []
        total_len = 0
        df: Counter = Counter()

        for doc in documents:
            tokens = remove_stopwords(tokenize_words(doc, lower=True))
            t_len = len(tokens)
            self.doc_lengths.append(t_len)
            total_len += t_len
            t_counts = Counter(tokens)
            self.doc_token_counts.append(t_counts)
            for word in t_counts:
                df[word] += 1

        self.avg_doc_len = total_len / float(self.corpus_size) if self.corpus_size > 0 else 0.0

        # Calculate Okapi BM25 IDF
        for word, freq in df.items():
            self.idf[word] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

    def score(self, query: str) -> List[float]:
        """Calculates BM25 score for every document against the query."""
        if self.corpus_size == 0:
            return []

        query_tokens = remove_stopwords(tokenize_words(query, lower=True))
        scores = [0.0] * self.corpus_size

        for q_term in query_tokens:
            if q_term not in self.idf:
                continue

            term_idf = self.idf[q_term]
            for doc_idx in range(self.corpus_size):
                tf = self.doc_token_counts[doc_idx].get(q_term, 0)
                if tf == 0:
                    continue

                d_len = self.doc_lengths[doc_idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (d_len / (self.avg_doc_len or 1.0)))
                scores[doc_idx] += term_idf * (numerator / denominator)

        return scores

    def rank(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """Returns list of (doc_index, score) sorted in descending score order."""
        scores = self.score(query)
        indexed_scores = [(idx, s) for idx, s in enumerate(scores) if s > 0.0]
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        return indexed_scores[:top_k]


# =========================================================================
# 8. Vector Cosine Similarity
# =========================================================================

def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """
    Computes cosine similarity between two sparse dictionaries.
    Since TFIDFVectorizer vectors are already L2 normalized,
    cosine similarity is simply the dot product.
    """
    if not vec1 or not vec2:
        return 0.0

    # Iterate over smaller dictionary for maximum speed
    if len(vec1) > len(vec2):
        vec1, vec2 = vec2, vec1

    dot_product = sum(val * vec2.get(term, 0.0) for term, val in vec1.items())
    return max(0.0, min(1.0, dot_product))


# =========================================================================
# 9. Rule-Based Intent Classification
# =========================================================================

INTENT_RULES: Dict[str, Dict[str, Any]] = {
    "study_planner": {
        "keywords": ["study plan", "study schedule", "timetable", "revision plan", "hours per day",
                     "study roadmap", "learning roadmap", "curriculum", "milestone", "schedule"],
        "regex": [r"\b(plan|schedule|timetable|roadmap|routine)\b.*(study|learn|exam|revision|semester)"],
        "weight": 2.0
    },
    "exam": {
        "keywords": ["exam", "quiz", "mock test", "test questions", "mcq", "multiple choice",
                     "practice questions", "assessment", "flashcard", "cloze", "fill in the blank"],
        "regex": [r"\b(quiz|exam|mock test|mcq|test prep|practice test)\b"],
        "weight": 2.0
    },
    "coding": {
        "keywords": ["debug", "def ", "function", "class ", "python", "java", "c++", "javascript",
                     "algorithm", "dsa", "syntax error", "runtime error", "leetcode", "complexity",
                     "big-o", "time complexity", "space complexity", "code review", "refactor"],
        "regex": [
            r"\b(def|class|import|return|console\.log|printf|public static void)\b",
            r"\b(debug|syntax|traceback|indentationerror|typeerror|indexerror)\b",
            r"\b(binary search|linked list|dynamic programming|sorting|tree|graph)\b"
        ],
        "weight": 2.2
    },
    "document": {
        "keywords": ["document", "pdf", "docx", "notes", "summarize notes", "summarize this text",
                     "extract passage", "document search", "rag", "article"],
        "regex": [r"\b(summarize|extract|analyze)\b.*(document|pdf|text|notes|paper)"],
        "weight": 1.8
    },
    "project": {
        "keywords": ["project idea", "project architecture", "tech stack", "build an app",
                     "module breakdown", "database schema", "system design", "system architecture"],
        "regex": [r"\b(project|architecture|system design|schema|stack)\b"],
        "weight": 1.9
    },
    "memory": {
        "keywords": ["flashcard", "flashcards", "mnemonic", "spaced repetition", "anki", "memorize"],
        "regex": [r"\b(flashcard|mnemonic|memorize|spaced repetition)\b"],
        "weight": 2.0
    },
    "audio": {
        "keywords": ["audio script", "podcast script", "voiceover", "spoken explanation", "tts", "read aloud"],
        "regex": [r"\b(audio|voice|podcast|tts)\b"],
        "weight": 1.7
    },
    "video": {
        "keywords": ["video script", "storyboard", "scene 1", "visual cue", "create a video script", "cartoon"],
        "regex": [r"\b(video script|storyboard|visual cue|animation)\b"],
        "weight": 1.7
    }
}

def classify_intent(text: str) -> str:
    """
    Classifies user prompt into specific academic intent categories
    using high-precision deterministic pattern matching and keyword scoring.
    Defaults to 'study' (general academic tutor) if no specific intent fires.
    """
    if not text:
        return "study"

    clean = normalize_text(text).lower()

    scores: Dict[str, float] = defaultdict(float)

    for intent, rule in INTENT_RULES.items():
        weight = rule["weight"]

        # 1. Exact phrase keyword matching
        for kw in rule["keywords"]:
            if kw in clean:
                scores[intent] += (weight * 2.0)

        # 2. Regular expression checks
        for pattern in rule["regex"]:
            if re.search(pattern, clean, flags=re.IGNORECASE):
                scores[intent] += (weight * 2.5)

    if not scores:
        return "study"

    best_intent, best_score = max(scores.items(), key=lambda x: x[1])
    return best_intent if best_score >= 2.0 else "study"

