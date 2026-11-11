"""Hybrid semantic + BM25 retrieval using reciprocal-rank fusion."""
from __future__ import annotations
from typing import Any

class HybridRetriever:
    def __init__(self, vector_store, embedding_model, keyword_retriever,
                 semantic_weight: float = 1.0, keyword_weight: float = 1.0, rrf_k: int = 60):
        if semantic_weight < 0 or keyword_weight < 0 or semantic_weight + keyword_weight == 0:
            raise ValueError("Retrieval weights must be non-negative and not both zero.")
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.keyword_retriever = keyword_retriever
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        self.rrf_k = rrf_k

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        semantic = self.vector_store.search(self.embedding_model.encode([query])[0], top_k)
        keyword = self.keyword_retriever.search(query, top_k)
        merged: dict[str, dict[str, Any]] = {}
        for weight, rows in ((self.semantic_weight, semantic), (self.keyword_weight, keyword)):
            for rank, row in enumerate(rows, start=1):
                key = row["id"]
                if key not in merged:
                    merged[key] = {**row, "rrf_score": 0.0}
                merged[key]["rrf_score"] += weight / (self.rrf_k + rank)
        return sorted(merged.values(), key=lambda r: r["rrf_score"], reverse=True)[:top_k]
