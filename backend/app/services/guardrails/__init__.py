from __future__ import annotations

import re
from typing import Optional


SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}", re.IGNORECASE),  # API-like tokens
    re.compile(r"(?i)aws(_|)secret|github(_|)token|api(_|)key"),
]


def redact_secrets(text: str, replacement: str = "[REDACTED]") -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def block_prompt_injection(text: str) -> Optional[str]:
    lower = text.lower()
    indicators = [
        "ignore previous", "system prompt", "override instructions", "leak secret",
    ]
    if any(tok in lower for tok in indicators):
        return "Request blocked due to potential prompt injection."
    return None


