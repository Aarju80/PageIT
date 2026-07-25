from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.errors import PageITError, error_payload
from app.fetcher import fetch_page
from app.report_builder import build_report
from app.validators.url import validate_url


router = APIRouter(prefix="/api", tags=["audit"])


class AuditRequest(BaseModel):
    url: str = Field(..., min_length=1)


@router.post("/audit")
def audit_endpoint(payload: AuditRequest) -> dict[str, object]:
    normalized_url = validate_url(payload.url)
    fetch_result = fetch_page(normalized_url)
    return build_report(normalized_url, fetch_result)
