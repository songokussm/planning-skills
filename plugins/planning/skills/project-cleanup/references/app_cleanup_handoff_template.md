# App cleanup handoff

Fill the placeholders and change nothing else. The block follows `shared/code-path/TASK_TEMPLATE.md`.

- `<APP>`: the project's uppercase short name used in its `<APP>_AGENT.md` file. Ask if unclear.
- `<app-path>`: absolute path to `<project>/app` as the coding agent sees it.
- `<rules-path>`: absolute path to `shared/CODING_RULES.md` as the coding agent sees it.

```
TITLE: <APP>:app-cleanup

CODING_RULES: <rules-path>

Working path: <app-path>

GOAL: Move everything in this app tree that is not required to run into one archive folder, and keep it out of deploys.

CONTEXT: The app tree has collected scratch files, superseded artifacts, and drift. Nothing is deleted; everything not required moves to one archive folder so the deploy source stays clean and every item stays recoverable.

STEPS:
1. Read the agent file and deploy config
   - Do: Read <APP>_AGENT.md and the deploy config in the working path to learn required structure and current deploy excludes.
   - Verify: both files read.
   - Fallback: if <APP>_AGENT.md is missing, stop and report BLOCKED - NEED DECISION.
2. Inventory
   - Do: Walk the working path, skipping archive/. Record path, type, size, modified time. Classify each as required, candidate, or UNRESOLVED, using the agent file and deploy config. Source, config, data, and documented log folders are never candidates.
   - Verify: one sorted list whose count reconciles with later steps.
   - Fallback: unclear items are UNRESOLVED and stay.
3. Save the inventory
   - Do: Write it to <working-path>/logs/<MMDD>/<HHMM>/app-cleanup-inventory.md using the machine clock.
   - Verify: the file exists.
   - Fallback: create logs/ if missing.
4. Move candidates
   - Do: Move each confirmed candidate to <working-path>/archive/<MMDD>/, keeping relative paths.
   - Verify: each moved item is gone from its origin and present in archive/<MMDD>/; count matches the inventory.
   - Fallback: if a move fails, copy it, keep the original, and note both paths.
5. Exclude archive from deploy
   - Do: Add archive/ to the deploy exclude list.
   - Verify: archive/ is in the exclude list.
   - Fallback: if there is no exclude mechanism, report BLOCKED - NEED DECISION.
6. Update the agent file
   - Do: Update only the references in <APP>_AGENT.md that point to moved paths.
   - Verify: no reference to a moved path remains; the diff shows only those lines.
   - Fallback: if unsure, leave it and flag it in the report.
7. Confirm the tree
   - Do: Diff the working path before and after.
   - Verify: the only differences are the relocated items.
   - Fallback: move back anything moved in error.

DONE WHEN:
- [ ] Inventory exists at <working-path>/logs/<MMDD>/<HHMM>/app-cleanup-inventory.md
- [ ] Every candidate is under archive/<MMDD>/ and gone from its origin
- [ ] Nothing was deleted
- [ ] Deploy config excludes archive/
- [ ] <APP>_AGENT.md has no stale references
- [ ] Before/after diff shows only the relocation
- [ ] Moved count matches the inventory

RISKS:
- Data loss: move, never delete; UNRESOLVED stays.
- Broken deploy: exclude step plus final diff.
- Missed candidates: inventory-to-moved reconciliation.
- Stale agent file: step 6.

NOTES:
- Read the CODING_RULES file first.
- Work only inside the working path.
- Use the machine clock for MMDD/HHMM; do not reuse an earlier value.
- When in doubt, leave the item and mark it UNRESOLVED.
```

## Delivery

After a blank line, print the run command, then send the file with the host's file-delivery tool. Nothing after.

```text
/handoffs <absolute path to <project>/handoffs/<MMDD>/<HHMM>/tasks/ as the coding agent sees it>
```
