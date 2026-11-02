
import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

NEXUS_BASE_URL = os.getenv("NEXUS_BASE_URL")
NEXUS_API_KEY = os.getenv("NEXUS_API_KEY")
NEXUS_MODEL = os.getenv("NEXUS_MODEL")


@dataclass(frozen=True)
class NexusConfig:
    base_url: str
    api_key: str = field(repr=False)
    model: str


def get_nexus_config(
    environ: Mapping[str, str] | None = None,
) -> NexusConfig:
    """Read and validate Nexus settings without exposing credential values."""
    values = os.environ if environ is None else environ
    base_url = values.get("NEXUS_BASE_URL", "").strip()
    api_key = values.get("NEXUS_API_KEY", "").strip()
    model = values.get("NEXUS_MODEL", "").strip()

    if not base_url:
        raise ValueError("Nexus Base URL is missing.")
    parsed_url = urlparse(base_url)
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        raise ValueError("Nexus Base URL must be a valid HTTPS URL.")
    if not api_key:
        raise ValueError("Nexus API Key is missing.")
    if not model:
        raise ValueError("Nexus Model ID is missing.")

    return NexusConfig(base_url=base_url.rstrip("/"), api_key=api_key, model=model)


def validate_config() -> bool:
    get_nexus_config()
    return True
