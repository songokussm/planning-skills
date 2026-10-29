---
name: create-handoffs
description: Write the task or audit handoff files for a planned batch of app/ changes, in the shape of shared/code-path/TASK_TEMPLATE.md or AUDIT_TEMPLATE.md, and log the batch. Use when planning is done and the user asks for the handoffs.
---

# Create Handoffs

Writes handoff files and one SESSION_LOG line. Does not read project source or file contents, audit, or analyze. No subagents. Uses Codebase Memory only to find file paths for WRITES and lanes.

## When

Once per planning session, after planning ends, covering every planned `app/` change. Not for one or two small doc or config edits (apply those directly when asked). Not while blocking questions remain. Exception: an urgent bug is handed off as soon as the user confirms the fix.

## References

`<root>` is the folder that holds the project folders and `shared/`. In one command, read:

- `<root>/shared/code-path/CODE_PATH.md` (save path, folder layout, reserved names, DECISIONS.md, clock rule)
- `<root>/shared/code-path/TASK_TEMPLATE.md` or `AUDIT_TEMPLATE.md`

The template is the only source for handoff shape, WRITES, lane, and dependency rules. Do not restate it or invent fields. If either file is missing, stop and say which.

## Steps

1. **Timestamp.** Run `date +"%m%d/%H%M"` in the user's local time zone (set `TZ` if the host clock is UTC). Use the output exactly.
2. **Find write paths.** For task handoffs, call Codebase Memory `index_status` for the app's project. If the index is older than the last batch, run `index_repository` and wait until it is ready. For each task, use `search_graph` (and `trace_path` or `get_architecture` when needed) to list the files the task is expected to edit. Never read file contents or code snippets. If Codebase Memory is unavailable, say so and ask the user whether to write the batch without lanes (every task in its own stage).
3. **Assign stages and lanes.** Follow the template rules. Tasks in one stage have disjoint WRITES, at most three lanes per stage. A task that builds on another's result, or shares a write path, goes in a later stage. A dependency-changing task gets its own early stage. A task that needs a live stack mid-batch runs alone in its stage. Name files `<N>.<M>-<name>.md` (single-task stage: `<N>.0`). Refer to other tasks by name, never by number.
4. **Write** each handoff at the CODE_PATH.md save path, in template shape, with its WRITES line. No build, rebuild, restart, or commit steps.
5. **Check paths.** Collect every path in WRITES, CONTEXT, and STEPS (starts with `app/`, `docs/`, or `shared/`, or has a file extension; WRITES paths are relative to Working path). Run one `test -e` over all of them. Replace a missing path with a behavior description, or ask the user. A missing path fails the run.
6. **Log.** Append one line to `<project>/docs/SESSION_LOG.md`, creating the file with this header if needed:

   ```text
   # Session Log
   Handoff batches written since the last end-session. end-session records and clears this file.

   <MMDD HHMM> | handoffs/<MMDD>/<HHMM>/tasks/ | <item IDs or none> | <N> tasks, <S> stages | written
   ```

   Do not edit ITEMS.md, NEXT.md, or ROADMAP.md.
7. **Deliver.** Send every new `.md` with the host's file-delivery tool. Print the stage plan as a short table (stage, lanes, why a task waits). Then, after a blank line, print the run command:

   ```text
   /handoffs <absolute path to handoffs/<MMDD>/<HHMM>/tasks/ as the coding agent sees it>
   ```

   For one audit handoff: `/audit <model> <path to .../audits/<phase>/>`, with `<model>` left literal.

Do not summarize the handoffs beyond the stage plan.
