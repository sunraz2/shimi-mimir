#!/usr/bin/env python3
import subprocess, sys, time, json
from mimir_client import Mimir

proc = subprocess.Popen([sys.executable, "mimir_server.py", "8891"])
time.sleep(1.2)
try:
    m = Mimir(base="http://localhost:8891", agent="tester")
    m.remember("t/key", {"v": 1}, tags=["x"])
    assert m.recall("t/key")["value"] == {"v": 1}
    m.remember("t/key", {"v": 2}, tags=["x"])
    assert m.recall("t/key")["version"] == 2, "version should increment"
    assert m.search("x")["results"][0]["key"] == "t/key"
    print("ALL MIMIR TESTS PASSED")
finally:
    proc.terminate()
