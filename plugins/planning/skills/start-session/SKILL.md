---
name: start-session
description: Cold-start briefing for a planning project. Prints the ranked list in docs/NEXT.md, or one item's status when an item ID is named. Read-only.
---

# Start Session

Read-only. One command, no subagents. end-session already ranked the work; this skill prints it.

## Mode

- **Item mode:** the user names an item (`start ITEM-NNN`). Go to Item Mode.
- **Project mode:** anything else.

The project root is the connected folder or working directory.

## Project mode

Run one command that prints `docs/NEXT.md`, a separator, then `docs/SESSION_LOG.md` if it exists. If NEXT.md is missing or empty, add `grep -E '^#{2,3} ' docs/ITEMS.md` to the same command.

Output:

```text
PROJECT: <folder name> - <Status line from NEXT.md>

<NEXT.md entries 1-5, verbatim>

<count and Stale lines from NEXT.md>
Note: SESSION_LOG has <N> batch(es) since the last close - end-session did not run
```

- Print the Note line only if SESSION_LOG.md has lines below its two header lines.
- NEXT.md missing: print `NEXT.md missing - run end-session to rank.` and up to ten item titles.
- No open items: say so in one line.
- No lead-in, summary, or commentary.

## Item Mode

Run `grep -n -A 40 '<ITEM-NNN>' docs/ITEMS.md`. If nothing matches, grep `docs/_archive/*/ITEMS_CLOSED.md`; a match there means the item is closed.

```text
PROJECT: <name> - ITEM-NNN: <title>
STATUS: <open | closed MMDD> - <next action, or "no action remains">
REFERENCES: <files the item names>
```
