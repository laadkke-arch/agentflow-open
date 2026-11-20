# Adapted from AF-RES-012 cb602858378db90adb1f085953016267f9afbd6d (src/search.py).
"""Stable ranking over description text alone."""
from collections import Counter
from hashlib import sha256
import json
import re
import unicodedata

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


SEED = 12012
RRF_K = 60
MODEL = "intfloat/multilingual-e5-small"
REVISION = "0a1c1d9ee03224db176563ffcfbc3bbc38f35266"


def tokens(text):
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return re.findall(r"[^\W_]+", normalized)


def json_bytes(value):
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


class LexicalIndex:
    def __init__(self, documents):
        self.model = BM25Okapi([tokens(d) for d in documents], k1=1.5, b=0.75, epsilon=0.25)
        self.size_bytes = json_bytes(
            (self.model.doc_freqs, self.model.doc_len, self.model.idf, self.model.avgdl)
        )

    def scores(self, queries):
        return np.stack([self.model.get_scores(tokens(text)) for text in queries])


class LsaIndex:
    def __init__(self, documents):
        self.vectorizer = TfidfVectorizer(
            tokenizer=tokens, token_pattern=None, lowercase=False, ngram_range=(1, 2),
            sublinear_tf=True, dtype=np.float64,
        )
        matrix = self.vectorizer.fit_transform(documents)
        dimension = min(48, matrix.shape[0] - 1, matrix.shape[1] - 1)
        self.svd = TruncatedSVD(
            n_components=dimension, algorithm="randomized", n_iter=7, random_state=SEED
        )
        self.vectors = normalize(self.svd.fit_transform(matrix))
        self.size_bytes = (
            json_bytes(self.vectorizer.vocabulary_)
            + self.vectorizer.idf_.nbytes
            + self.svd.components_.nbytes
            + self.vectors.nbytes
        )

    def scores(self, queries):
        query_matrix = self.vectorizer.transform(queries)
        query_vectors = normalize(self.svd.transform(query_matrix))
        return query_vectors @ self.vectors.T


class E5Index:
    def __init__(self, documents):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(
            MODEL, revision=REVISION, device="cpu", trust_remote_code=False
        )
        self.model.max_seq_length = 512
        self.vectors = self.encode(documents, "passage")
        self.size_bytes = self.vectors.nbytes

    def encode(self, texts, prefix):
        return self.model.encode(
            [f"{prefix}: {text}" for text in texts], batch_size=16,
            normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False,
        )

    def scores(self, queries):
        return self.encode(queries, "query") @ self.vectors.T


def stable_order(ids):
    return sorted(ids, key=lambda item: (sha256(f"{SEED}/{item}".encode()).digest(), item))


def ranking(scores, tie_order):
    # Round before sorting so insignificant numerical drift does not break exact ties.
    scores = np.round(scores, 12)
    return sorted(range(len(scores)), key=lambda idx: (-scores[idx], tie_order[idx]))


def competition_ranks(scores):
    """Equal component scores get equal RRF contributions, even for a flat query."""
    scores = np.round(scores, 12)
    counts = Counter(scores)
    ranks = {}
    position = 1
    for score, count in sorted(counts.items(), reverse=True):
        ranks[score] = position
        position += count
    return np.asarray([ranks[score] for score in scores], dtype=np.float64)


def reciprocal_rank_fusion(lexical, semantic):
    return np.stack([
        1.0 / (RRF_K + competition_ranks(a)) + 1.0 / (RRF_K + competition_ranks(b))
        for a, b in zip(lexical, semantic, strict=True)
    ])


def has_signal(scores):
    rounded = np.round(scores, 12)
    return bool(np.ptp(rounded))
