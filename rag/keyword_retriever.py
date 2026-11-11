"""BM25 keyword retriever."""
from __future__ import annotations
import re
from typing import Any

def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())

class BM25KeywordRetriever:
    def __init__(self):
        self._chunks: list[dict[str, Any]] = []
        self._index = None

    def fit(self, chunks: list[dict[str, Any]]) -> None:
        try:
            from rank_bm25 import BM25Okapi
        except ImportError as exc:
            raise RuntimeError("Install rank-bm25 to use keyword retrieval.") from exc
        self._chunks = list(chunks)
        self._index = BM25Okapi([tokenize(c["text"]) for c in self._chunks]) if chunks else None

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if self._index is None or top_k < 1:
            return []
        scores = self._index.get_scores(tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return [{"id": self._chunks[i]["id"], "text": self._chunks[i]["text"],
                 "metadata": self._chunks[i]["metadata"], "score": float(score)}
                for i, score in ranked[:top_k] if score > 0]
