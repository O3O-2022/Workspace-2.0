---
description: Show tier, model and clean name for one or more tasks. Starts nothing.
argument-hint: <task; another task>
model: claude-haiku-5-5
---
Split on `;`: $ARGUMENTS

Run the `workspace-2` skill's router once with all tasks:
`python <skill dir>/scripts/route.py --table "<task 1>" "<task 2>" …`
(skill dir is usually `~/.claude/skills/workspace-2`).

Print the table only. No commentary.
