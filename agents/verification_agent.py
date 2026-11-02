
from collections.abc import Mapping
from typing import Any


def verify_recommendations(
    retention_context: dict[str, Any],
    recommendations: list[dict[str, Any]]
) -> dict[str, Any]:

    if not isinstance(retention_context, dict):
        raise ValueError("Retention context must be a dictionary.")

    if not isinstance(recommendations, list):
        raise ValueError("Recommendations must be a list.")

    evidence = retention_context.get("evidence", [])

    if not isinstance(evidence, list):
        raise ValueError("Evidence must be a list.")

    available_source_ids = {
        item["source_id"]
        for item in evidence
        if isinstance(item, Mapping)
        and isinstance(item.get("source_id"), str)
        and item["source_id"]
    }
    evidence_by_source_id = {
        item["source_id"]: item["text"]
        for item in evidence
        if isinstance(item, Mapping)
        and isinstance(item.get("source_id"), str)
        and isinstance(item.get("text"), str)
    }

    verified = []
    rejected = []

    for item in recommendations:

        if not isinstance(item, Mapping):
            rejected.append({
                "recommendation": item,
                "reason": "Invalid recommendation format."
            })
            continue

        text = item.get("recommendation")
        source_ids = item.get("source_ids", [])

        if not isinstance(text, str) or not text.strip():
            rejected.append({
                "recommendation": item,
                "reason": "Recommendation text is missing."
            })
            continue

        if not isinstance(source_ids, list) or not source_ids:
            rejected.append({
                "recommendation": text,
                "reason": "No supporting source IDs provided."
            })
            continue

        if not all(
            isinstance(source_id, str)
            and source_id in available_source_ids
            for source_id in source_ids
        ):
            rejected.append({
                "recommendation": text,
                "reason": "One or more source IDs are not available."
            })
            continue

        evidence_quotes = item.get("evidence_quotes")
        if not isinstance(evidence_quotes, list) or not evidence_quotes:
            rejected.append({
                "recommendation": text,
                "reason": "No exact supporting evidence quotation provided."
            })
            continue

        invalid_quote = any(
            not isinstance(quote, Mapping)
            or not isinstance(quote.get("source_id"), str)
            or quote["source_id"] not in source_ids
            or not isinstance(quote.get("quote"), str)
            or not quote["quote"].strip()
            or quote["quote"] not in evidence_by_source_id.get(
                quote["source_id"], ""
            )
            for quote in evidence_quotes
        )
        if invalid_quote:
            rejected.append({
                "recommendation": text,
                "reason": (
                    "One or more supporting quotations do not exactly match "
                    "the cited retrieved evidence."
                )
            })
            continue

        verified.append({
            "recommendation": text,
            "source_ids": list(source_ids),
            "evidence_quotes": [dict(quote) for quote in evidence_quotes],
            "status": "references_and_quotes_validated"
        })

    return {
        "verified_recommendations": verified,
        "rejected_recommendations": rejected,
        "verification_status": (
            (
                "needs_review"
                if rejected
                else "references_validated"
                if verified
                else "no_recommendations"
            )
        )
    }
