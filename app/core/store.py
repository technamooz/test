import asyncio, json, os, secrets
from datetime import datetime, timezone
from pathlib import Path
from .config import settings

class StateStore:
    def __init__(self):
        self.path = settings.data_dir / "technamooz_state.json"
        self.lock = asyncio.Lock()
        self.state = {"schema_version": 2, "username": settings.admin_username, "password_hash": "", "links": {}, "subs": {}, "settings": {}}
    async def load(self):
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                self.state.update(loaded)
            except (OSError, ValueError) as exc:
                raise RuntimeError(f"state file is unreadable: {exc}") from exc
        if not self.state.get("password_hash"):
            from .security import hash_password
            self.state["password_hash"] = hash_password(settings.admin_password)
        if settings.admin_username and not self.state.get("username"):
            self.state["username"] = settings.admin_username
        await self.save()
    async def save(self):
        async with self.lock:
            self.state["schema_version"] = 2
            self.state["saved_at"] = datetime.now(timezone.utc).isoformat()
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")
            with tmp.open("r+", encoding="utf-8") as f:
                f.flush(); os.fsync(f.fileno())
            tmp.chmod(0o600); tmp.replace(self.path); self.path.chmod(0o600)
    async def snapshot(self):
        async with self.lock: return json.loads(json.dumps(self.state))
    async def create_link(self, payload: dict):
        uid = secrets.token_hex(16)
        self.state["links"][uid] = {"id": uid, "label": payload.get("label", "New node"), "protocol": payload.get("protocol", "vless-ws"), "host": payload.get("host", settings.host), "port": int(payload.get("port", 443)), "active": True, "used_bytes": 0, "limit_bytes": int(payload.get("limit_bytes", 0))}
        await self.save(); return self.state["links"][uid]

store = StateStore()
