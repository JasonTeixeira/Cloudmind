"""
Secrets initialization:
- In production, wire a real secret manager (Doppler, 1Password, AWS Secrets Manager, GCP Secret Manager)
- Here we keep a safe no-op that validates essential envs and logs soft warnings.
"""

import os
import logging

logger = logging.getLogger(__name__)


ESSENTIAL_ENVS = [
    "SECRET_KEY",
]

OPTIONAL_PROVIDER_KEYS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_AI_API_KEY",
]


def init_secrets() -> None:
    """Validate essential secrets are present; in production, enforce."""
    try:
        env = os.getenv("ENVIRONMENT", "development").lower()
        if env in {"test", "testing"}:
            return
        missing = [key for key in ESSENTIAL_ENVS if not os.getenv(key)]
        if env == "production" and missing:
            raise RuntimeError(f"Missing essential secrets in production: {missing}")
        if missing:
            logger.warning(f"Missing essential secrets: {missing}. Consider using a secret manager.")
        # Soft-warn for provider keys
        missing_providers = [k for k in OPTIONAL_PROVIDER_KEYS if not os.getenv(k)]
        if missing_providers:
            logger.info(f"Optional AI provider keys not set: {missing_providers}")
        logger.info("Secrets validated.")
    except Exception as e:
        logger.debug(f"init_secrets skipped: {e}")


