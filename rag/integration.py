"""Stable contract for integrating hybrid RAG evidence retrieval."""

from collections.abc import Mapping
from typing import Any, Protocol

from utils.integration_errors import IntegrationError


class RetrievalIntegrationError(IntegrationError):
    """A safe, explicit failure from an installed retrieval provider."""


class EvidenceRetriever(Protocol):
    """Expected interface for a retriever returning source-bearing chunks."""

    def retrieve(
        self,
        customer_data: Mapping[str, Any],
        prediction_result: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        """Return chunks with ``source_id`` and ``text`` fields."""
