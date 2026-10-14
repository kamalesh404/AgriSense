from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import routes

app = FastAPI(
    title="AgriSense",
    description="AI-powered crop disease detection and farm management",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "agrisense"}
