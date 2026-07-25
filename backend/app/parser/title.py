from __future__ import annotations

from bs4 import BeautifulSoup


def extract_title(soup: BeautifulSoup) -> str | None:
    title_tag = soup.find("title")
    if title_tag is None:
        return None
    title = title_tag.get_text(strip=True)
    return title or None
