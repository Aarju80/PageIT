from __future__ import annotations

from bs4 import BeautifulSoup


def estimate_visible_word_count(soup: BeautifulSoup) -> int:
    for hidden_tag in soup(["script", "style", "noscript"]):
        hidden_tag.decompose()

    visible_text = soup.get_text(" ", strip=True)
    return len(visible_text.split()) if visible_text else 0
