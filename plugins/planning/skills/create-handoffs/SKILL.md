---
name: create-handoffs
description: Write the task or audit handoff files for a planned batch of code-repo changes, in the shape of shared/code-path/TASK_TEMPLATE.md or AUDIT_TEMPLATE.md, and log the batch. Use when planning is done and the user asks for the handoffs.
---

# Create Handoffs

Writes handoff files and one SESSION_LOG line. Does not read project source or file contents, audit, or analyze. No subagents. Uses Codebase Memory only to find file paths for WRITES and lanes.

## When

Once per planning session, after planning ends, covering every planned code-repo change. A project's code repo is in WSL at `~/code/<project>`; the old `<project>/app/` folders are archived and must never appear in a handoff. Not for one or two small doc or config edits (apply those directly when asked). Not while blocking questions remain. Exception: an urgent bug is handed off as soon as the user confirms the fix.

## References

`<root>` is the folder that holds the project folders and `shared/`. In one command, read:

- `<root>/shared/code-path/CODE_PATH.md` (save path, folder layout, reserved names, DECISIONS.md, clock rule)
- `<root>/shared/code-path/TASK_TEMPLATE.md` or `AUDIT_TEMPLATE.md`

The template is the only source for handoff shape, WRITES, lane, and dependency rules. Do not restate it or invent fields. If either file is missing, stop and say which.

## Steps

1. **Timestamp.** Run `date +"%m%d/%H%M"` in the user's local time zone (set `TZ` if the host clock is UTC). Use the output exactly.
2. **Find write paths.** For task handoffs, call Codebase Memory `index_status` for the app's project (`<project>-app`, root `~/code/<project>`). If the index is older than the last batch, run `index_repository` and wait until it is ready. For each task, use `search_graph` (and `trace_path` or `get_architecture` when needed) to list the files the task is expected to edit. Codebase Memory does not index files without functions, such as stylesheets, templates, and static assets. For a UI task, also run a file-name search (for example `find` on `*.css`, `*.html`, and template folders) for the stylesheet and template files behind the target screen, and add them to WRITES. Never read file contents or code snippets. If Codebase Memory is unavailable, say so and ask the user whether to write the batch without lanes (every task in its own stage).
3. **Assign stages and lanes.** Follow the template rules. Tasks in one stage have disjoint WRITES, at most three lanes per stage. A task that builds on another's result, or shares a write path, goes in a later stage. A dependency-changing task gets its own early stage. A task that needs a live stack mid-batch runs alone in its stage. Name files `<N>.<M>-<name>.md` (single-task stage: `<N>.0`). Refer to other tasks by name, never by number.
4. **Write** each handoff at the CODE_PATH.md save path, in template shape, with its WRITES line. For audit handoffs, tag every investigation step `Evidence: code` or `Evidence: ui`, split any step that needs both, and add `App URL:` when any step is `ui`. No build, rebuild, restart, or commit steps.
5. **Check paths.** Collect every path in WRITES, CONTEXT, and STEPS (starts with `docs/` or `shared/`, sits in the code repo, or has a file extension; WRITES paths are relative to Working path, which is `~/code/<project>/` in WSL). Run one existence check over all of them. Code-repo paths live in WSL: from a Windows or Cowork device shell, check them with `wsl test -e ~/code/<project>/<path>`; a plain `test -e` on D: will wrongly report them missing. Replace a missing path with a behavior description, or ask the user. A missing path fails the run.
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

   The handoff path is the `/mnt/d/github/<project>/handoffs/...` form (coding agents run in WSL).

8. **Launch.** Only when the user says to run the batch: ask which pair to use (cursor, openai, claude, anthropic; see "Launching work in T3" in `shared/chat-instructions/cowork.md`), with cursor as the first option. "Go" without a pair means cursor. Then start one T3 thread in the target project (`~/code/<project>`) through the `t3` MCP, with that pair's parent model and the run command as its first message. Report the thread ID and model. If the `t3` MCP is not connected, give the user the run line to paste into a new T3 thread instead.

   For one audit handoff: `/audit <model> <path to .../audits/<phase>/>`, with `<model>` left literal. `/audit` runs code steps and calls `/ui-audit` for any `Evidence: ui` steps. For a handoff whose steps are all `ui`, print `/ui-audit <model> <path>` instead.

Do not summarize the handoffs beyond the stage plan.
