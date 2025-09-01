"""
Retry and backoff utilities for provider/service calls.
"""

from __future__ import annotations

import asyncio
import random
from typing import Any, Awaitable, Callable, Optional, Type, TypeVar

T = TypeVar("T")


class TransientError(Exception):
    """Raised when a transient error occurs which may succeed on retry."""


async def async_with_retries(
    func: Callable[[], Awaitable[T]],
    *,
    attempts: int = 5,
    base_delay_seconds: float = 0.2,
    max_delay_seconds: float = 3.0,
    jitter_fraction: float = 0.25,
    retry_on: Optional[tuple[Type[BaseException], ...]] = (TransientError,),
) -> T:
    """Execute an async function with exponential backoff and jitter.

    - attempts: total tries including the first
    - base_delay_seconds: initial backoff delay
    - max_delay_seconds: cap on backoff delay
    - jitter_fraction: randomization factor to reduce thundering herd
    - retry_on: exception types to retry on
    """

    attempt = 0
    delay = base_delay_seconds

    while True:
        try:
            return await func()
        except BaseException as exc:  # noqa: BLE001
            attempt += 1
            should_retry = retry_on and isinstance(exc, retry_on)
            if attempt >= attempts or not should_retry:
                raise

            jitter = delay * jitter_fraction
            sleep_for = min(max_delay_seconds, delay + random.uniform(-jitter, jitter))
            await asyncio.sleep(max(0.0, sleep_for))
            delay = min(max_delay_seconds, delay * 2)


def with_retries(
    func: Callable[[], T],
    *,
    attempts: int = 5,
    base_delay_seconds: float = 0.2,
    max_delay_seconds: float = 3.0,
    jitter_fraction: float = 0.25,
    retry_on: Optional[tuple[Type[BaseException], ...]] = (TransientError,),
) -> T:
    """Synchronous version of retry/backoff."""

    attempt = 0
    delay = base_delay_seconds

    while True:
        try:
            return func()
        except BaseException as exc:  # noqa: BLE001
            attempt += 1
            should_retry = retry_on and isinstance(exc, retry_on)
            if attempt >= attempts or not should_retry:
                raise

            jitter = delay * jitter_fraction
            sleep_for = min(max_delay_seconds, delay + random.uniform(-jitter, jitter))
            # Use asyncio if running in an event loop; else time.sleep
            try:
                loop = asyncio.get_running_loop()
                # Schedule a delay without blocking loop callers
                loop.run_until_complete(asyncio.sleep(max(0.0, sleep_for)))  # type: ignore[attr-defined]
            except RuntimeError:
                import time

                time.sleep(max(0.0, sleep_for))
            delay = min(max_delay_seconds, delay * 2)


