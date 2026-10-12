import hashlib
import hmac
import secrets
import time
from collections import defaultdict
import bcrypt

SESSION_TTL = 60 * 60 * 24
SESSIONS: dict[str, float] = {}
FAILURES: defaultdict[str, list[float]] = defaultdict(list)

def hash_password(password: str) -> str:
    raw = password.encode("utf-8")
    if len(raw) > 72:
        raise ValueError("password must be at most 72 UTF-8 bytes")
    return "bcrypt$" + bcrypt.hashpw(raw, bcrypt.gensalt()).decode("ascii")

def verify_password(password: str, stored: str) -> bool:
    try:
        if stored.startswith("bcrypt$"):
            raw = password.encode("utf-8")
            return len(raw) <= 72 and bcrypt.checkpw(raw, stored[7:].encode("ascii"))
        if stored.startswith("pbkdf2_sha256$"):
            _, iterations, salt, expected = stored.split("$", 3)
            digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iterations))
            return hmac.compare_digest(digest.hex(), expected)
    except (ValueError, TypeError, UnicodeError):
        return False
    return False

def new_session() -> str:
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = time.time() + SESSION_TTL
    return token

def valid_session(token: str | None) -> bool:
    if not token: return False
    expiry = SESSIONS.get(token, 0)
    if expiry <= time.time():
        SESSIONS.pop(token, None)
        return False
    return True
