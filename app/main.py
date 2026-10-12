from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from .core.store import store
from .core.config import settings
from .api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await store.load()
    yield

app = FastAPI(title=settings.app_name, version=settings.version, docs_url=None, redoc_url=None, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[], allow_credentials=False, allow_methods=["GET", "POST", "PATCH", "DELETE"], allow_headers=["Content-Type"])
@app.middleware("http")
async def headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
app.include_router(router)
FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
@app.get("/", include_in_schema=False)
async def root(): return FileResponse(FRONTEND / "index.html")
@app.get("/{path:path}", include_in_schema=False)
async def frontend(path: str):
    target = FRONTEND / path
    if target.is_file() and FRONTEND in target.resolve().parents: return FileResponse(target)
    return FileResponse(FRONTEND / "index.html")
