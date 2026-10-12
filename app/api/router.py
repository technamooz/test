from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from ..core.config import settings
from ..core.logging import logger
from ..core.rate_limit import login_limiter
from ..core.security import SESSIONS, new_session, valid_session, verify_password, hash_password
from ..core.store import store
from ..services.config_manager import config_manager
from ..services.configs import subscription
from .deps import client_ip, require_auth, require_same_origin
from .schemas import CredentialChange, LinkCreate, LinkPatch, LoginBody

router = APIRouter(prefix="/api")


def _secure_request(request: Request) -> bool:
    if settings.secure_cookies:
        return True
    return request.url.scheme == "https" or request.headers.get("x-forwarded-proto", "").split(",", 1)[0].strip() == "https"


@router.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "version": settings.version}


@router.post("/auth/login", dependencies=[Depends(require_same_origin)])
async def login(body: LoginBody, request: Request):
    ip = client_ip(request)
    if not login_limiter.allowed(ip):
        raise HTTPException(status_code=429, detail="تلاش‌های ورود بیش از حد مجاز است")
    state = await store.snapshot()
    if body.username != state.get("username") or not verify_password(body.password, state.get("password_hash", "")):
        logger.warning("login_failed ip=%s", ip)
        raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور اشتباه است")
    token = new_session()
    response = JSONResponse({"ok": True})
    response.set_cookie("technamooz_session", token, httponly=True, secure=_secure_request(request), samesite="lax", max_age=86400, path="/")
    logger.info("login_success ip=%s", ip)
    return response


@router.post("/auth/logout", dependencies=[Depends(require_same_origin)])
async def logout(request: Request):
    SESSIONS.pop(request.cookies.get("technamooz_session"), None)
    response = JSONResponse({"ok": True})
    response.delete_cookie("technamooz_session", path="/")
    return response


@router.get("/auth/me")
async def me(request: Request):
    return {"authenticated": valid_session(request.cookies.get("technamooz_session")), "username": store.state.get("username")}


@router.post("/auth/change-credentials", dependencies=[Depends(require_auth), Depends(require_same_origin)])
async def change_credentials(body: CredentialChange):
    if not verify_password(body.current_password, store.state.get("password_hash", "")):
        raise HTTPException(status_code=400, detail="رمز عبور فعلی نادرست است")
    store.state["username"] = body.username
    if body.new_password:
        store.state["password_hash"] = hash_password(body.new_password)
    await store.save()
    return {"ok": True, "username": body.username}


@router.get("/dashboard", dependencies=[Depends(require_auth)])
async def dashboard():
    links = await config_manager.list()
    return {
        "links": links,
        "stats": {
            "links": len(links),
            "active": sum(1 for item in links if item.get("active")),
            "traffic": sum(item.get("used_bytes", 0) for item in links),
        },
    }


@router.get("/configs", dependencies=[Depends(require_auth)])
async def list_configs():
    return await config_manager.list()


@router.post("/configs", dependencies=[Depends(require_auth), Depends(require_same_origin)])
async def create_config(body: LinkCreate):
    return await config_manager.create(body.model_dump())


@router.patch("/configs/{link_id}", dependencies=[Depends(require_auth), Depends(require_same_origin)])
async def update_config(link_id: str, body: LinkPatch):
    return await config_manager.update(link_id, body.model_dump(exclude_unset=True))


@router.delete("/configs/{link_id}", dependencies=[Depends(require_auth), Depends(require_same_origin)])
async def delete_config(link_id: str):
    await config_manager.delete(link_id)
    return {"ok": True}


@router.get("/subscription", dependencies=[Depends(require_auth)])
async def get_subscription():
    state = await store.snapshot()
    return {"content": subscription(list(state["links"].values()))}
