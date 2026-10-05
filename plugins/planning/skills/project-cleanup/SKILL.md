---
name: project-cleanup
description: Sweep one project and move everything not needed to run into a dated _archive folder, never deleting. Use when the user asks to clean up, tidy, prune, or archive leftover files in a project.
---

# Project Cleanup

One project per run. Move, never delete. The report must be good enough that the user trusts it without rechecking.

## Setup

1. **Project:** the one the user names, otherwise the connected folder. If the session is at the workspace root and no project is named, ask for the name. Do not list all projects as a menu. Confirm it with `test -d`.
2. **app/ check:** `test -d <project>/app` only. Never list, read, grep, or move anything under `app/`, including in a first orientation command. Never run a recursive listing of the whole project.
3. **Clock:** run `date +%m%d/%H%M` once in the user's local time zone and reuse it for every path this run.
4. **Rules:** read `docs/RULES.md` if present. Its project-specific rules override the defaults below.

## Tier 1: docs/

Goal: `docs/` holds only the live core set, with no subfolders. Flatten any subfolder.

| Bucket | Means | Destination |
|---|---|---|
| CORE | GUIDE, RULES, ITEMS, NEXT, SESSION_LOG, ROADMAP, DECISION_LOG, and other live canonical files | stays |
| RESOURCES | Needed later: referenced by an open item, or work in progress | `<project>/resources/` |
| ARCHIVE | Referenced only by closed items, or unreferenced and clearly stale | `<project>/_archive/<MMDD>/docs/` |
| UNRESOLVED | Unclear | leave in place, list in report |

A file referenced by both an open and a closed item is UNRESOLVED. No reference at all is weak evidence; default to UNRESOLVED.

## Tier 2: other project files

Scope: the project root minus `docs/`, `resources/`, `_archive/`, and `app/`. Classify REQUIRED, ARCHIVE, or UNRESOLVED. Both REQUIRED and ARCHIVE need positive evidence. Silence in RULES.md is not evidence.

- Deploy folders (`_deploy` and similar) are always UNRESOLVED.
- Fold old archive-like folders (`archive`, `.backup`, and similar) into `_archive/`.
- ARCHIVE items go to `<project>/_archive/<MMDD>/<original relative path>`.

## Moving files

Use `scripts/cleanup_move.py` for every move, run directly in one command (no subagent):

```bash
python scripts/cleanup_move.py snapshot <project> before.json
python scripts/cleanup_move.py move manifest.json results.json      # manifest: [{"src": ..., "dest": ...}]
python scripts/cleanup_move.py snapshot <project> after.json
python scripts/cleanup_move.py diff before.json after.json results.json diff_report.json
```

`move` copies and keeps the original if a move fails, and adds `-2`, `-3` on name collisions. The `clean` field in `diff_report.json` is the verification.

## Tier 3: app/ (only if it exists)

Do not touch it. Fill in `references/app_cleanup_handoff_template.md` and save it to `<project>/handoffs/<MMDD>/<HHMM>/tasks/1-app-cleanup.md`. If the app's short name is unclear, ask.

## Report

Use counts and paths, not narrative:

- Tier 1 and 2: counts per bucket and where each archive batch landed
- UNRESOLVED: each path with a one-line reason (the part the user acts on)
- Tier 3: handoff path and run command, or "no app/, skipped"

When unsure, choose UNRESOLVED. A wrong UNRESOLVED costs nothing; a wrong ARCHIVE hides a file.
