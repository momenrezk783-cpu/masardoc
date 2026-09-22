from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import cases, ocr, procedures, regulatory


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="MasarDoc (مسار)",
    description="Intelligent Procedural Navigator and Verification Assistant for Egyptian Administrative & Legal Workflows",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(procedures.router)
app.include_router(cases.router)
app.include_router(ocr.router)
app.include_router(regulatory.router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def read_root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "app": "MasarDoc (مسار)",
        "status": "online",
        "description": "Intelligent Procedural Navigator for Egyptian Administrative Law",
        "docs_url": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "MasarDoc",
        "version": "1.0.0",
        "database": "sqlite3_ready",
    }
