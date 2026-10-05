---
name: audit-review
description: Rank and merge multi-model audit reports already saved in a project audits folder, write results.md, then write a fix handoff or a targeted follow-up audit. Use when the user says an audit is complete or asks to review audit reports. Not for /handoffs task results (.result.md files), code review, or first-time audit handoffs.
---

# Audit Review

Run without asking for clarification. Access `app/` only as the project instructions allow.

## 0. Confirm these are audit reports

Proceed only if `<project>/audits/` exists and its newest `<MMDD>/<name>/` folder holds at least one `<MODEL>/report.md` with finding tables. A `*.result.md` under `handoffs/` is a task result, never an audit report. If the check fails, say no audit reports were found, name the path checked, and stop.

## 1. Locate the batch

Layout: `<project>/audits/<MMDD>/<name>/<MODEL>/report.md`, plus `STATE.md` and, for code audits, `OBSERVATION_REQUESTS.md`. The run folder name is the model.

- Use the newest `<MMDD>`. Take every sibling folder sharing a prefix (for example `code-audit-1-...`, `code-audit-2-...`) as one batch. No siblings means a batch of one.
- Folders containing `observation` are follow-up phases in the same batch.
- If the user names a folder, use it and its prefix siblings instead.
- Older flat folders hold `<model>.md` files and one shared STATE.md. Read those; the filename is the model.
- Skip files without finding tables. STATE.md is evidence, not a report.

## 1a. Pick the mode

| Condition | Mode |
|---|---|
| An `observation` folder has a report | Final pass: steps 1b-5 |
| No `observation` folder, and any OBSERVATION_REQUESTS.md has a `## Request` heading | Gap pass: step 3a only |
| Neither | Final pass |

## 1b. Extract

Final pass only. Do not read reports into the main thread. Delegate extraction per `references/extraction.md`. All comparison and decisions stay with you.

## 2. Judge

**Complete or partial.** Read each report's `STATUS:` (`complete`, `in progress`, or absent, which counts as complete). An empty section under a present heading means that step never ran, whatever STATUS says. Use the run's own STATE.md to confirm which steps ran. Score partial reports on what they finished.

**Duplicates.** Matching CONTENT_HASH is an exact duplicate; near-identical findings are a near duplicate. Keep the earlier one, void the later, and exclude it from every count. Record it as a process defect.

**Rank** each non-void report on coverage, specificity (files, lines, symbols), actionable recommendations, and edge cases. With one report, summarize it without ranking.

**Merge** at the item level, keeping every sub-item:

- In 2+ reports: keep the most specific wording, tag `multi-model`.
- In one report: first search the other reports' locations for the same file or symbol. An opposing claim is a disagreement (below). Otherwise tag `single-model`.
- Others were interrupted before that section: tag `uncontested`, treat as unconfirmed.
- From an observation folder: tag `observation-confirmed`; never count with source findings.
- Count agreement per slice, against the models that ran that slice.
- Order by impact (High, Medium, Low), then effort (Low first). Never truncate.

**Disagreements.** Resolve by method, not votes. Record per report what it examined (element, URL, width, user role) and what it found. Most conflicts are different targets. Escalate only when the same target gives different answers.

**What no report was asked.** Check whether one item serves several roles that a planned change would break, whether the audit answered the question that motivated it, and whether slices conflict (one deletes what another refactors). Tag these `reviewer-derived`, never count them as model agreement, and log the missed question as a scoping gap.

## 3. Decide

Final pass only. Choose a **targeted follow-up audit** if: the top report has blocked or unverified steps, a High single-model or uncontested finding would change the fix, a section is missing from every report, a reviewer-derived finding needs data no report gathered, or voids left too little agreement. Otherwise choose a **fix handoff**.

- A follow-up covers only the unanswered questions.
- If a slice has no complete run, retry only the failed model against its existing run folder (STATE.md resumes it), unless sibling models already answered that slice.
- A choice only the user can make is an open question in results.md, not a reason to audit. Write the fix handoff for everything it does not gate.
- A phase the user parked is not a gap. Carry it forward.

## 3a. Gap pass

Follow `references/gap-pass.md`.

## 4. Write

Final pass only.

- **results.md:** follow `references/results-template.md`.
- **Handoffs:** get the timestamp from `date +"%m%d/%H%M"` in the user's local time zone. Read `<root>/shared/code-path/AUDIT_TEMPLATE.md` (follow-up) or `TASK_TEMPLATE.md` (fix), where `<root>` holds the project folders and `shared/`. Save to `<project>/handoffs/<MMDD>/<HHMM>/<code|mcp>/<N>-<name>.md` and confirm the file exists.
- If both apply, write the follow-up audit first, then the fix handoff for findings it does not gate.
- If this batch follows up an earlier audit, merge that audit's results.md into the fix scope.

## 5. Report

Send results.md and each handoff with the host's file-delivery tool. In chat, print only:

```text
Audit review complete. Building <targeted audit | fix handoff>.<partial or voided report count, if any>
Run: /audit <model> <path to the handoff folder>
```

Add one line only if a reviewer-derived finding drives the decision.
