
from collections.abc import Mapping
from typing import Any


def build_retention_context(
    analysis_context: dict[str, Any],
    retrieved_evidence: list[dict[str, Any]]
) -> dict[str, Any]:

    if not isinstance(analysis_context, dict):
        raise ValueError("Analysis context must be a dictionary.")

    if not isinstance(retrieved_evidence, list):
        raise ValueError("Retrieved evidence must be a list.")

    if not retrieved_evidence:
        return {
            "status": "insufficient_evidence",
            "recommendations": [],
            "message": (
                "No retrieved evidence is available. "
                "Retention recommendations cannot be generated safely."
            )
        }

    valid_evidence: list[dict[str, Any]] = []

    for item in retrieved_evidence:
        if (
            isinstance(item, Mapping)
            and isinstance(item.get("source_id"), str)
            and item["source_id"].strip()
            and isinstance(item.get("text"), str)
            and item["text"].strip()
        ):
            valid_evidence.append(dict(item))

    if not valid_evidence:
        raise ValueError(
            "Evidence must contain source_id and text fields."
        )

    return {
        "status": "ready_for_llm",
        "customer_context": analysis_context,
        "evidence": valid_evidence,
        "instructions": (
            "Prepare personalized retention recommendations using "
            "only the supplied customer information and retrieved evidence. "
            "Do not invent policies, discounts, or benefits. "
            "For every recommendation, include supporting source IDs and "
            "an exact supporting quotation with its source ID."
        )
    }
