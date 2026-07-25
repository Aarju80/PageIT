from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.errors import PageITError, error_payload
from app.routes.audit import router


def allowed_origins() -> list[str]:
    configured = os.getenv("ALLOWED_ORIGINS", "*")
    return [origin.strip() for origin in configured.split(",") if origin.strip()]


app = FastAPI(title="PageIT API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "PageIT API", "status": "ok"}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(PageITError)
async def pageit_error_handler(_: Request, exc: PageITError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=error_payload(exc))


@app.exception_handler(Exception)
async def default_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_payload(exc),
    )
