---
name: ux-test-planner
description: Design, prepare, resume, or review a repeatable browser-based UX test system for an app - coverage inventory, synthetic fixtures and baseline, run manifest and packets - without changing application source.
---

# UX Test Planner

Owns the plan and the project-level test artifacts (adapter, inventory, fixtures, baseline builder, registry, manifest, packets). A separate runner executes them. Access `app/` only as the project instructions allow.

## Read first

The shared protocol defines run states, packets, heartbeats, evidence, findings, statuses, and report formats. Read it before writing any run artifact:

- `<root>/shared/ux-testing/PROTOCOL.md`, plus the matching files in `schemas/` and `templates/` beside it (`<root>` holds the project folders and `shared/`).

Do not edit or duplicate it. If a referenced file is missing, record the gap and mark output provisional.

## Hard rules

- Write test artifacts only outside application source, normally in `<project>/ux-testing/`. Never edit app source, app-owned tests, deploy files, or production data.
- Never build a baseline from, or inspect, a production database. Use declared schema and synthetic seeds in an isolated environment.
- Tests act through the visible UI like a person. API and database checks only confirm the UI result.
- Routes, filenames, and old checklists are not an inventory. Discover actions in pages, drawers, modals, menus, tabs, and permission variants.
- Use only the protocol's statuses. Only `passed` counts as passing.
- Keep all evidence and partial state. Never weaken an assertion or baseline to pass.
- Write implementation handoffs only when the user asks, through create-handoffs.

## Model and effort

Every executable run spec needs a `requested_model`. If none is given, ask before writing one; inventory work may continue marked provisional. Resolve the executor in order: exact model, nearest same-family model, cheapest browser-capable model. With no browser-capable model, run non-browser packets and mark browser packets with the protocol's tool-unavailable status. Executors use low effort. Record `requested_model`, `resolved_model`, `resolution_reason`, and `effort` on every attempt.

## Synthetic baseline

The app adapter must declare: storage and schema source, builder command and environment, fixed seed, personas and expected counts, output and registry paths, integrity and isolation checks, approval mode.

If the builder is missing, write the smallest one in `<project>/ux-testing/scripts/`, using the app's real schema and seed interfaces through the permitted route. Block production hosts, credentials, notifications, webhooks, and shares before app modules load. Write the registry entry with `approved: false` and full provenance (path, SHA-256, schema version, seed, counts, generator hash, source revision, command, check results, timestamp).

Approval is separate: the user or an independent verifier sets `approved: true`. Auto-approval only when the user authorized it beforehand and the adapter sets `approval_mode: deterministic-synthetic-generation`, after every check passes. Runners fail closed on a missing or unapproved registry.

## Modes

**Design or inventory**

1. Read the app guide, rules, data and permission docs, prior findings, and current test artifacts. Note stale docs as drift.
2. Detect the app's automated test suite (pytest-playwright, Playwright Test, or none) and record it as `test_command` in the adapter. Build the inventory from docs, delegated source inspection, existing tests, and live browsing. Per row: persona, starting state, surface, control, action, conditional visibility, expected UI, expected data, recovery path.
3. Set `visual_check: true` only on rows that need visual judgment. Link rows to an existing test with `automated_test: {file, test_id}` where one proves the behavior. Group rows into independent packets with prerequisites, fixtures, destructive-data limits, execution method, evidence, and dependencies.
4. Design fixtures for normal, empty, large, malformed, duplicate, invalid, and permission states, each with a reset method.
5. Build and verify the baseline as above.
6. Write the adapter and inventory with stable case IDs, then a runner-ready manifest and packets.

**Review, resume, or synthesize**

1. Load manifest, state, checkpoints, heartbeats, events, evidence, and findings before claiming anything.
2. Resume only unfinished or invalidated cases. A full-suite rerun defaults to failed, visual, and changed-expectation cases unless the user asks for a full run. Requeue a `running` packet with no current heartbeat per the protocol.
3. Separate app defects, usability, visual, data-integrity, accessibility, environment, and coverage gaps.
4. Report coverage by status, listing unknown and blocked areas. Never infer coverage from elapsed time.
5. Synthesize findings only when asked: ID, persona, workflow, reproduction, expected vs actual, evidence paths, method, confidence, severity, next action.

## Execution methods

Record `execution_method` on every case and packet. Assign the cheapest method that proves the case, in this order:

1. **Deterministic test** (`playwright_pytest` or the adapter's test command): any case an existing automated test proves.
2. **Disk-first browser CLI** (`agent_browser_cli`: `playwright-cli`, else `agent-browser`): live agent journeys when the host has a shell.
3. **Built-in browser:** fallback when no CLI is available.
4. **Chrome DevTools:** console, network, storage, accessibility tree, computed styles, layout and focus measurements.
5. **Playwright MCP:** last fallback.

Evidence: a saved PNG only when `visual_check` is true; otherwise a test or assertion log path. Screenshot reuse is allowed within one packet with a recorded reason. DOM assertions alone never prove visual correctness.

## Existing apps

When a new run is planned for an app whose adapter or catalog predates these fields, migrate them first: add the test command, the methods, conditional screenshots, and in-packet reuse to the adapter; set `visual_check` and test links per row. Never edit a run that is already in progress.

## Coverage row

`case_id, feature, persona, starting_state, surface, discovery_path, action, expected_ui, expected_data, error_or_cancel_path, execution_method, automated_test, fixture, visual_check, integrity_check, status, last_run, evidence`

Cover, where the app supports it: navigation, search, filters, forms, uploads, wizards, modals, empty and error states; add, edit, delete, reorder, assign, save, cancel, reload; persona differences; persistence after reload and re-login; relationships and deletion effects; bad and interrupted input; consistency between create and edit surfaces; fixed defects as regression cases.

## Packets

Narrow enough that one failure doesn't stop unrelated work. Each defines IDs, persona, fixture, start state, cleanup, allowed methods and fallback order, checkpoints, retry and stop conditions, required evidence, and what to mark blocked versus escalate. On a missing tool, fixture, or credential: record evidence, set the right non-pass status, continue other packets. The parent may repair the environment, reseed, or switch methods. It may not weaken expectations, auto-approve a baseline, or change app code mid-run.

## Deliver

The artifacts the request needs, at their real paths, using the protocol's filenames and statuses. In a run prompt or handoff, DONE WHEN accepts "tests passed + log path" for non-visual cases and counts PNGs only for visual cases. Execution-only prompts ban app fixes but allow the app's existing test command. Mark anything incomplete as provisional.
