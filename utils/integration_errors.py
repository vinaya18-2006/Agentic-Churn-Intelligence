"""Safe, explicit failures raised by optional integration providers."""


class IntegrationError(RuntimeError):
    """An integration failure with a user-safe message."""
