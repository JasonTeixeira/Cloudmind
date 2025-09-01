from typing import Optional, Dict, Any
import time
import random


class SafeHTTPClient:
    """Lightweight HTTP client with timeouts, retries, and jittered backoff.

    Uses httpx if available; falls back to urllib.
    """

    def __init__(self, timeout: float = 5.0, max_retries: int = 3, backoff_base: float = 0.2):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_base = backoff_base

        try:
            import httpx  # type: ignore

            self._httpx = httpx
        except Exception:
            self._httpx = None

    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Any:
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                if self._httpx:
                    with self._httpx.Client(timeout=self.timeout) as client:
                        return client.get(url, headers=headers)
                else:
                    import urllib.request

                    req = urllib.request.Request(url, headers=headers or {})
                    with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec B310
                        class Resp:
                            status_code = resp.status
                            text = resp.read().decode("utf-8", errors="ignore")

                        return Resp()
            except Exception as exc:
                last_exc = exc
                if attempt >= self.max_retries:
                    break
                sleep_s = self.backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                time.sleep(sleep_s)
        if last_exc:
            raise last_exc
        raise RuntimeError("Unknown HTTP error")


