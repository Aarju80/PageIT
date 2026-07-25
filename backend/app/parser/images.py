from __future__ import annotations

from bs4 import BeautifulSoup


def count_images_missing_alt(soup: BeautifulSoup) -> tuple[int, int]:
    images = soup.find_all("img")
    missing_alt = 0

    for image in images:
        alt_value = image.get("alt")
        if alt_value is None or alt_value == "":
            missing_alt += 1

    return missing_alt, len(images)
