---
description: Rename linked sessions with unclear names to "[Category] verb + object".
---
Use the `workspace-2` skill, section 3.

1. `list_sessions` with `linked: true`.
2. Unclear = `session-N`, `fork-N`, `Untitled`, `new session`, vague verbs ("fix stuff", "continue…"), or over 45 characters.
3. For each, read the last 3 events, propose `[Category] verb + object — scope` in the user's language.
4. Show `old → new`, then apply with `set_session_title`. Leave clear names alone.
