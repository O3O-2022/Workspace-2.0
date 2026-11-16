---
description: Check the hub's own cost — context size, 5-hour usage, sessions to archive.
---
Use the `workspace-2` skill, section 5. Check, using small `limit`s:

- Hub context: if over ~200k tokens → tell the user to run `/compact`.
- `get_usage`: if the 5-hour window is over ~60% → say how many sessions to run at once (2–3).
- Linked sessions done and not resuming → list them as archive candidates.
- Running sessions on a higher tier than their work needs → suggest `/ws-audit`.

Output at most 6 lines: one line per finding, each with the action. If nothing needs doing, say "Hub is light." and stop.
