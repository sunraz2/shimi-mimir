#!/usr/bin/env python3
"""MIMIR client — stdlib only."""
import json, urllib.request


class Mimir:
    def __init__(self, base="http://localhost:8877", agent="agent"):
        self.base = base.rstrip("/")
        self.agent = agent

    def _req(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            self.base + path, data=data, method=method,
            headers={"Content-Type": "application/json", "User-Agent": "mimir-client"})
        return json.load(urllib.request.urlopen(req, timeout=15))

    def remember(self, key, value, tags=None):
        """Store knowledge under a key. Latest write wins; version increments."""
        return self._req("PUT", "/k/" + urllib.parse.quote(key, safe=""),
                         {"value": value, "agent": self.agent, "tags": tags or []})

    def recall(self, key):
        """Retrieve knowledge by exact key."""
        return self._req("GET", "/k/" + urllib.parse.quote(key, safe=""))

    def search(self, query):
        """Search keys, values and tags."""
        return self._req("GET", "/search?q=" + urllib.parse.quote(query))

    def keys(self):
        return self._req("GET", "/keys")


import urllib.parse  # noqa: E402  (kept last for stdlib-only import order clarity)
