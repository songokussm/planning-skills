---
name: project-doc-audit
description: Audit one project's docs against its real implementation. Finds stale instructions, duplicated or conflicting authority, and drift, and writes a severity-ranked report. Report only; fixes nothing.
---

# Project Doc Audit

Read-only except for the report file. Access `app/` only as the project instructions allow.

`docs/NEXT.md` and `docs/SESSION_LOG.md` are standard planning files. Do not flag them as unknown, stale, or duplicating ITEMS.md.

## 1. Inventory

Confirm the project root; ask if unclear. Read:

- every file in `docs/`, starting with GUIDE.md and RULES.md
- `CLAUDE.md`, `AGENTS.md`, and `.claude/` files at the project root, if present
- the implementation's structure and names, through the permitted code accessor or a read-only subagent

## 2. Check each doc

- **Authority:** is this doc the only source for its topic? Does another doc state the same rule differently? Does it claim control it cannot have?
- **Currency:** do paths, filenames, config keys, commands, versions, and tool names match what exists?
- **Scope:** does it hold content that belongs elsewhere, or mix audiences?
- **Completeness:** would someone following it hit steps or errors it doesn't cover?

## 3. Classify each finding

- **Severity:** Critical (wrong or unsafe), High (misleading or outdated), Medium (incomplete or misplaced), Low (typo or format).
- **Category:** Authority, Currency, Scope, Completeness, Structure.
- **Source:** the doc line and the file or output that contradicts it. No source, no finding.
- **Fix:** edit, move, delete, or name the single authority.

```text
DOC: docs/RULES.md
HIGH | Currency
Claim: "Deploy with scripts/deploy.sh."
Reality: scripts/ has no deploy.sh; deploy runs from _deploy/compose.yml.
Fix: Point to _deploy/compose.yml.
```

## 4. Report

Write `<project>/audits/<MMDD>/project-doc/FINDINGS.md`:

1. Summary: counts by severity and category, one sentence on overall health.
2. Critical, High, Medium findings, in the format above.
3. Low findings, grouped by type.
4. Docs with no findings.
5. Fixes ranked by impact and effort.

In chat: one line per Critical and High finding, plus Medium and Low counts.

Never edit a doc without the user's approval per finding. Never touch implementation or deploy files.
