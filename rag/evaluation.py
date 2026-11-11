"""Basic retrieval metrics for labeled query-to-document evaluation."""
from __future__ import annotations

def precision_at_k(retrieved: list[str], relevant: set[str], k: int = 5) -> float:
    if k < 1: raise ValueError("k must be >= 1")
    selected = retrieved[:k]
    return sum(item in relevant for item in selected) / k

def recall_at_k(retrieved: list[str], relevant: set[str], k: int = 5) -> float:
    if k < 1: raise ValueError("k must be >= 1")
    if not relevant: return 0.0
    return sum(item in relevant for item in retrieved[:k]) / len(relevant)

def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    for rank, item in enumerate(retrieved, start=1):
        if item in relevant: return 1.0 / rank
    return 0.0

def evaluate(results: dict[str, list[str]], qrels: dict[str, set[str]], k: int = 5) -> dict[str, float]:
    queries = [q for q in results if q in qrels]
    if not queries: return {"precision_at_k": 0.0, "recall_at_k": 0.0, "mrr": 0.0, "query_count": 0}
    n = len(queries)
    return {
        "precision_at_k": sum(precision_at_k(results[q], qrels[q], k) for q in queries) / n,
        "recall_at_k": sum(recall_at_k(results[q], qrels[q], k) for q in queries) / n,
        "mrr": sum(reciprocal_rank(results[q], qrels[q]) for q in queries) / n,
        "query_count": n,
    }

def mean_reciprocal_rank(
    results: list[list[str]],
    relevant_by_query: list[set[str]]
) -> float:
    """Calculate mean reciprocal rank across multiple queries."""
    if len(results) != len(relevant_by_query):
        raise ValueError("Results and relevance labels must have equal lengths")

    if not results:
        return 0.0

    scores = [
        reciprocal_rank(retrieved, relevant)
        for retrieved, relevant in zip(results, relevant_by_query)
    ]

    return sum(scores) / len(scores)

