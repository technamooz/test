"""Managed Xray Core process for the single-container Railway deployment.

Xray listens only on loopback. The public Railway HTTP endpoint remains owned by
FastAPI, which can proxy WebSocket traffic to the internal Xray inbounds.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
import time
from pathlib import Path
from typing import Any

import websockets

logger = logging.getLogger("Technamooz.xray")


class XrayManager:
    def __init__(self) -> None:
        data_dir = Path(os.environ.get("DATA_DIR", "/data"))
        self.enabled = os.environ.get("XRAY_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}
        self.binary = Path(os.environ.get("XRAY_BINARY_PATH", "/usr/local/bin/xray"))
        self.config_path = Path(os.environ.get("XRAY_CONFIG_PATH", str(data_dir / "xray-config.json")))
        self.vless_port = int(os.environ.get("XRAY_VLESS_PORT", "10001"))
        self.trojan_port = int(os.environ.get("XRAY_TROJAN_PORT", "10002"))
        self.process: asyncio.subprocess.Process | None = None
        self.started_at: float | None = None
        self.last_reload: float | None = None
        self.last_error: str | None = None
        self._lock = asyncio.Lock()

    @staticmethod
    def _client(link: dict[str, Any], uid: str) -> dict[str, Any]:
        return {"id": uid, "email": str(link.get("label") or uid)[:64]}

    def build_config(self, links: dict[str, dict[str, Any]]) -> dict[str, Any]:
        vless, trojan = [], []
        for uid, link in links.items():
            if not link.get("active", True) or link.get("expired", False):
                continue
            protocol = link.get("protocol", "vless-ws")
            if protocol == "trojan-ws":
                # Xray's Trojan client password is the UUID used by this panel.
                trojan.append({"password": uid, "email": str(link.get("label") or uid)[:64]})
            elif protocol == "vless-ws":
                vless.append(self._client(link, uid))

        inbounds: list[dict[str, Any]] = []
        if vless:
            inbounds.append({
                "tag": "technamooz-vless-ws", "listen": "127.0.0.1", "port": self.vless_port,
                "protocol": "vless", "settings": {"clients": vless, "decryption": "none"},
                "streamSettings": {"network": "ws", "wsSettings": {"path": "/ws"}},
            })
        if trojan:
            inbounds.append({
                "tag": "technamooz-trojan-ws", "listen": "127.0.0.1", "port": self.trojan_port,
                "protocol": "trojan", "settings": {"clients": trojan},
                "streamSettings": {"network": "ws", "wsSettings": {"path": "/trojan"}},
            })
        return {
            "log": {"loglevel": os.environ.get("XRAY_LOG_LEVEL", "warning")},
            "api": {"tag": "api", "services": ["HandlerService", "StatsService"]},
            "stats": {}, "policy": {"levels": {"0": {"statsUserUplink": True, "statsUserDownlink": True}}, "system": {"statsInboundUplink": True, "statsInboundDownlink": True}},
            "inbounds": inbounds,
            "outbounds": [{"protocol": "freedom", "tag": "direct"}, {"protocol": "blackhole", "tag": "blocked"}],
            "routing": {"rules": [{"type": "field", "inboundTag": ["api"], "outboundTag": "api"}]},
        }

    async def write_config(self, links: dict[str, dict[str, Any]]) -> dict[str, Any]:
        config = self.build_config(links)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.config_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.chmod(0o600)
        tmp.replace(self.config_path)
        return config

    async def validate(self) -> tuple[bool, str]:
        if not self.enabled:
            return False, "disabled"
        if not self.binary.exists():
            return False, f"binary not found: {self.binary}"
        proc = await asyncio.create_subprocess_exec(str(self.binary), "-test", "-config", str(self.config_path), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out, err = await proc.communicate()
        message = (err or out).decode("utf-8", "replace").strip()
        return proc.returncode == 0, message or ("ok" if proc.returncode == 0 else "validation failed")

    async def start(self, links: dict[str, dict[str, Any]]) -> None:
        async with self._lock:
            if not self.enabled:
                self.last_error = "disabled by XRAY_ENABLED"
                return
            await self.write_config(links)
            ok, message = await self.validate()
            if not ok:
                self.last_error = message
                logger.warning("Xray config validation skipped/failed: %s", message)
                return
            if self.process and self.process.returncode is None:
                return
            self.process = await asyncio.create_subprocess_exec(str(self.binary), "run", "-config", str(self.config_path), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, start_new_session=True)
            self.started_at = time.time()
            self.last_reload = self.started_at
            self.last_error = None
            asyncio.create_task(self._drain_logs(self.process))
            logger.info("Xray Core started; vless_port=%s trojan_port=%s", self.vless_port, self.trojan_port)

    async def _drain_logs(self, process: asyncio.subprocess.Process) -> None:
        if not process.stdout:
            return
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            logger.info("[xray] %s", line.decode("utf-8", "replace").rstrip())

    async def reload(self, links: dict[str, dict[str, Any]]) -> None:
        async with self._lock:
            await self.write_config(links)
            if self.process and self.process.returncode is None:
                self.process.send_signal(signal.SIGHUP)
                self.last_reload = time.time()
                return
        await self.start(links)

    async def stop(self) -> None:
        async with self._lock:
            if self.process and self.process.returncode is None:
                self.process.terminate()
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=8)
                except asyncio.TimeoutError:
                    self.process.kill()
                    await self.process.wait()
            self.process = None

    def status(self) -> dict[str, Any]:
        running = bool(self.process and self.process.returncode is None)
        return {"enabled": self.enabled, "running": running, "binary": str(self.binary), "config_path": str(self.config_path), "vless_port": self.vless_port, "trojan_port": self.trojan_port, "uptime_seconds": int(time.time() - self.started_at) if running and self.started_at else 0, "last_reload": self.last_reload, "last_error": self.last_error}

    async def bridge(self, client_ws: Any, protocol: str) -> None:
        """Bridge an accepted FastAPI WebSocket to the loopback Xray inbound."""
        if not (self.process and self.process.returncode is None):
            raise RuntimeError("Xray Core is not running")
        port = self.trojan_port if protocol == "trojan-ws" else self.vless_port
        async with websockets.connect(f"ws://127.0.0.1:{port}/{'trojan' if protocol == 'trojan-ws' else 'ws'}", max_size=None, ping_interval=20) as upstream:
            async def client_to_xray():
                while True:
                    message = await client_ws.receive()
                    if message.get("type") == "websocket.disconnect":
                        break
                    payload = message.get("bytes")
                    if payload is not None:
                        await upstream.send(payload)
                    elif message.get("text") is not None:
                        await upstream.send(message["text"])

            async def xray_to_client():
                async for message in upstream:
                    if isinstance(message, bytes):
                        await client_ws.send_bytes(message)
                    else:
                        await client_ws.send_text(message)

            tasks = [asyncio.create_task(client_to_xray()), asyncio.create_task(xray_to_client())]
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            for task in done:
                if task.exception():
                    raise task.exception()


xray_manager = XrayManager()
