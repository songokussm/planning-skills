# Gap pass

Handles open observation requests and decides whether to write follow-up (Phase 2 or 3) audit handoffs.

1. **Read** every Phase 1 `OBSERVATION_REQUESTS.md` in full. Over about 15 files, delegate with the extraction access block and return each request's table verbatim with slice and model.
2. **Dedupe by content.** Requests naming the same element or route with the same question merge into one, listing every run that raised it. Drop a request that any Phase 1 report already answers with source evidence, and name that report.
3. **Drop unreachable requests.** The coding agent can only read the repo and observe the app's local or dev instance. Drop anything needing a named remote host, SSH, production, long-running production behavior, or credentials not in the working tree. Log each drop (question, source report, reason) in results.md. Handoffs never mention why.
4. **Group by phase:** Phase 2 for functional or live checks (data, API, deploy, tests), Phase 3 for visual checks (layout, contrast). Group further by what needs observing.
5. **Dispatch only what could change the fix.** Write a follow-up audit handoff per group using `<root>/shared/code-path/AUDIT_TEMPLATE.md`, leaving `MODEL:` blank and putting `observation` in the folder name. Record the rest as deferred or parked, with counts. Split any handoff over about 120 lines or 10 steps.
6. **Save** to a new `<project>/handoffs/<MMDD>/<HHMM>/audits/mcp/<N>-<name>.md`, never into the folder you read.
7. **Update results.md** (per-slice and batch) with request dispositions, handoff paths, and any parked phase. Do not replace them with a status-only file.

Continuing a parked phase later: write its handoffs straight from the grouping recorded in results.md, without rereading or re-deduping.

Report: results links, disposition counts, handoff paths with `/audit <model> <path>` lines. Never claim a handoff this run did not write.
