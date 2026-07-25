import pytest

from app.content_guard import ContentGuardError, validate_content_type


def test_validate_content_type_accepts_html_content_type():
    assert validate_content_type("text/html; charset=utf-8") is True


def test_validate_content_type_rejects_non_html_content():
    with pytest.raises(ContentGuardError):
        validate_content_type("application/json")
