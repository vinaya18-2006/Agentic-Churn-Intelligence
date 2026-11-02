import unittest

from agents.analysis_agent import build_analysis_context
from agents.orchestrator import run_agent_workflow
from agents.retention_agent import build_retention_context
from agents.retrieval_agent import prepare_retrieved_evidence
from agents.verification_agent import verify_recommendations
from config import get_nexus_config
from dashboard.agent_bridge import run_customer_workflow
from ml.integration import validate_prediction
from rag.integration import EvidenceRetriever
from utils.nexus_client import NexusClient, NexusIntegrationUnavailable


class StaticRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.calls = 0

    def retrieve(self, customer_data, prediction_result):
        self.calls += 1
        self.asserted_customer = customer_data
        self.asserted_prediction = prediction_result
        return self.chunks


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.customer = {"customer_id": "C-1", "tenure": 12}
        self.prediction = {"churn_probability": 0.72}
        self.evidence = [{
            "source_id": "policy-1",
            "text": "Offer a service review to customers reporting outages.",
            "metadata": {"document": "support-policy.pdf", "page": 2},
            "retrieval_method": "hybrid",
        }]

    def test_agent_and_integration_modules_import(self):
        self.assertTrue(callable(build_analysis_context))
        self.assertTrue(callable(build_retention_context))
        self.assertTrue(callable(prepare_retrieved_evidence))
        self.assertTrue(callable(verify_recommendations))
        self.assertTrue(callable(StaticRetriever([]).retrieve))

    def test_orchestrator_orders_retrieval_and_strategy(self):
        retriever = StaticRetriever(self.evidence)
        received_context = {}

        def strategy_generator(context):
            received_context.update(context)
            return [{
                "recommendation": "Offer a service review.",
                "source_ids": ["policy-1"],
                "evidence_quotes": [{
                    "source_id": "policy-1",
                    "quote": "Offer a service review",
                }],
            }]

        result = run_agent_workflow(
            self.customer,
            self.prediction,
            retriever=retriever,
            strategy_generator=strategy_generator,
        )

        self.assertEqual(retriever.calls, 1)
        self.assertEqual(retriever.asserted_customer, self.customer)
        self.assertEqual(retriever.asserted_prediction, self.prediction)
        self.assertEqual(result["workflow_status"], "completed")
        self.assertEqual(result["strategy_status"], "generated")
        self.assertEqual(result["retrieval_status"], "available")
        self.assertEqual(
            result["analysis"]["retrieved_evidence"][0]["metadata"],
            self.evidence[0]["metadata"],
        )
        self.assertEqual(received_context["evidence"], result["retrieved_evidence"])
        self.assertEqual(
            result["recommendations"][0]["status"],
            "references_and_quotes_validated",
        )

    def test_missing_customer_data_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Customer data"):
            run_agent_workflow({}, self.prediction)

    def test_missing_evidence_blocks_strategy_generation(self):
        strategy_called = False

        def strategy_generator(context):
            nonlocal strategy_called
            strategy_called = True
            return []

        result = run_agent_workflow(
            self.customer,
            self.prediction,
            retrieved_chunks=[],
            strategy_generator=strategy_generator,
        )

        self.assertFalse(strategy_called)
        self.assertEqual(
            result["workflow_status"], "blocked_insufficient_evidence"
        )
        self.assertEqual(
            result["strategy_status"], "blocked_insufficient_evidence"
        )
        self.assertEqual(result["recommendations"], [])

    def test_recommendation_with_unknown_source_is_rejected(self):
        result = verify_recommendations(
            {"evidence": self.evidence},
            [{
                "recommendation": "Apply an unlisted discount.",
                "source_ids": ["unknown-policy"],
                "evidence_quotes": [{
                    "source_id": "unknown-policy",
                    "quote": "Apply an unlisted discount",
                }],
            }],
        )

        self.assertEqual(result["verified_recommendations"], [])
        self.assertEqual(result["verification_status"], "needs_review")
        self.assertIn(
            "source IDs",
            result["rejected_recommendations"][0]["reason"],
        )

    def test_unmatched_evidence_quote_is_rejected(self):
        result = verify_recommendations(
            {"evidence": self.evidence},
            [{
                "recommendation": "Apply an unlisted discount.",
                "source_ids": ["policy-1"],
                "evidence_quotes": [{
                    "source_id": "policy-1",
                    "quote": "Apply an unlisted discount",
                }],
            }],
        )

        self.assertEqual(result["verified_recommendations"], [])
        self.assertIn(
            "quotations",
            result["rejected_recommendations"][0]["reason"],
        )

    def test_retrieval_preserves_source_metadata(self):
        prepared = prepare_retrieved_evidence(self.evidence)
        self.assertEqual(prepared[0]["source_id"], "policy-1")
        self.assertEqual(prepared[0]["metadata"], self.evidence[0]["metadata"])
        self.assertEqual(prepared[0]["retrieval_method"], "hybrid")

    def test_dashboard_bridge_import_and_missing_prediction(self):
        result = run_customer_workflow(self.customer, None)
        self.assertEqual(result["workflow_status"], "missing_ml_prediction")

    def test_missing_customer_is_reported_by_dashboard_bridge(self):
        result = run_customer_workflow(None, self.prediction)
        self.assertEqual(result["workflow_status"], "missing_customer_data")

    def test_prediction_validation_does_not_invent_missing_scores(self):
        self.assertIsNone(validate_prediction(None))
        self.assertEqual(
            validate_prediction({"churn_probability": 0.4})[
                "churn_probability"
            ],
            0.4,
        )
        with self.assertRaises(ValueError):
            validate_prediction({"churn_probability": 1.2})

    def test_nexus_configuration_requires_verified_model_setting(self):
        cases = [
            ({}, "Base URL"),
            (
                {"NEXUS_BASE_URL": "https://example.invalid"},
                "API Key",
            ),
            (
                {
                    "NEXUS_BASE_URL": "https://example.invalid",
                    "NEXUS_API_KEY": "test-key-not-a-real-credential",
                },
                "Model ID",
            ),
            (
                {
                    "NEXUS_BASE_URL": "http://example.invalid",
                    "NEXUS_API_KEY": "test-key-not-a-real-credential",
                    "NEXUS_MODEL": "documented-model-id",
                },
                "HTTPS",
            ),
        ]
        for config_values, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    get_nexus_config(config_values)

        config = get_nexus_config({
            "NEXUS_BASE_URL": "https://example.invalid/",
            "NEXUS_API_KEY": "test-key-not-a-real-credential",
            "NEXUS_MODEL": "documented-model-id",
        })
        self.assertEqual(config.base_url, "https://example.invalid")
        self.assertNotIn("test-key-not-a-real-credential", repr(config))

    def test_nexus_client_refuses_unverified_requests(self):
        with self.assertRaises(NexusIntegrationUnavailable):
            NexusClient().generate_recommendations({"evidence": self.evidence})


if __name__ == "__main__":
    unittest.main()
