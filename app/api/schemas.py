from pydantic import BaseModel, ConfigDict, Field, field_validator


class LoginBody(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)


class LinkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1, max_length=80)
    protocol: str = Field(default="vless-ws")
    host: str = Field(default="", max_length=255)
    port: int = Field(default=443, ge=1, le=65535)
    limit_bytes: int = Field(default=0, ge=0)

    @field_validator("protocol")
    @classmethod
    def supported_protocol(cls, value: str) -> str:
        if value not in {"vless-ws", "trojan-ws"}:
            raise ValueError("unsupported protocol")
        return value


class LinkPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str | None = Field(default=None, min_length=1, max_length=80)
    host: str | None = Field(default=None, max_length=255)
    port: int | None = Field(default=None, ge=1, le=65535)
    limit_bytes: int | None = Field(default=None, ge=0)
    active: bool | None = None


class CredentialChange(BaseModel):
    current_password: str = Field(min_length=1, max_length=256)
    username: str = Field(min_length=3, max_length=64)
    new_password: str | None = Field(default=None, min_length=8, max_length=256)
