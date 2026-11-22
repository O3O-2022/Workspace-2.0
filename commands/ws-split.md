---
description: Split a long code file by topic — plan first, behaviour unchanged, build + test after.
argument-hint: <file> [topic]
---
File and optional topic: $ARGUMENTS
If no file is given, list the 5 longest source files in the project (lines) and stop.

1. Read the file's outline (declarations, function list, line counts per topic) — not the whole body unless needed.
2. Propose a plan, max 10 lines: `topic → new file`, what stays, how they connect (header / import / public calls only, no shared globals). Same class: topic files (C++: one header + `Class_Topic.cpp`; C#: `partial class`; others: modules). Independent work: a subsystem or component.
3. Wait for a yes.
4. Move code without changing behaviour. Update includes / imports / build files (e.g. CMake, .uproject modules, .csproj) only as needed.
5. Build, then run the same tests as before. If either fails, fix or revert the move — do not leave it broken.
6. Report: `Result / Changed (old file: N → M lines, new files) / Not verified / Next`.
