from fastapi import HTTPException, Request
from ..core.config import settings
from ..core.security import valid_session


def client_ip(request: Request) -> str:
    if settings.trusted_proxy:
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",", 1)[0].strip()
    return request.client.host if request.client else "unknown"


def require_auth(request: Request) -> str:
    token = request.cookies.get("technamooz_session")
    if not valid_session(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token or ""


def require_same_origin(request: Request) -> None:
    if request.method in {"GET", "HEAD", "OPTIONS"}:
        return
    origin = request.headers.get("origin")
    if not origin:
        return
    host = request.headers.get("host", "").lower()
    if origin.split("://", 1)[-1].lower().rstrip("/") != host:
        raise HTTPException(status_code=403, detail="Cross-origin request blocked")
