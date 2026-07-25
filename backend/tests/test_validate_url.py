import pytest

from app.validators.url import PageITValidationError, validate_url


def test_validate_url_accepts_valid_http_url():
    normalized = validate_url("https://example.com")
    assert normalized == "https://example.com"


def test_validate_url_rejects_invalid_url():
    with pytest.raises(PageITValidationError):
        validate_url("not a real url")


def test_validate_url_rejects_missing_url():
    with pytest.raises(PageITValidationError) as exc_info:
        validate_url("")

    assert exc_info.value.code == "MISSING_URL"


def test_validate_url_rejects_unsupported_scheme():
    with pytest.raises(PageITValidationError) as exc_info:
        validate_url("ftp://example.com")

    assert exc_info.value.code == "INVALID_URL"
