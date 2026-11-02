
from typing import Any


def build_analysis_context(
    customer_data: dict[str, Any],
    prediction_result: dict[str, Any],
    retrieved_evidence: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """
    Prepare customer information and ML prediction
    for the next stage of the agent workflow.
    """

    if not isinstance(customer_data, dict) or not customer_data:
        raise ValueError("Customer data must be a non-empty dictionary.")

    if not isinstance(prediction_result, dict) or not prediction_result:
        raise ValueError("Prediction result must be a non-empty dictionary.")

    analysis_context = {
        "customer_data": customer_data.copy(),
        "prediction_result": prediction_result.copy(),
        "retrieved_evidence": retrieved_evidence or [],
        "analysis_status": (
            "evidence_available"
            if retrieved_evidence
            else "insufficient_evidence"
        ),
        "message": (
            "Customer information and the supplied churn prediction are "
            "available. Retrieved evidence is required before explaining "
            "churn factors or suggesting retention actions."
        )
    }

    return analysis_context
