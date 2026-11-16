---
description: Write a short sub-session brief only (goal, known, files, done, one report).
argument-hint: <task>
model: claude-sonnet-5-5
---
Use the `workspace-2` skill, section 4. Write a brief for: $ARGUMENTS

Max 9 lines, template order. Only facts from this conversation or that you can check in seconds; mark guesses as guesses. End with:
"Report once at the end: Result / Changed / Not done / Next."
"Do not end your turn while waiting on a build or long run — keep going until done."

Output the brief in a code block, nothing else.
