---
name: project-system-audit
description: Multi-session audit of the whole planning-to-coding system across every project in the workspace. Checks docs against implementations, maps skills, instructions, handoffs and load, then designs and applies approved fixes. Use when the user asks for a system-wide audit, not a single-project doc check.
---

# Project System Audit

A six-phase audit that spans many sessions. For one project's docs, use project-doc-audit instead.

`<root>` is the folder holding the project folders and `shared/`. A project is a child of `<root>` that has a `docs/` folder. Recount the projects every run.

Read `references/procedure.md` before any phase work. It holds the phase steps, vocabularies, and report templates.

## Phases

```text
1 Project research (2-3 projects per run) --+
                                             +--> 3 Analysis --> [user approves] --> 4 Design --> [user approves packages] --> 5 Implement (one package per run) --> 6 Verify
2 System research (once) -------------------+
```

Never skip ahead or merge phases. Phase 3 needs every project carded and Phase 2 done. Phases 3 and 4 end at a stop gate.

## Audit folder

One folder per audit: `<root>/shared/audits/<MMDD>/project-system/`, where MMDD is the audit's start date. Only `README.md` (manifest) and `FINDINGS.md` sit at its root; each phase writes in its own `phase-<n>/` subfolder. Reports are cumulative. Never start a second folder for the same audit.

To find the active audit, list `<root>/shared/audits/` newest first and open the `project-system` folder whose README shows an unfinished phase. None found: start Phase 1.

## Choosing the phase

If the user names a phase, run it. Otherwise read the README manifest and report the next phase before starting. If the next step is a stop gate, say so and stop.

## Rules

- Phases 1-3 are read-only outside the audit folder. No fixes before Phase 4, no edits before the user approves a package.
- Never open or edit `app/` from the planning session. App changes go through create-handoffs.
- Every finding cites a file and line, or a command and its output. Otherwise mark it `unverified` and say what would settle it.
- Never create two authoritative copies of anything.
- Delegate research to the cheapest available subagent, one per project or section, spawned together. Re-check subagent claims before reporting them.

## Every run ends by

Updating the README manifest (status and `Next action`) and sending the changed reports with the host's file-delivery tool.
