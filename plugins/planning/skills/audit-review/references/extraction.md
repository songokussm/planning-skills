# Extraction format

At most 8 reports per subagent. Before spawning, confirm every report is assigned exactly once.

Start every worker prompt with this block, verbatim:

> Read each file with the environment's normal file tools, using absolute paths. Do not request folder access. If a file cannot be read, emit `UNREADABLE: <path> - <error>` and continue.

Then ask for exactly this record per report:

```text
MODEL: <run folder name>
SLICE: <slice folder name>
STAGE: <1 for source slices; 2 for any folder containing "observation">
PATH: <absolute path>
LINES: <wc -l>
STATUS: <STATUS: value verbatim, or ABSENT>
SECTIONS:
  - <heading verbatim> | <line count> | FILLED | EMPTY
FINDINGS:
  - Finding N (<block title>): <finding verbatim> | <severity> | <location> | <change class or none>
  - Finding N sub-item <label>: <issue verbatim> | <severity or inherit> | <its own location> | <change class or inherit>
STATE_FILE: <STATE.md verbatim, or ABSENT>
OBSERVATION_COUNT: <count of "## Request" headings in this run's OBSERVATION_REQUESTS.md, else 0>
OBSERVATION_TITLES: <one per line verbatim, or none>
CONTENT_HASH: <md5sum of report>
```

Rules for workers:

- Verbatim only. No paraphrase, judging, ranking, or dedupe.
- EMPTY means a heading with nothing under it.
- **Sub-items:** if a finding block lists several distinct defects at different locations (numbered list, G1/G2 labels, table rows), emit each as a sub-item in addition to the headline. Several citations of one defect stay one line.
- Count observation requests from OBSERVATION_REQUESTS.md even if the report says none.
- Return records only, no narrative.

Verify: headline findings returned equal the finding blocks found. A worker that returns prose, or no sub-items where bundled lists exist, failed; rerun it.
