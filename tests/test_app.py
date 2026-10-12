import asyncio
import os
import tempfile
import unittest

class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['ADMIN_USERNAME']='test_admin'
        os.environ['ADMIN_PASSWORD']='test_password_123'
        os.environ['SECRET_KEY']='test_secret_key'
        os.environ['DATA_DIR']=tempfile.mkdtemp()
        from app.main import app
        from app.core.store import store
        cls.app, cls.store = app, store
        asyncio.run(store.load())

    def test_health_and_auth(self):
        from httpx import ASGITransport, AsyncClient
        async def run():
            async with AsyncClient(transport=ASGITransport(app=self.app),base_url='https://test') as c:
                h=await c.get('/api/health'); self.assertEqual(h.status_code,200)
                bad=await c.post('/api/auth/login',json={'username':'bad','password':'bad'}); self.assertEqual(bad.status_code,401)
                good=await c.post('/api/auth/login',json={'username':'test_admin','password':'test_password_123'}); self.assertEqual(good.status_code,200)
                self.assertEqual((await c.get('/api/auth/me')).json()['authenticated'],True)
        asyncio.run(run())

    def test_config_creation(self):
        from app.core.security import new_session
        from httpx import ASGITransport, AsyncClient
        async def run():
            async with AsyncClient(transport=ASGITransport(app=self.app),base_url='https://test') as c:
                c.cookies.set('technamooz_session',new_session())
                r=await c.post('/api/configs',json={'label':'Test Node','protocol':'vless-ws','host':'example.com','port':443})
                self.assertEqual(r.status_code,200); self.assertTrue(r.json()['uri'].startswith('vless://'))
        asyncio.run(run())
