"""Adapter implementing the repository's existing EvidenceRetriever contract."""
from __future__ import annotations
import json
from collections.abc import Mapping
from typing import Any
from .integration import EvidenceRetriever, RetrievalIntegrationError
from .rag_pipeline import RAGPipeline

class CustomerChurnEvidenceRetriever(EvidenceRetriever):
    def __init__(self, pipeline: RAGPipeline | None = None, top_k: int = 5):
        self.pipeline = pipeline or RAGPipeline()
        self.top_k = top_k

    def retrieve(self, customer_data: Mapping[str, Any],
                 prediction_result: Mapping[str, Any]) -> list[dict[str, Any]]:
        try:
            # Serialize only supplied context; callers should avoid passing secrets/credentials.
            query = "Customer context: " + json.dumps(dict(customer_data), default=str)
            query += "\nChurn prediction context: " + json.dumps(dict(prediction_result), default=str)
            if not customer_data and not prediction_result:
                return []
            return self.pipeline.retrieve(query, self.top_k)
        except Exception as exc:
            raise RetrievalIntegrationError(f"Customer churn evidence retrieval failed: {exc}") from exc
