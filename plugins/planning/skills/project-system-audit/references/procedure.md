# Procedure

## Vocabularies

| Use | Values |
|---|---|
| Doc vs implementation | aligned, mostly aligned (stale paths or names only), materially drifted (wrong behavior or locations), cannot verify |
| Skill status | active/general, active/specialized, on-demand, overlapping, superseded, apparently unused (search recorded), unable to determine |
| Handoff field | preserve (coding needs it), reference (point to the authority), discover (coding can find it), remove |
| Matrix cell | aligned, partial, conflicting, missing, unverified |
| Finding confidence | confirmed fact, likely issue (name the inference), unresolved question |

An absence claim needs the search that was run, including one broader listing.

## Systems audited

1. Project docs (`<project>/docs/`)
2. Implementation guidance files near the code root
3. Planning skills (installed)
4. Planning skill resources (bundled files)
5. Coding skills (`shared/coding/skills/`)
6. Project instructions (`shared/chat-instructions/`)
7. Planning instructions (same folder)
8. Coding instructions (`AGENTS.md`, `AGENTS.override.md`)
9. Shared docs, templates, routing, and scripts (`shared/`)

The implementation root varies: `app/`, a static site folder, a scripts folder, or none for content work. Discover it.

## Phase 1: Project research (per 2-3 projects)

1. Reconcile the project list with the README Coverage table. Add new projects as `Carded: no`. Pick 2-3 uncarded projects, keeping close dependencies together.
2. One subagent per project fills the project card (template below) from GUIDE.md, RULES.md, a listing of the root, and the specific location claims the docs make. Metadata and listings, not whole source files.
3. One verifier subagent re-checks the most consequential claims on one card. A disputed claim becomes `unverified`.
4. Append cards to `phase-1/PROJECT_MAP.md`, alignment rows to `phase-1/ALIGNMENT.md`, findings to `FINDINGS.md`. Update README.

## Phase 2: System research (once)

One subagent per section, then verifiers.

- **Planning layer:** installed skills, the instruction files, and what loads when. Record behavior that nothing enforces.
- **Skill resources:** per skill, skill to bundled files to shared files to project files.
- **Coding layer:** coding skills, AGENTS files, guidance files, code-index tools, MCP routing, how results return to planning.
- **Shared system:** every shared file, with purpose, consumers, load behavior, authority, and currency.
- **Skill map:** one row per skill with status, trigger, files read and written, tools, dependencies, and output.

Verify five random skill-map rows against the real skill, and every shared component path.

## Phase 3: Analysis (once, then stop)

Precondition: all projects carded, Phase 2 complete.

- **Handoffs:** classify every field (vocabulary above). Trace three contrasting real handoffs through to their results.
- **Authority map:** one home per rule. Flag duplicates, conflicts, cycles, orphans.
- **Load map:** bytes and load trigger per file, totals for six scenarios: planning startup, start-session item work, project work, create-handoffs, coding startup, a coding skill call.
- **Consistency matrix:** processes by layer. Every non-aligned cell cites a finding number.

Close: add a top-of-file synthesis to FINDINGS.md and present drift, duplication, unused parts, and load. **Stop until the user approves.**

## Phase 4: Design (once, then stop)

Write target architecture, recommendations, retirements, and a dependency-ordered sequence of work packages. Each recommendation:

```text
R-<n>: <title>
Problem / Evidence (finding numbers) / Current authority / Proposed authority
Affected files / Dependencies / Benefit / Load impact / Risk / Verification
```

Rules: every recommendation cites a finding; nothing retires before its replacement is verified; no step leaves two live copies; no package depends on a later one. **Stop until the user approves specific packages.**

## Phase 5: Implement (one approved package per run)

1. Open `phase-5/WP-<n>-<name>.md` from the template below.
2. Record a restore point (git commit, or `<file>.bak-<MMDD>`).
3. Change only what the package names; log anything else as a finding.
4. Check every path the changed files name.
5. Exercise dependent workflows and one end-to-end task. Untestable means status `partial`.
6. Search for the moved content to confirm one copy exists.
7. Update docs that describe the change. Retire superseded material by archiving, never deleting.

App files go through create-handoffs.

## Phase 6: Verify (once)

Precondition: every package complete or dropped by the user.

Re-run with commands: path resolution in all instructions and skills, retired paths unreferenced, single copies, routing names real files. Re-check alignment for touched projects, rebuild the matrix, re-measure the six load totals (before, after, difference). Run one real task through the full chain if the user agrees; otherwise list it as unverified. Write `phase-6/VERIFICATION.md` with method, result, and pass/fail per check, then mark the audit complete.

## Templates

README manifest:

```markdown
# Project System Audit - <MMDD>
Status: Phase <n>
Next action: <one line>

| Project | Carded | Alignment | Notes |
|---|---|---|---|

| Phase | Status | Evidence |
|---|---|---|
```

Project card:

```markdown
## <project>
Purpose / Docs root (files, words) / Implementation root and shape
Coding instructions / Guidance files / Project skills / Build and deploy
Project dependencies / Shared dependencies / Handoffs folder
Alignment:
Mismatches: - <claim> | source: <file:line> | actual: <what exists>
Unverified: - <claim> | would need: <check>
```

Finding (append only, never renumber):

```markdown
## F-<MMDD>-<n>: <title>
Confidence / System / Projects / Evidence / What is wrong / Why it matters / Phase
```

Work package:

```markdown
# WP-<n>: <name>
Approved / Recommendation / Restore point / Files changed / Dependent workflows
Verification / End-to-end result / Docs updated / Retired / Copy check / Deviations / Status
```
