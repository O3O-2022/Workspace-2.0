---
description: Write a short handoff note so a new session can continue without re-reading everything.
model: claude-sonnet-5-5
---
Write a handoff note from this conversation, max 10 lines:

```
Goal:
Done:
Not done:
Files touched: <exact paths>
Decisions made: <and why, one line each>
Next step:
Not verified:
```

Facts only, exact paths and commands. Do not start a session. If the user asks for a file, save it as `HANDOFF.md` in the project root.
