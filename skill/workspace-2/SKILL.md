---
name: workspace-2
description: Workspace 2.0 — run sub-sessions and sub-agents cheaply. Use whenever you are about to start a sub-session (start_session), spawn a sub-agent (Agent tool), hand off a task, or when the user complains about token usage, weekly/5-hour limits, messy session names, or asks to "put each session on the right model". Picks the cheapest model that can do the job, gives the session a clean name, writes a short brief, and keeps the hub from re-reading what it does not need.
---

# Workspace 2.0

Sub-sessions make work faster, but every new session starts on **the same model as its parent**. A hub running on the top model spawns ten workers on the top model, and most of them only upload files, run tests or rename strings. That is where the tokens go.

This skill does five things every time a sub-session or sub-agent is created, and one audit on demand.

## 1. Pick the model by the job, not by the parent

Classify the task first. When unsure, run the helper:

```bash
python scripts/route.py "fix the MLRS truck rolling over on hills and verify in a 20-min match"
# → {"tier": "deep", "model": "<your deep model id>", "name": "[Bug] MLRS truck rolling over on hills", ...}
```

| Tier | Use for | Typical model |
| --- | --- | --- |
| `light` | status questions, side chat, reading a log, listing files, one lookup | Haiku |
| `standard` | mechanical edits, renames, translation passes, running tests or scripts, uploads, form filling, re-shooting with known settings | Sonnet |
| `deep` | debugging with unknown cause, design, creative judgment (picking shots, reviewing visuals), refactors across files | Opus |
| `frontier` | the single hardest problem in flight: multi-system bugs, architecture decisions, anything that failed twice on `deep` | top model (Fable / Mythos class) |

Rules:
- **At most one `frontier` session at a time.** Top models often have their own weekly limit line.
- **Idle sessions go down a tier.** A finished session waiting for a possible follow-up does not need `deep`.
- **Escalate on failure, not on fear.** Start at the lowest tier that plausibly works; move up one tier when the same failure repeats twice.
- Sub-agents (Agent tool): pass `model` explicitly. Read-only searches are `light` or `standard`.

Model ids come from the app's model picker. Put yours in `scripts/models.json` once; `route.py` reads it.

## 2. Switch the model right after starting

`start_session` has no model argument in some hosts. Immediately after it returns, call `set_session_model` with the chosen id.

**Known quirk:** in auto permission mode a hook may rewrite the call (it adds a `session` label) and the classifier then asks you to re-issue it. Re-send the call **once, with exactly the input the error quotes**, and nothing else in that response. If it is refused again, tell the user which session to switch by hand.

You cannot switch your own session. Tell the user to pick the model in the app's model menu.

## 3. Name it so the sidebar reads like a task list

Format: `[Category] verb + object — scope`, under ~45 characters, in the user's language.

| Category | When |
| --- | --- |
| `[Bug]` | something is broken |
| `[Feature]` | new behaviour |
| `[Test]` | measuring, verifying, QA |
| `[Content]` | models, sound, text, images |
| `[Store]` | store page, trailer, release |
| `[Research]` | read-only investigation |
| `[Ops]` | builds, CI, packaging, housekeeping |

Bad: `session-15`, `Fix stuff`, `Continue the previous work about the thing`. Good: `[Bug] Night glow on missiles — sky lighting`.

`route.py` proposes a name; edit it if it reads badly. Rename an existing session with `set_session_title`.

## 4. Brief short, report once

The brief is the only context a fresh session has, and every word is re-read on every turn. Template:

```
Goal: <one sentence>
Already known: <facts that save it a search; nothing it can grep in seconds>
Look at: <2-5 files or docs>
Done when: <a number, a test, a file — something checkable>
Rules: <only the ones it would otherwise break>
Report: once, at the end, 3 lines max, in <language>.
Do not end your turn while waiting on a build or a long run — keep going until done.
```

Never write "read the whole CLAUDE.md" (it is already loaded). Never paste file contents the session can read itself.

**Why "do not end your turn while waiting":** a session that ends its turn to "wait for a notification" is idle; nothing wakes it, and the hub burns tokens nudging it.

## 5. Keep the hub light

The hub's context is re-read on every turn, so the hub is usually the biggest spender.

- Do not relay every child note to the user. Relay only decisions and finished results.
- Do not re-wake finished workers for new work. Give new work to a new, small session.
- Use `get_session` / `list_events` with a small `limit` instead of reading full transcripts.
- When the hub's context passes ~200k tokens, ask the user to run `/compact`.
- Check `get_usage` before fanning out. If the 5-hour window is above ~60%, run two or three sessions, not six.
- Archive sessions that are done and will not be resumed.

## 6. Audit on demand ("put every session on the right model")

1. `list_sessions` with `linked: true`.
2. For each session, read its title and the last few events (`limit` 3-6).
3. Classify with the table above (idle → one tier lower).
4. Show the user a table: session · new model · one-line reason. Then apply with `set_session_model` (see the quirk in step 2).
5. Rename sessions with unclear names (`session-15` → a real task name).

## What this skill does not do

- It does not change permission modes, push code, or publish anything.
- It does not pick a model more expensive than the user's current one without saying so.
- It does not know your exact prices. The tiers are relative; check your plan's pricing page.
