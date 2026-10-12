from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from .core.store import store
from .core.config import settings
from .core.logging import configure_logging
from .api.router import router

configure_logging()

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
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'; connect-src 'self'; img-src 'self' data:"
    if request.url.scheme == "https" or request.headers.get("x-forwarded-proto", "").split(",", 1)[0].strip() == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
app.include_router(router)


@app.get("/health", include_in_schema=False)
async def health_alias():
    return {"status": "ok", "app": settings.app_name, "version": settings.version}
FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
@app.get("/", include_in_schema=False)
async def root(): return FileResponse(FRONTEND / "index.html")
@app.get("/{path:path}", include_in_schema=False)
async def frontend(path: str):
    target = FRONTEND / path
    if target.is_file() and FRONTEND in target.resolve().parents: return FileResponse(target)
    return FileResponse(FRONTEND / "index.html")
