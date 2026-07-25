from __future__ import annotations

from urllib.parse import urlparse

from app.errors import PageITError


class PageITValidationError(PageITError):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(code, message, status_code)


def validate_url(raw_url: str | None) -> str:
    cleaned_url = (raw_url or "").strip()

    if not cleaned_url:
        raise PageITValidationError("MISSING_URL", "The URL field is required.", status_code=400)

    parsed = urlparse(cleaned_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise PageITValidationError("INVALID_URL", "Please provide a valid http or https URL.", status_code=400)

    return cleaned_url
