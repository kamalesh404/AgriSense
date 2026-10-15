import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api import routes
from .core.model import get_predictor

app = FastAPI(
    title="AgriSense",
    description="AI-powered crop disease detection and farm management platform for Tamil Nadu farmers",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
_request_counts: dict[str, list[float]] = {}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    if client_ip not in _request_counts:
        _request_counts[client_ip] = []

    _request_counts[client_ip] = [
        t for t in _request_counts[client_ip] if now - t < RATE_LIMIT_WINDOW
    ]

    if len(_request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."},
        )

    _request_counts[client_ip].append(now)
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup_event():
    predictor = get_predictor()
    predictor.load_model()


app.include_router(routes.router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "agrisense"}


@app.get("/api/model-status")
async def model_status() -> dict:
    predictor = get_predictor()
    return {
        "loaded": predictor.is_loaded,
        "classes": predictor.classes,
        "version": "2.0.0",
    }
