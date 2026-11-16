---
description: Move finished or waiting sessions one model tier down so waking them costs less.
---
Use the `workspace-2` skill, section 1 ("Idle sessions go down a tier").

1. `list_sessions` with `linked: true`. Idle = not running and last event is a finished report or a question already answered.
2. For each idle session: one tier down from its current model (never below light). Skip sessions waiting on the user's answer.
3. Show `session | now | new`, apply with `set_session_model`.
4. Suggest archiving sessions that are done and will not resume. Do not archive without a yes.
