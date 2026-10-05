# results.md

Write one per slice (`audits/<MMDD>/<slice>/results.md`) and one for the batch (`audits/<MMDD>/results.md`). Each overwrites the previous review of its scope.

## Per slice

Eight parts, in order: Header; Ranking; Findings by model; Agreements; Disagreements and resolutions; Merged findings; Observation requests and disposition; Slice recommendation. Note duplicates, interruptions, and contradictions where they occur.

## Batch, eleven sections in order

1. **Header:** reports and models reviewed (runs vs files if they differ), folder path, every slice with its phase (1 source, 2 functional, 3 visual), unresolved observation requests, parked phases, decision in one line.
2. **Ranking:** rank, model, slice, phase, coverage, specificity, recommendations, edge cases, status, notes. Voided reports stay, marked.
3. **Coverage matrix** (multi-slice only): slice by model, DONE / PARTIAL / FAILED / NOT ATTEMPTED.
4. **Disagreements:** the resolution table per contested item. Omit if none.
5. **Merged findings:** one table with columns Finding, Verdict, Agreement (`4 of 5`, `reviewer-derived`, `observation-confirmed`), Impact, Effort, Location. Before writing, reconcile: every extracted finding and sub-item appears here, in section 6, or in section 7.
6. **Closed by this audit:** already fixed or disproven, with agreement counts.
7. **Single-model, uncontested, reviewer-derived, and voided:** each named with the reason it is in or out.
8. **Open decisions:** choices the user must make, and what each gates.
9. **Scoping gaps:** questions the handoff missed, duplicate defects, and observation-request accounting (total requests reconciled to answered, contradicted, unreachable, deferred, parked, dispatched).
10. **Decision:** fix handoff or follow-up audit, why, and what is in and out of scope.
11. **Side effects to clean up:** state the runs left behind (test records, uploads, settings). Omit if none.
