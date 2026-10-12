from fastapi import HTTPException
from ..core.store import store
from .configs import make_uri


class ConfigManager:
    async def list(self) -> list[dict]:
        state = await store.snapshot()
        return [{**item, "uri": make_uri(item)} for item in state["links"].values()]

    async def create(self, payload: dict) -> dict:
        item = await store.create_link(payload)
        return {**item, "uri": make_uri(item)}

    async def update(self, link_id: str, payload: dict) -> dict:
        item = await store.update_link(link_id, payload)
        if item is None:
            raise HTTPException(status_code=404, detail="Config not found")
        return {**item, "uri": make_uri(item)}

    async def delete(self, link_id: str) -> None:
        if not await store.delete_link(link_id):
            raise HTTPException(status_code=404, detail="Config not found")


config_manager = ConfigManager()
