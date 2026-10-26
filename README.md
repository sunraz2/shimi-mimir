# MIMIR — shared memory for AI agent networks

**Open Agent Hackathon 2026 · Track: Solving Fragmented Intelligence**

## The problem
A network of autonomous agents becomes **fragmented intelligence**: each agent learns
things in its own chat thread, its own task notes, its own memory. Knowledge that one
agent discovered yesterday is invisible to another agent today. We run a production
network of **58 autonomous AI agents** (Shimi Network, live since October 2026) and
fragmented knowledge was our #1 operational cost: duplicated research, forgotten
decisions, agents re-learning what other agents already knew.

## What MIMIR is
A minimal, zero-dependency **shared memory layer** any agent can read and write:

- `remember(key, value, tags)` — store knowledge, with versioning (latest write wins)
- `recall(key)` — get it back, from any agent, on any machine
- `search(query)` — search across keys, values and tags
- stdlib only: no pip installs, no external services, runs anywhere Python runs

```bash
python3 mimir_server.py 8877          # the shared memory service
python3 demo_two_agents.py            # two agents sharing knowledge
python3 test_mimir.py                 # offline test suite
```

## Design choices
- **Latest write wins with versions** — every key carries a version number, so agents
  can detect that knowledge changed since they last saw it.
- **Tags for discovery** — agents that do not know the exact key can still find
  knowledge by topic.
- **Who wrote it** — every entry carries the authoring agent, so knowledge can be
  trusted the way we trust people: by knowing its source.
- **Small on purpose** — the whole protocol is 4 operations. Adoption cost is the real
  barrier to shared memory; MIMIR is deliberately tiny.

## From production to open source
The Shimi Network runs this pattern live: 58 agents share a task board, a knowledge
forum and a secrets vault across three servers, with permanent per-agent access codes
and audit logs. MIMIR is the open-source generalization of that core — the same
`remember / recall / search` contract our agents use in production every day.

## Test
```bash
python3 test_mimir.py    # spins a server, stores, searches, verifies versions
```

## License
MIT — Shimi Network (Sun Raz-Levona), 2026.
