---
name: end-session
description: Close a planning session. Records what happened in ITEMS.md, ROADMAP.md and DECISION_LOG.md, archives closed work, and writes the ranked NEXT.md that start-session prints.
---

# End Session

Three jobs: record what this session did, keep the planning docs correct, and leave a ranked NEXT.md. The next start-session reads only NEXT.md.

Records only. It does not audit the doc system (sizes, placement, staleness). If you notice a doc problem, say "worth a project-doc-audit run" in one line and move on.

No subagents. Batch reads into one command.

## Write boundary

Write only to `<project>/docs/*.md`, `<project>/docs/_archive/<MMDD>/`, and `<project>/backups/`. Never write another project's files. If something belongs to another project, note it here and let that project's session act on it.

## 1. Identify the project

Use the connected folder, working directory, or paths already in the conversation. Ask if unclear. Record the absolute `project_root`.

## 2. One read

Print, with separators:

- `docs/ITEMS.md`
- `docs/ROADMAP.md`
- `docs/SESSION_LOG.md` if present
- `grep -n -i -A 5 'close\|end-session' docs/RULES.md` (project-specific close rules; follow them)
- line count and first 15 lines of `docs/DECISION_LOG.md` if present

## 3. Gather

From the conversation and SESSION_LOG.md: decisions made, work done, batches handed off, what is still open, what was discussed but not decided. Record only what happened.

## 4. Ownership sweep

Run when this session added or edited an item, or touched another project. Otherwise skip with a one-line note.

Rule: an open item stays in this project's ITEMS.md only if this project must take the next action. For every open item ask: "would another project's own docs already cover this?" If yes, remove it (log a one-time fix as a decision first). If no project covers it, keep it and mark it a bridge item.

Show the user the removed and flagged items, with reasons, before writing. Never drop items silently. Say so if an item has survived this sweep three closes in a row.

## 5. Compose ITEMS.md

- **Handed off:** for each SESSION_LOG batch, add to each covered item `**Handed off:** handoffs/<MMDD>/<HHMM>/tasks/ - <written | run | reviewed>`. Use `run` or `reviewed` only if the conversation shows it.
- **Open items** carry enough to act without asking: description, what was learned, plan, and next action with an owner.
- **Survived:** last line of every open item, `**Survived:** N closes`. Still open since last close: +1. New this session: 0. No number yet: 0. Closed items drop the line.
- If in doubt whether an item closed, keep it open. Relocate information, never delete it.

## 6. Compose decisions and ROADMAP.md

| Decision state | Goes to |
|---|---|
| Settled, DECISION_LOG.md exists | DECISION_LOG.md, newest first |
| Settled, no DECISION_LOG.md | ROADMAP.md decision log section |
| Open | ROADMAP.md decision log section |

When an open decision settles, move it from ROADMAP.md to DECISION_LOG.md. Keep each entry under 80 words and use the project's numbering. Mark finished ROADMAP tasks done and add new ones.

Pruning in the same pass:

- ROADMAP rows or sections marked Done, Cancelled, or Closed move verbatim to `docs/_archive/<MMDD>/ROADMAP_CLOSED.md`.
- DECISION_LOG.md entries beyond the newest 20 move to `backups/DECISION_LOG_ARCHIVE.md`.

Edit `docs/GUIDE.md` only if a decision changed documented behavior. Keep the edit minimal.

## 7. Rank and write NEXT.md

The order is the recommendation. Rank open items with these tests, stopping at the first that separates two items:

1. **Unblocks:** how much other work waits on it.
2. **Decay:** what gets worse if it sits (uncommitted edits, a batch written but not run, unreviewed results).
3. **Residue:** started work beats new work.
4. **Milestone pull:** progress toward a ROADMAP milestone or GUIDE.md purpose.
5. **Size:** smaller first, ties only. Size is the user's time.

Demote: items another project must act on, items waiting on an external event or another item (mention in the blocker's Why now), items waiting on an undecided decision (rank the decision). A batch written but not run usually ranks first as "Run <batch path>".

Replace `docs/NEXT.md` with exactly:

```text
# Next
Updated: <MMDD HHMM>
Status: <one-line project status>

1. <title> [S|M|L] - <what it is, 12 words max> | <ITEM-NNN or batch path>
   - Why now: <8 words max>
2. ...
(up to 8 entries)

<X> more waiting.
<Y> blocked or another project's to act on.
Stale: <IDs> - survived 3+ closes, decide or drop
```

S is under 30 minutes, M is 30 minutes to 2 hours, L is over 2 hours. Omit count or Stale lines that would be zero. If the top three are all S, add `Note: top three are small; largest open item is <title> [L].`

## 8. Write

Before each write, confirm the absolute target path starts with `project_root`. If not, stop and ask.

Order (archive first, so a failed write loses nothing):

1. Create `docs/_archive/<MMDD>/` if needed.
2. Append closed items to `ITEMS_CLOSED.md`, pruned ROADMAP rows to `ROADMAP_CLOSED.md`, pruned decisions to `backups/DECISION_LOG_ARCHIVE.md`.
3. Write ITEMS.md, ROADMAP.md, DECISION_LOG.md, NEXT.md, and GUIDE.md if edited.
4. Reset SESSION_LOG.md to its two header lines.

Verify in one command: each archived item ID is in its archive file, the `**Survived:**` count equals the open item count, and the ITEMS.md size. Fix and rewrite if Survived lines are short. If ITEMS.md is over 10KB, note it as a project-doc-audit candidate.

## 9. Report

Send the changed files with the host's file-delivery tool. Report in at most five lines: items closed, items added, batches recorded, NEXT.md top entry, and any project-doc-audit note.
