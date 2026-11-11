"""Unit tests for the Advanced RAG evaluation metrics."""

from rag.evaluation import precision_at_k, recall_at_k, mean_reciprocal_rank


def test_precision_at_k():
    relevant = {"doc1", "doc3"}
    retrieved = ["doc1", "doc2", "doc3", "doc4"]
    assert precision_at_k(retrieved, relevant, k=4) == 0.5


def test_recall_at_k():
    relevant = {"doc1", "doc3", "doc5"}
    retrieved = ["doc1", "doc2", "doc3", "doc4"]
    assert recall_at_k(retrieved, relevant, k=4) == 2 / 3


def test_mean_reciprocal_rank_first_result_relevant():
    results = [["doc1", "doc2"], ["doc3", "doc4"]]
    relevant_by_query = [{"doc1"}, {"doc4"}]
    assert mean_reciprocal_rank(results, relevant_by_query) == 0.75


def test_metrics_return_zero_when_no_relevant_results():
    assert precision_at_k(["doc1", "doc2"], set(), k=2) == 0.0
    assert recall_at_k(["doc1", "doc2"], set(), k=2) == 0.0
    assert mean_reciprocal_rank([["doc1"]], [set()]) == 0.0
