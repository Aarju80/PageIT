from __future__ import annotations

from app.errors import PageITError


class ContentGuardError(PageITError):
    def __init__(self, message: str, status_code: int = 415) -> None:
        super().__init__("UNSUPPORTED_CONTENT_TYPE", message, status_code)


def validate_content_type(content_type: str | None) -> bool:
    if not content_type:
        raise ContentGuardError("The target page did not return a valid content type.")

    normalized = content_type.lower()
    if "html" in normalized:
        return True

    raise ContentGuardError("Only HTML pages can be audited.")
