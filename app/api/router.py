from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ..core.config import settings
from ..core.security import new_session, valid_session, verify_password, SESSIONS
from ..core.store import store
from ..services.configs import make_uri, subscription

router = APIRouter(prefix="/api")
class LoginBody(BaseModel):
    username: str
    password: str
class LinkBody(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    protocol: str = Field(default="vless-ws")
    host: str = Field(default="", max_length=255)
    port: int = Field(default=443, ge=1, le=65535)
    limit_bytes: int = Field(default=0, ge=0)

def require_auth(request: Request):
    if not valid_session(request.cookies.get("technamooz_session")):
        raise HTTPException(401, "Unauthorized")

@router.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "version": settings.version}

@router.post("/auth/login")
async def login(body: LoginBody):
    if body.username != store.state.get("username") or not verify_password(body.password, store.state.get("password_hash", "")):
        raise HTTPException(401, "نام کاربری یا رمز عبور اشتباه است")
    token = new_session(); response = JSONResponse({"ok": True})
    response.set_cookie("technamooz_session", token, httponly=True, secure=settings.secure_cookies, samesite="lax", max_age=86400, path="/")
    return response

@router.post("/auth/logout")
async def logout(request: Request):
    SESSIONS.pop(request.cookies.get("technamooz_session"), None)
    response = JSONResponse({"ok": True}); response.delete_cookie("technamooz_session", path="/"); return response

@router.get("/auth/me")
async def me(request: Request):
    return {"authenticated": valid_session(request.cookies.get("technamooz_session")), "username": store.state.get("username")}

@router.get("/dashboard", dependencies=[Depends(require_auth)])
async def dashboard():
    state = await store.snapshot(); links = list(state["links"].values())
    return {"links": links, "stats": {"links": len(links), "active": sum(1 for x in links if x.get("active")), "traffic": sum(x.get("used_bytes", 0) for x in links)}}

@router.post("/configs", dependencies=[Depends(require_auth)])
async def create_config(body: LinkBody):
    link = await store.create_link(body.model_dump()); return {**link, "uri": make_uri(link)}

@router.get("/configs", dependencies=[Depends(require_auth)])
async def list_configs():
    state = await store.snapshot(); return [{**x, "uri": make_uri(x)} for x in state["links"].values()]

@router.get("/subscription", dependencies=[Depends(require_auth)])
async def get_subscription():
    state = await store.snapshot(); return {"content": subscription(list(state["links"].values()))}
