"""Bridge between dashboard records and the agent orchestration workflow."""

from collections.abc import Mapping
from typing import Any

from agents.orchestrator import run_agent_workflow
from ml.integration import validate_prediction
from rag.integration import EvidenceRetriever
from utils.nexus_client import RecommendationGenerator


def run_customer_workflow(
    customer_data: Mapping[str, Any] | None,
    prediction_result: Mapping[str, Any] | None,
    *,
    retriever: EvidenceRetriever | None = None,
    strategy_generator: RecommendationGenerator | None = None,
) -> dict[str, Any]:
    """Run only configured workflow stages and report missing prerequisites."""
    if not isinstance(customer_data, Mapping) or not customer_data:
        return {
            "workflow_status": "missing_customer_data",
            "message": "A non-empty customer record is required.",
        }

    validated_prediction = validate_prediction(prediction_result)
    if validated_prediction is None:
        return {
            "workflow_status": "missing_ml_prediction",
            "message": (
                "No ML prediction was supplied. The agent workflow was not run."
            ),
        }

    return run_agent_workflow(
        dict(customer_data),
        validated_prediction,
        retriever=retriever,
        strategy_generator=strategy_generator,
    )
