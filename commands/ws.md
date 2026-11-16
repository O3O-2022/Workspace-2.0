---
description: Workspace 2.0 — list all /ws commands.
model: claude-haiku-5-5
---
Print exactly this table and nothing else:

| Command | What it does |
| --- | --- |
| `/ws-spawn <task>` | Start a sub-session the cheap way: right model, clean name, short brief |
| `/ws-route <task; task…>` | Show tier, model and name for tasks (no session started) |
| `/ws-brief <task>` | Write a short brief only |
| `/ws-audit` | Put every linked session on the right model |
| `/ws-name` | Rename linked sessions with unclear names |
| `/ws-idle` | Move finished / waiting sessions one tier down |
| `/ws-lighten` | Check the hub: context size, 5-hour usage, sessions to archive |
| `/ws-handoff` | Write a short handoff note for a new session |
| `/ws-terse [on\|off]` | Short, exact replies for this session |
