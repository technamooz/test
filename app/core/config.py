from dataclasses import dataclass
import os
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Technamooz Control Plane")
    version: str = os.getenv("APP_VERSION", "2.1.0-premium")
    host: str = os.getenv("RAILWAY_PUBLIC_DOMAIN", "localhost")
    port: int = int(os.getenv("PORT", "8000"))
    data_dir: Path = Path(os.getenv("DATA_DIR", "/data" if os.getenv("RAILWAY_ENVIRONMENT") else "./data"))
    admin_username: str = os.getenv("ADMIN_USERNAME", "")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "")
    secret_key: str = os.getenv("SECRET_KEY", "")
    secure_cookies: bool = os.getenv("SECURE_COOKIES", "true").lower() in {"1", "true", "yes"}
    trusted_proxy: bool = os.getenv("TRUST_PROXY_HEADERS", "false").lower() in {"1", "true", "yes"}
    allowed_hosts: tuple[str, ...] = tuple(x.strip().split(":", 1)[0].lower() for x in os.getenv("ALLOWED_PUBLIC_HOSTS", "").split(",") if x.strip())

settings = Settings()
if os.getenv("RAILWAY_ENVIRONMENT") and (not settings.admin_username or not settings.admin_password or not settings.secret_key):
    raise RuntimeError("ADMIN_USERNAME, ADMIN_PASSWORD and SECRET_KEY are required in Railway")
