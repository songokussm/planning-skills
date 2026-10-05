---
name: cowork-tools
description: Back up, compare, or restore the user's custom skills (SKILL.md plus bundled files) and record visible MCP servers. Triggers - "backup my tools", "compare tools", "tool drift", "restore tools", "repair my tools".
---

# Cowork Tools

Actions: `backup <path>`, `compare <path>`, `restore <path>`. If `path` is missing, ask and stop.

## What counts as custom

The synced skills cache (`$HOME/.claude/skills/synced/<account-id>/`) holds custom and built-in skills. Its `manifest.json` decides: entries with `source: "plugin"` are custom. Everything else is skipped, and an unknown source is listed in the report. If manifest.json is missing or unreadable, stop. Search only inside `$HOME/.claude`; never run `find` from `/` or across a mounted drive.

Skills installed from a plugin marketplace are restored by reinstalling the plugin, not from this backup.

## Backup file set

Write into `<path>/<YYYYMMDD>/` (today, local time), and nothing else:

| File | Content |
|---|---|
| `<skill>.skill` | That skill's SKILL.md, byte-exact, CRLF stripped, starting with `---` |
| `resources/<skill>/...` | Every other file in the skill folder, same relative paths, no archives |
| `snapshot.json` | Per skill: SKILL.md bytes, resource file count and bytes; skipped built-ins; MCP server names and tool counts; cache root used |
| `mcp-list.md` | MCP server names and tools, as a manual reconnect reference |

## backup

1. Build the whole set in a scratch folder first. Connected folders often block delete, so never write probe or temp files into the target.
2. If a SKILL.md has a duplicated frontmatter block, keep the last one (count `name:` keys, not `---` lines).
3. If a custom skill folder has no SKILL.md, copy it from the newest earlier day folder that has one and record `recovered_from` in snapshot.json. If none exists, report it as not backed up.
4. Copy the set into the day folder in one pass.
5. Verify: `.skill` count equals custom skill count; each `.skill` starts with `---`, closes its frontmatter, and its `name:` matches the filename; each resources tree matches live file count and bytes; snapshot.json parses. Report anything short and stop.

Report:

```text
BACKUP - <path>/<YYYYMMDD> - <YYYYMMDD HHMM>
custom_skill    N  .skill files, verified
skill_resource  N  files in R trees
mcp_server      N  names only
Skipped built-in: N
```

## compare

1. If `path` is a backups root, use its newest day folder. Missing folder or snapshot.json: say so and stop. Any file outside the backup file set is corruption; flag it.
2. Diff each `.skill` against live SKILL.md by content hash, each resources tree by relative path and file hash, and MCP servers by name. A removed MCP server may only mean this session has fewer attached.

```text
COMPARE - live vs <day folder>
Type            Added  Removed  Changed  Unchanged
custom_skill
skill_resource
mcp_server
<one line per removed or changed item>
```

## restore

1. Run compare. Stop if there is no drift or the backup is corrupt.
2. Changed or missing SKILL.md: call `propose_skills` with the `.skill` text verbatim as `skillMd` (kind `improvement` if the skill exists, otherwise `new`), at most 3 per call. Never retype or summarize the text.
3. A skill with bundled files cannot be fully restored from chat; `propose_skills` carries SKILL.md only. Report it as `bundled - reinstall from plugin or upload manually` and send its resources with the host's file-delivery tool.
4. Stale MCP tools: `RefreshMcpTools`. Missing servers: `SuggestConnectors`.

```text
RESTORE - <day folder>
<type> <name> <action> <status: card shown | bundled - manual | repaired | still missing | needs your click>
```

Never call anything "restored" until the user saves the card.
