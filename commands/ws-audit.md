---
description: Put every linked session on the right model. Shows a table first.
---
Use the `workspace-2` skill, section 6.

1. `list_sessions` with `linked: true`. For each, title + last 3–6 events only.
2. Pick a tier (idle → one lower; at most one frontier).
3. Show: `session | state | now | new | reason` — only rows that change.
4. Apply with `set_session_model`. Report: "<n> changed, <m> unchanged", plus any that failed and why.
