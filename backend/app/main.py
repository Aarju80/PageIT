from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.errors import PageITError, error_payload
from app.routes.audit import router


app = FastAPI(title="PageIT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

app.include_router(router)


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
