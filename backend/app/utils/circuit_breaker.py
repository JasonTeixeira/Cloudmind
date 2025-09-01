import time
import threading
from typing import Callable, Type, Tuple


class CircuitBreaker:
    """Simple in-process circuit breaker.

    - Opens after `failure_threshold` consecutive failures.
    - Stays open for `reset_timeout` seconds, then half-opens to allow a trial call.
    - Success on half-open closes the circuit; failure re-opens.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: float = 30.0,
        handled_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    ) -> None:
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.handled_exceptions = handled_exceptions

        self._lock = threading.Lock()
        self._failures = 0
        self._state = "closed"  # closed | open | half_open
        self._opened_at = 0.0

    def call(self, func: Callable, *args, **kwargs):
        with self._lock:
            now = time.time()
            if self._state == "open":
                if now - self._opened_at >= self.reset_timeout:
                    self._state = "half_open"
                else:
                    raise RuntimeError("Circuit open")

        try:
            result = func(*args, **kwargs)
        except self.handled_exceptions as exc:
            with self._lock:
                self._failures += 1
                if self._failures >= self.failure_threshold:
                    self._state = "open"
                    self._opened_at = time.time()
            raise exc

        with self._lock:
            # Success path
            self._failures = 0
            if self._state in ("open", "half_open"):
                self._state = "closed"
        return result


