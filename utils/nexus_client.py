"""Nexus API placeholder; no request is sent until its contract is verified."""

from collections.abc import Mapping
from typing import Any, Protocol

from utils.integration_errors import IntegrationError


class RecommendationGenerator(Protocol):
    """Expected interface for a verified retention recommendation provider."""

    def __call__(
        self, retention_context: Mapping[str, Any]
    ) -> list[dict[str, Any]]:
        """Return evidence-cited recommendation candidates."""


class NexusIntegrationUnavailable(IntegrationError):
    """Raised when an unverified Nexus request cannot safely be made."""


class NexusClient:
    """Explicit placeholder that avoids guessing Nexus endpoints or payloads."""

    def generate_recommendations(
        self, retention_context: Mapping[str, Any]
    ) -> list[dict[str, Any]]:
        del retention_context
        raise NexusIntegrationUnavailable(
            "Nexus generation is not configured: verified API documentation, "
            "authentication and request format, endpoint, and model ID are "
            "required before a request can be implemented."
        )
