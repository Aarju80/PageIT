from __future__ import annotations

from bs4 import BeautifulSoup

from app.parser.headings import count_h1_headings
from app.parser.images import count_images_missing_alt
from app.parser.meta_description import extract_meta_description
from app.parser.title import extract_title
from app.parser.word_count import estimate_visible_word_count


def parse_html_document(html: str) -> dict[str, object]:
    soup = BeautifulSoup(html, "html.parser")
    missing_alt_count, total_images = count_images_missing_alt(soup)

    return {
        "title": extract_title(soup),
        "metaDescription": extract_meta_description(soup),
        "h1Count": count_h1_headings(soup),
        "imagesMissingAlt": missing_alt_count,
        "totalImages": total_images,
        "approxWordCount": estimate_visible_word_count(soup),
    }
