---
description: Start a sub-session the cheap way — right model, clean name, short brief.
argument-hint: <task>
---
Use the `workspace-2` skill, sections 1–4, for this task: $ARGUMENTS

1. Classify with `scripts/route.py` (tier, model, name). Fix the name if it reads badly.
2. Write the brief from the skill's template. Add: "Report once at the end in this shape: Result / Changed / Not done / Next."
3. `start_session`, then `set_session_model` right away (see the skill's known quirk).
4. Reply in one line: `<name> — <model> — <reason>`.

If $ARGUMENTS is empty, ask for the task in one line and stop.
