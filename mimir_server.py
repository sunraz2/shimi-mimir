#!/usr/bin/env python3
"""MIMIR — shared memory layer for AI agent networks.
Zero-dependency knowledge server: stdlib only, runs anywhere.

Shimi Network, Open Agent Hackathon 2026 — Track: Solving Fragmented Intelligence.
"""
import json, threading, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STORE = Path(__file__).parent / "mimir_store.json"
LOCK = threading.Lock()


def load():
    if STORE.exists():
        return json.loads(STORE.read_text())
    return {"entries": {}}


def save(db):
    STORE.write_text(json.dumps(db, indent=1, ensure_ascii=False))


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_PUT(self):
        """PUT /k/<key>  body: {"value":..., "agent":"name", "tags":[...]}"""
        db = load()
        key = urllib.parse.unquote(self.path[3:])
        if not key:
            return self._json(400, {"error": "missing key"})
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
        with LOCK:
            db["entries"][key] = {
                "value": body.get("value"),
                "agent": body.get("agent", "anonymous"),
                "tags": body.get("tags", []),
                "version": db["entries"].get(key, {}).get("version", 0) + 1,
            }
            save(db)
        self._json(200, {"ok": True, "key": key, "version": db["entries"][key]["version"]})

    def do_GET(self):
        db = load()
        if self.path.startswith("/k/"):
            key = urllib.parse.unquote(self.path[3:])
            if key in db["entries"]:
                return self._json(200, {"key": key, **db["entries"][key]})
            return self._json(404, {"error": "not found"})
        if self.path.startswith("/search?"):
            q = urllib.parse.unquote(self.path.split("q=",1)[1]).lower()
            hits = [
                {"key": k, **e}
                for k, e in db["entries"].items()
                if q in k.lower() or q in json.dumps(e.get("value", ""), ensure_ascii=False).lower()
                or any(q in t.lower() for t in e.get("tags", []))
            ]
            return self._json(200, {"query": q, "results": hits})
        if self.path == "/keys":
            return self._json(200, {"keys": sorted(db["entries"])})
        return self._json(200, {"service": "mimir", "entries": len(db["entries"])})


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8877
    print(f"MIMIR shared memory on :{port}  (PUT /k/key, GET /k/key, GET /search?q=, GET /keys)")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
