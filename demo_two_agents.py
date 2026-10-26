#!/usr/bin/env python3
"""Demo: two agents on different machines share knowledge through MIMIR.
Run mimir_server.py first, then this script."""
from mimir_client import Mimir

researcher = Mimir(agent="shimi-research")
builder = Mimir(agent="shimi-pituach")

# Agent A learns something and stores it
researcher.remember("market/agent-economy", {
    "source": "Gartner 2026",
    "finding": "AI spending 2.7T$ in 2026; agents market 16.5B -> 29.2B$",
    "verified": True,
}, tags=["market", "agents"])

# Agent B reads what A learned — no chat, no copy-paste, no fragmentation
fact = builder.recall("market/agent-economy")
print("builder learned from researcher:", fact["value"]["finding"], "(v" + str(fact["version"]) + ")")

# Agent B adds what it built
builder.remember("build/landing-verify", {
    "status": "live", "repo": "shimi-landingverify",
    "proven": "caught a missing asset on a published page before users saw it",
}, tags=["build"])

# Any agent can search across all knowledge
hits = researcher.search("landing")
print("researcher finds builder's knowledge:", [h["key"] for h in hits["results"]])
