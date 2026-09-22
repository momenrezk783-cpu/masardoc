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

# app/main.py may be used as the deployment entry point. The frontend lives
# in the repository-level static directory, one level above this file.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def read_root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_path):
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
