
from collections.abc import Mapping
from typing import Any


def prepare_retrieved_evidence(
    retrieved_chunks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Validate and prepare RAG search results
    for the Retention Strategy Agent.
    """

    if not isinstance(retrieved_chunks, list):
        raise ValueError("Retrieved chunks must be a list.")

    evidence: list[dict[str, Any]] = []

    for chunk in retrieved_chunks:

        if not isinstance(chunk, Mapping):
            continue

        source_id = chunk.get("source_id")
        text = chunk.get("text")

        if (
            isinstance(source_id, str)
            and source_id.strip()
            and isinstance(text, str)
            and text.strip()
        ):
            prepared_chunk = dict(chunk)
            prepared_chunk["source_id"] = source_id.strip()
            prepared_chunk["text"] = text.strip()
            metadata = chunk.get("metadata")
            if isinstance(metadata, Mapping):
                prepared_chunk["metadata"] = dict(metadata)
            evidence.append(prepared_chunk)

    return evidence
