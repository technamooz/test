import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path

from xray_manager import XrayManager


class XrayManagerTests(unittest.TestCase):
    def test_build_config_contains_active_vless_and_trojan_clients(self):
        manager = XrayManager()
        links = {
            "11111111-1111-1111-1111-111111111111": {"active": True, "protocol": "vless-ws", "label": "vless"},
            "22222222-2222-2222-2222-222222222222": {"active": True, "protocol": "trojan-ws", "label": "trojan"},
            "33333333-3333-3333-3333-333333333333": {"active": False, "protocol": "vless-ws", "label": "disabled"},
        }
        config = manager.build_config(links)
        self.assertEqual(len(config["inbounds"]), 2)
        vless = next(x for x in config["inbounds"] if x["protocol"] == "vless")
        trojan = next(x for x in config["inbounds"] if x["protocol"] == "trojan")
        self.assertEqual(vless["settings"]["clients"][0]["id"], "11111111-1111-1111-1111-111111111111")
        self.assertEqual(trojan["settings"]["clients"][0]["password"], "22222222-2222-2222-2222-222222222222")

    def test_write_config_is_valid_json_and_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = XrayManager()
            manager.config_path = Path(tmp) / "xray.json"
            asyncio.run(manager.write_config({}))
            loaded = json.loads(manager.config_path.read_text())
            self.assertIn("inbounds", loaded)
            self.assertEqual(manager.config_path.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
