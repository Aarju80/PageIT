from __future__ import annotations

from bs4 import BeautifulSoup


def extract_meta_description(soup: BeautifulSoup) -> str | None:
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag is None:
        return None

    description = meta_tag.get("content", "").strip()
    return description or None
