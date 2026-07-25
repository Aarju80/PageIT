from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import httpx

from app.content_guard import ContentGuardError, validate_content_type
from app.errors import PageITError


MAX_RESPONSE_BYTES = 1_000_000

# Reuse HTTP connections for better performance
_client = httpx.Client(follow_redirects=True, timeout=2.0)


@dataclass(slots=True)
class FetchResult:
    status_code: int
    response_time_ms: int
    content_type: str | None
    html: str


class FetcherError(PageITError):
    def __init__(self, code: str, message: str, status_code: int) -> None:
        super().__init__(code, message, status_code)


def fetch_page(url: str) -> FetchResult:
    start = perf_counter()

    try:
        response = _client.get(url)
    except httpx.TimeoutException as exc:
        raise FetcherError("TIMEOUT", "The target page did not respond within 2000ms.", 504) from exc
    except httpx.ConnectError as exc:
        raise FetcherError("UNREACHABLE", "The target page could not be reached.", 502) from exc
    except httpx.RequestError as exc:
        raise FetcherError("UNREACHABLE", "The target page could not be reached.", 502) from exc

    response_time_ms = int((perf_counter() - start) * 1000)
    content_type = response.headers.get("content-type")

    try:
        validate_content_type(content_type)
    except ContentGuardError as exc:
        raise exc

    content_length = len(response.content)
    if content_length > MAX_RESPONSE_BYTES:
        raise FetcherError("RESPONSE_TOO_LARGE", "The target page response is too large to audit safely.", 413)

    return FetchResult(
        status_code=response.status_code,
        response_time_ms=response_time_ms,
        content_type=content_type,
        html=response.text,
    )
