from urllib.parse import quote
from ..core.config import settings

def make_uri(link: dict) -> str:
    uid, host, port = link["id"], link.get("host") or settings.host, link.get("port", 443)
    proto, label = link.get("protocol", "vless-ws"), link.get("label", "Technamooz")
    path = f"/ws/{uid}"
    if proto == "trojan-ws":
        return f"trojan://{uid}@{host}:{port}?security=tls&type=ws&host={quote(host)}&path={quote(path, safe='/')}&sni={quote(host)}#{quote(label)}"
    return f"vless://{uid}@{host}:{port}?encryption=none&security=tls&type=ws&host={quote(host)}&path={quote(path, safe='/')}&sni={quote(host)}&fp=chrome#{quote(label)}"

def subscription(links: list[dict]) -> str:
    import base64
    return base64.b64encode("\n".join(make_uri(x) for x in links).encode()).decode()
