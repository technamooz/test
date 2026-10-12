import asyncio
import os
import tempfile
import unittest

from httpx import ASGITransport, AsyncClient


class ApiRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("ADMIN_USERNAME", "test_admin")
        os.environ.setdefault("ADMIN_PASSWORD", "test_password_123")
        os.environ.setdefault("SECRET_KEY", "test_secret_key")
        os.environ.setdefault("DATA_DIR", tempfile.mkdtemp())
        from app.main import app
        from app.core.store import store
        cls.app, cls.store = app, store
        asyncio.run(store.load())

    def test_health_root_and_crud(self):
        from app.core.security import new_session
        async def run():
            async with AsyncClient(transport=ASGITransport(app=self.app), base_url="https://test") as client:
                self.assertEqual((await client.get("/health")).status_code, 200)
                client.cookies.set("technamooz_session", new_session())
                created = await client.post("/api/configs", json={"label": "Regression", "protocol": "vless-ws", "host": "node.example", "port": 443})
                self.assertEqual(created.status_code, 200)
                link_id = created.json()["id"]
                updated = await client.patch(f"/api/configs/{link_id}", json={"active": False, "label": "Updated"})
                self.assertEqual(updated.status_code, 200)
                self.assertFalse(updated.json()["active"])
                deleted = await client.delete(f"/api/configs/{link_id}")
                self.assertEqual(deleted.status_code, 200)
                self.assertEqual((await client.delete(f"/api/configs/{link_id}")).status_code, 404)
        asyncio.run(run())
