from __future__ import annotations

from typing import Any


class PageITError(Exception):
    """Base PageIT domain error."""

    def __init__(self, code: str, message: str, status_code: int) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def error_payload(error: Exception) -> dict[str, Any]:
    if isinstance(error, PageITError):
        return {"error": {"code": error.code, "message": error.message}}

    return {"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred while auditing the page."}}
