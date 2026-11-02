import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class DashboardAppTests(unittest.TestCase):
    def test_customer_analytics_runs_with_explicit_evidence_block(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path), default_timeout=30).run()
        self.assertFalse(app.exception)

        app.sidebar.radio[0].set_value("Customer Analytics").run()
        self.assertFalse(app.exception)

        load_demo_button = next(
            button
            for button in app.button
            if button.label == "Load Demo Dashboard"
        )
        load_demo_button.click().run()
        self.assertFalse(app.exception)

        workflow_button = next(
            button
            for button in app.button
            if button.label == "Run customer workflow"
        )
        workflow_button.click().run()
        self.assertFalse(app.exception)

        rendered_markdown = " ".join(
            str(item.value) for item in app.markdown
        )
        self.assertIn("blocked_insufficient_evidence", rendered_markdown)
        self.assertTrue(
            any("Recommendations are blocked" in str(item.value)
                for item in app.warning)
        )
        self.assertTrue(
            any("No recommendations were generated" in str(item.value)
                for item in app.info)
        )

    def test_customer_csv_without_prediction_is_retained_and_reported(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path), default_timeout=30).run()
        app.sidebar.radio[0].set_value("Customer Analytics").run()

        app.file_uploader[0].set_value(
            ("customers.csv", b"customer_id,tenure\nC901,8\n", "text/csv")
        ).run()
        self.assertFalse(app.exception)
        self.assertTrue(
            any(
                item.label == "Customer ID" and item.value == "C901"
                for item in app.metric
            )
        )
        self.assertTrue(
            any("No churn probability column was found" in str(item.value)
                for item in app.warning)
        )

        workflow_button = next(
            button
            for button in app.button
            if button.label == "Run customer workflow"
        )
        workflow_button.click().run()
        self.assertFalse(app.exception)
        rendered_markdown = " ".join(
            str(item.value) for item in app.markdown
        )
        self.assertIn("missing_ml_prediction", rendered_markdown)


if __name__ == "__main__":
    unittest.main()
