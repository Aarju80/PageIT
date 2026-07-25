# PageIT

PageIT is a lightweight website-auditing tool that takes a public URL, fetches the HTML, and returns a concise technical + SEO health report.

The app is designed to be fast, modular, and easy to deploy. It focuses on the core signals that matter most for a quick audit: response status, page title, meta description, H1 count, missing image alt text, and visible word count.

---

## What PageIT does

Given a public URL, PageIT returns:

- HTTP status code
- Response time in milliseconds
- Page title
- Meta description
- H1 count
- Number of images missing `alt` text
- Total image count
- Approximate visible word count

---

## Live Demo

- Frontend: https://page-it.vercel.app/
- Backend API: https://pageit.onrender.com
- Backend health check: https://pageit.onrender.com/health
- GitHub Repository: https://github.com/Aarju80/PageIT

---

## Features

### Website Audit

- URL validation before any request is sent
- Response-time measurement
- Safe HTML fetching
- Redirect-aware requests
- Graceful handling for unreachable or non-HTML pages

### SEO Analysis

- Extract page title from `document.title`
- Extract the meta description from the `description` meta tag
- Count all `h1` tags
- Detect images missing `alt` text
- Estimate visible word count by ignoring script/style/noscript content

### Robust Error Handling

The API is intentionally defensive and never leaks a stack trace to the client.

It handles:

- Missing URL
- Invalid URL
- DNS/connection failure
- Request timeouts
- Unsupported content types
- Oversized responses
- Unexpected server-side exceptions

---

## Project Structure

```text
pageit/
├── backend/
│   ├── app/
│   │   ├── parser/
│   │   ├── routes/
│   │   ├── validators/
│   │   ├── content_guard.py
│   │   ├── errors.py
│   │   ├── fetcher.py
│   │   ├── main.py
│   │   ├── report_builder.py
│   │   └── __init__.py
│   ├── tests/
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── style.css
    ├── script.js
    └── config.js
```

---

## Tech Stack

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- httpx
- BeautifulSoup4

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

### Testing

- pytest

---

## Run Locally

### 1. Backend

```bash
cd backend
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
GET /health
```

Run tests:

```bash
pytest
```

### 2. Frontend

```bash
cd frontend
npx serve .
```

You can also use VS Code Live Server for the static frontend.

If your backend is running on a non-default port, update the API base URL in `frontend/config.js`.

---

## API Contract

### Endpoint

```http
POST /api/audit
```

### Request Body

```json
{
  "url": "https://example.com"
}
```

### Success Response

```json
{
  "url": "https://example.com",
  "status": 200,
  "responseTimeMs": 341,
  "title": "Example Domain",
  "metaDescription": "Example website",
  "h1Count": 1,
  "imagesMissingAlt": 2,
  "totalImages": 5,
  "approxWordCount": 187,
  "fetchedAt": "2026-07-24T10:15:00Z"
}
```

### Error Response

```json
{
  "error": {
    "code": "TIMEOUT",
    "message": "The target page did not respond within 8000ms."
  }
}
```

### Error Codes

| Scenario | Status | Error Code |
|-----------|--------|------------|
| Missing URL | 400 | `MISSING_URL` |
| Invalid URL | 400 | `INVALID_URL` |
| Connection Failed | 502 | `UNREACHABLE` |
| Timeout | 504 | `TIMEOUT` |
| Non-HTML Response | 415 | `UNSUPPORTED_CONTENT_TYPE` |
| Response Too Large | 413 | `RESPONSE_TOO_LARGE` |
| Internal Error | 500 | `INTERNAL_ERROR` |

---

## Design Decisions

### 1. BeautifulSoup instead of a headless browser

The assignment focuses on parsing HTML metadata, not running JavaScript-heavy pages. BeautifulSoup is a better fit because it is lighter, faster, easier to host, and has fewer dependency constraints. That keeps the app simple and deployment-friendly.

### 2. Treat target-site failures as audit results, not as app failures

A page returning `404` or `500` is still a valid audit target. Those status codes are useful findings for the user. PageIT only treats failures as API errors when the application cannot perform the audit itself, such as invalid input, timeout, or content-type mismatch.

### 3. Fail fast before making the network request

The app validates the URL before calling the remote page. This reduces wasted requests, improves feedback speed, and ensures the error contract is consistent and predictable.

---

## Testing

Unit tests cover the core parsing and validation behavior.

### Included Coverage

- Happy path HTML parsing
- Missing metadata fallback
- Malformed or partial HTML input
- URL validation
- Unsupported content-type handling

Run the test suite with:

```bash
pytest
```

---

## Deployment Notes

PageIT is deployed as two separate services:

- Backend API: Render
- Frontend: Vercel

### Backend on Render

Use these Render settings for the FastAPI backend:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Pre-Deploy Command: leave empty
```

The deployed backend URL is:

```text
https://pageit.onrender.com
```

Health check endpoint:

```text
GET https://pageit.onrender.com/health
```

Expected response:

```json
{"status":"ok"}
```

### Frontend on Vercel

Use these Vercel settings for the static frontend:

```text
Root Directory: frontend
Framework Preset: Other
Build Command: leave empty
Output Directory: leave empty
```

The deployed frontend URL is:

```text
https://page-it.vercel.app/
```

The frontend calls the Render backend through `frontend/config.js`:

```js
window.PAGEIT_CONFIG = {
  apiBaseUrl: "https://pageit.onrender.com"
};
```

If the Render backend URL changes, update `frontend/config.js`, commit the change, and redeploy the frontend.

---

## Future Improvements

Possible extensions include:

- Lighthouse performance analysis
- Open Graph tag detection
- Broken-link checking
- SEO scoring
- robots.txt validation
- sitemap.xml detection
- favicon detection
- PDF report export
- audit history
- dark/light theme toggle

---

## AI Usage

AI tools were used to brainstorm the architecture, review the API design, improve error-handling strategy, and refine the documentation. All final implementation decisions and verification were completed by the developer.

---

## Acknowledgements

This project was developed as part of the Digital Heroes Internship Qualification Task for the Software Development role.

---

<div align="center">

### Built for Digital Heroes Training Task

<a href="https://digitalheroesco.com">digitalheroesco.com</a>

Made with using FastAPI, BeautifulSoup, and Vanilla JavaScript.

</div>

