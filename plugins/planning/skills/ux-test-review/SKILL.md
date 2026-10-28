---
name: ux-test-review
description: Review a project's newest UX test run, check whether its evidence can be trusted, explain the result in plain language, and recommend next steps. Use when the user asks to review or act on the latest UX test results.
---

# UX Test Review

Read-only. Never modify `app/`, a run folder, or production data.

## Find the run

Read `<project>/ux-testing/adapter.json`. Its `run_root_parents` names where runs live, and `coverage_catalog` names the catalog. If the adapter is missing, ask for the run folder.

Under each run parent, check `<run>/RUN.json` and `<run>/<app_slug>/<run>/RUN.json`. Keep manifests that parse and have a nonempty `run_id` and a valid `created_at`. Pick the newest by `created_at`, then `run_id`. Ignore folder names and modified times. If none is valid, report the folders searched and why each was rejected, then stop.

## Check the evidence first

Run `python -B <project>/ux-testing/scripts/validate_run_evidence.py validate --run-root <run> --catalog <coverage catalog>`, adding `--expected-model` with the model from the user's original request or saved run prompt. Do not copy `RUN.json`'s `requested_model`, because the validator checks it. If the original model is unknown, omit the flag and say model consistency is unchecked.

| Exit | Meaning |
|---|---|
| 0 | Evidence passed |
| 1 | Evidence invalid |
| 2 | Validator could not finish |

If no validator runs, evidence trust is unknown, never trusted. If it fails, say the pass claims are untrusted before quoting any totals.

## Inspect

Read the smallest set that covers every artifact type: RUN.json, STATE.json, coverage.json; the final report, report.json, coverage summary, unresolved blockers; attempts and checkpoints; evidence manifests, logs, DOM captures, screenshots; findings.jsonl and events.jsonl.

Reconcile counts across state, coverage, attempts, and report. Sample evidence from each distinct case type. Judge each case by its own evidence rule: a PNG is required only when `visual_check` is true; a non-visual pass is proved by an existing test or assertion log path. A missing PNG on a non-visual case is not missing proof. Screenshot reuse is valid only within one packet with a recorded reason, unless the adapter is stricter. Trace every validator finding to its artifact. Keep three things separate: what the report claims, what the evidence proves, what is unknown.

## Explain

Short sentences, plain words. Define a test term the first time it matters. Keep exact counts, failures, and filenames.

Lead with one verdict:

- **Trustworthy:** evidence passed and counts reconcile.
- **Partly trustworthy:** name which results have valid evidence.
- **Untrusted:** evidence failed or proof is missing.
- **Incomplete:** the run stopped before producing results.

Then:

1. **What happened:** plain summary with exact totals.
2. **What we can trust:** evidence-backed results only.
3. **What needs attention:** defects, blockers, contradictions, missing proof.
4. **Next steps:** in priority order, naming the part that changes (application, test runner, fixtures, environment, docs). Evidence-integrity work first, then failed P0, failed P1, then nice-to-haves. Do not blame the app for a test-runner problem.

End with clickable paths to the run folder and its report. If the report is missing, say so.
