from fastapi.testclient import TestClient

from app.content_guard import ContentGuardError
from app.errors import PageITError
from app.main import app


client = TestClient(app)


def test_audit_endpoint_rejects_invalid_url():
    response = client.post("/api/audit", json={"url": "not a real url"})

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "INVALID_URL",
            "message": "Please provide a valid http or https URL.",
        }
    }


def test_audit_endpoint_rejects_missing_url():
    response = client.post("/api/audit", json={})

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "MISSING_URL",
            "message": "The URL field is required.",
        }
    }


def test_audit_endpoint_handles_dns_failure(monkeypatch):
    def fake_fetch_page(_: str):
        raise PageITError("UNREACHABLE", "The target page could not be reached.", 502)

    monkeypatch.setattr("app.routes.audit.fetch_page", fake_fetch_page)

    response = client.post("/api/audit", json={"url": "https://missing.example"})

    assert response.status_code == 502
    assert response.json() == {
        "error": {
            "code": "UNREACHABLE",
            "message": "The target page could not be reached.",
        }
    }


def test_audit_endpoint_handles_timeout(monkeypatch):
    def fake_fetch_page(_: str):
        raise PageITError("TIMEOUT", "The target page did not respond within 2000ms.", 504)

    monkeypatch.setattr("app.routes.audit.fetch_page", fake_fetch_page)

    response = client.post("/api/audit", json={"url": "https://example.com"})

    assert response.status_code == 504
    assert response.json() == {
        "error": {
            "code": "TIMEOUT",
            "message": "The target page did not respond within 2000ms.",
        }
    }


def test_audit_endpoint_handles_non_html_response(monkeypatch):
    def fake_fetch_page(_: str):
        raise ContentGuardError("Only HTML pages can be audited.")

    monkeypatch.setattr("app.routes.audit.fetch_page", fake_fetch_page)

    response = client.post("/api/audit", json={"url": "https://example.com/file.pdf"})

    assert response.status_code == 415
    assert response.json() == {
        "error": {
            "code": "UNSUPPORTED_CONTENT_TYPE",
            "message": "Only HTML pages can be audited.",
        }
    }
