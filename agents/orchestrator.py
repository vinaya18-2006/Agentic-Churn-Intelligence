
from typing import Any

from agents.analysis_agent import build_analysis_context
from agents.retrieval_agent import prepare_retrieved_evidence
from agents.retention_agent import build_retention_context
from agents.verification_agent import verify_recommendations
from rag.integration import EvidenceRetriever
from utils.nexus_client import RecommendationGenerator


def run_agent_workflow(
    customer_data: dict[str, Any],
    prediction_result: dict[str, Any],
    retrieved_chunks: list[dict[str, Any]] | None = None,
    recommendations: list[dict[str, Any]] | None = None,
    *,
    retriever: EvidenceRetriever | None = None,
    strategy_generator: RecommendationGenerator | None = None
) -> dict:
    """
    Retrieve evidence, analyze customer inputs, prepare a strategy, and verify it.
    """
    if not isinstance(customer_data, dict) or not customer_data:
        raise ValueError("Customer data must be a non-empty dictionary.")
    if not isinstance(prediction_result, dict) or not prediction_result:
        raise ValueError("Prediction result must be a non-empty dictionary.")
    if retrieved_chunks is not None and retriever is not None:
        raise ValueError(
            "Provide retrieved_chunks or a retriever, not both."
        )
    retrieval_requested = retrieved_chunks is not None or retriever is not None

    # Retrieval precedes analysis so the same validated evidence reaches each agent.
    if retriever is not None:
        retrieved_chunks = retriever.retrieve(customer_data, prediction_result)
        if not isinstance(retrieved_chunks, list):
            raise TypeError("The retriever must return a list of evidence chunks.")

    if retrieved_chunks is None:
        retrieved_chunks = []
    elif not isinstance(retrieved_chunks, list):
        raise TypeError("Retrieved chunks must be a list.")
    evidence = prepare_retrieved_evidence(retrieved_chunks)

    # Step 1: Analyze customer and supplied ML prediction with retrieved evidence.
    analysis_context = build_analysis_context(
        customer_data,
        prediction_result,
        evidence
    )

    # Step 2: Prepare the evidence-grounded retention strategy context.
    retention_context = build_retention_context(
        analysis_context,
        evidence
    )

    if recommendations is not None and strategy_generator is not None:
        raise ValueError(
            "Provide recommendations or a strategy generator, not both."
        )

    generated_recommendations: list[dict[str, Any]] = []
    if recommendations is not None:
        generated_recommendations = recommendations
        strategy_status = "provided"
    elif evidence and strategy_generator is not None:
        generated_recommendations = strategy_generator(retention_context)
        if not isinstance(generated_recommendations, list):
            raise TypeError(
                "The strategy generator must return a list of recommendations."
            )
        strategy_status = "generated"
    elif not evidence:
        strategy_status = "blocked_insufficient_evidence"
    else:
        strategy_status = "unavailable"

    # Step 3: Reject candidates without valid evidence references and quotations.
    verification_result = verify_recommendations(
        retention_context,
        generated_recommendations
    )

    if not evidence:
        workflow_status = "blocked_insufficient_evidence"
    elif verification_result["rejected_recommendations"]:
        workflow_status = "needs_review"
    elif strategy_status == "unavailable":
        workflow_status = "awaiting_strategy_generator"
    else:
        workflow_status = "completed"

    return {
        "analysis": analysis_context,
        "retrieved_evidence": evidence,
        "retention_context": retention_context,
        "recommendations": verification_result["verified_recommendations"],
        "verification": verification_result,
        "retrieval_status": (
            "available"
            if evidence
            else "no_evidence"
            if retrieval_requested
            else "unavailable"
        ),
        "strategy_status": strategy_status,
        "workflow_status": workflow_status
    }
