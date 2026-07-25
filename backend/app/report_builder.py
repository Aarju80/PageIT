from __future__ import annotations

from datetime import datetime, timezone

from app.fetcher import FetchResult
from app.parser.parse import parse_html_document


def build_report(url: str, fetch_result: FetchResult) -> dict[str, object]:
    parsed = parse_html_document(fetch_result.html)

    return {
        "url": url,
        "status": fetch_result.status_code,
        "responseTimeMs": fetch_result.response_time_ms,
        "title": parsed["title"],
        "metaDescription": parsed["metaDescription"],
        "h1Count": parsed["h1Count"],
        "imagesMissingAlt": parsed["imagesMissingAlt"],
        "totalImages": parsed["totalImages"],
        "approxWordCount": parsed["approxWordCount"],
        "fetchedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
