from __future__ import annotations

from bs4 import BeautifulSoup


def count_h1_headings(soup: BeautifulSoup) -> int:
    return len(soup.find_all("h1"))
