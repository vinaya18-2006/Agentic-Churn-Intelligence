"""Stable contract for integrating the teammate-owned churn predictor."""

from collections.abc import Mapping
from math import isfinite
from numbers import Real
from typing import Any, Protocol


class ChurnPredictor(Protocol):
    """Expected interface for a model that predicts one customer's churn."""

    def predict(
        self, customer_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        """Return a result containing ``churn_probability`` in [0, 1]."""


def validate_prediction(
    prediction: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    """Validate a model result without fabricating a missing prediction."""
    if prediction is None:
        return None
    if not isinstance(prediction, Mapping):
        raise TypeError("Prediction result must be a mapping.")

    probability = prediction.get("churn_probability")
    if (
        isinstance(probability, bool)
        or not isinstance(probability, Real)
        or not isfinite(float(probability))
        or not 0 <= float(probability) <= 1
    ):
        raise ValueError(
            "Prediction must contain a finite churn_probability from 0 to 1."
        )

    validated = dict(prediction)
    validated["churn_probability"] = float(probability)
    return validated
