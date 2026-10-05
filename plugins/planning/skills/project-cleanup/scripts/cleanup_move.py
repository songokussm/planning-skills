#!/usr/bin/env python3
"""
cleanup_move.py - deterministic primitives for the project-cleanup skill.

Why this exists: the skill's whole safety story is "move-not-delete, then
prove nothing else changed." Freehand mv/cp commands from a model are the
one place that story can quietly break (a typo'd path, a partial move, a
silently skipped directory). This script makes the three risky operations
scriptable and independently checkable instead of improvised per run:

  snapshot  - record every path/type/size/mtime under a root, before or after
  move      - move a list of src->dest pairs, move-not-delete, one manifest
              entry per item, always logging what actually happened
  diff      - compare a before/after snapshot pair and report exactly what
              changed, so "only the manifest's items moved" is a fact you
              can check, not a claim

No step in this skill should hand-run `mv`/`shutil.move` directly - always
go through `move`, so every relocation leaves the same evidence trail.

Usage:
  python cleanup_move.py snapshot <root> <out.json>
  python cleanup_move.py move <manifest.json> <results_out.json>
  python cleanup_move.py diff <before.json> <after.json> <results.json> <report_out.json>

manifest.json format (input to `move`):
  [
    {"src": "/abs/path/to/item", "dest": "/abs/path/to/archive/2026/0817/item"}
  ]

`diff`'s third argument is the results.json that `move` just produced, NOT
the original manifest - it needs the actual outcome (a dest may have been
auto-renamed on collision, or the item copied instead of moved) to know
what changed on purpose versus what changed unexpectedly. Always run
snapshot -> move -> snapshot -> diff in that order, in the same shell
session, so the results.json from this run's move is what feeds this run's
diff.
"""

import json
import os
import shutil
import sys


def _walk_snapshot(root):
    root = os.path.abspath(root)
    entries = []
    if not os.path.isdir(root):
        return entries
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                st = os.lstat(full)
                entries.append({
                    "path": rel.replace("\\", "/"),
                    "type": "dir" if os.path.isdir(full) and not os.path.islink(full) else "file",
                    "size": st.st_size,
                    "mtime": st.st_mtime,
                })
            except OSError as e:
                entries.append({"path": rel.replace("\\", "/"), "type": "error", "error": str(e)})
    return entries


def cmd_snapshot(root, out_path):
    entries = _walk_snapshot(root)
    with open(out_path, "w") as f:
        json.dump({"root": os.path.abspath(root), "entries": entries}, f, indent=2)
    print(f"snapshot: {len(entries)} entries -> {out_path}")


def _unique_dest(dest):
    """If dest exists, append -2, -3, ... before the extension until free.
    A destination collision is just two archived items wanting the same
    name - not a reason to leave the source stuck in place forever, and
    not ambiguous enough to need a human decision. Keep the original name
    as the base so provenance stays legible; only the suffix changes."""
    if not os.path.exists(dest):
        return dest
    base, ext = os.path.splitext(dest)
    n = 2
    while True:
        candidate = f"{base}-{n}{ext}"
        if not os.path.exists(candidate):
            return candidate
        n += 1


def _move_one(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    original_dest = dest
    dest = _unique_dest(dest)
    renamed = dest != original_dest
    try:
        shutil.move(src, dest)
        status = "moved_renamed_on_collision" if renamed else "moved"
        return {"src": src, "dest": dest, "status": status}
    except OSError as e:
        # Fallback: copy, leave original in place (never delete on failure).
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
            return {"src": src, "dest": dest, "status": "copied_original_retained", "error": str(e)}
        except OSError as e2:
            return {"src": src, "dest": dest, "status": "failed", "error": str(e2)}


def cmd_move(manifest_path, out_path):
    with open(manifest_path) as f:
        manifest = json.load(f)
    results = [_move_one(item["src"], item["dest"]) for item in manifest]
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"move: {len(results)} items -> {out_path} | {counts}")


def cmd_diff(before_path, after_path, results_path, out_path):
    # Reconciles against move's ACTUAL results, not the original manifest
    # intent - a collision auto-rename or a copy-fallback both mean the
    # real dest (or whether src was even removed) can differ from what the
    # manifest asked for. Diffing against intent instead of outcome would
    # make every rename or fallback look like an unexplained change.
    #
    # Compare files only. Directories are structural byproduct of a move
    # (an emptied source folder disappearing, a new archive/ or resources/
    # folder appearing) - counting them as "unexpected" would bury the one
    # signal this check exists to catch (a FILE that moved or vanished
    # outside the manifest) under expected noise every single run.
    with open(before_path) as f:
        before_snap = json.load(f)
        before = {e["path"] for e in before_snap["entries"] if e.get("type") == "file"}
        root = before_snap["root"]
    with open(after_path) as f:
        after = {e["path"] for e in json.load(f)["entries"] if e.get("type") == "file"}
    with open(results_path) as f:
        results = json.load(f)

    moved_srcs = set()   # src paths that should now be GONE from before
    moved_dests = set()  # dest paths that should now be NEW in after
    for r in results:
        rel_dest = os.path.relpath(r["dest"], root).replace("\\", "/")
        if r["status"] in ("moved", "moved_renamed_on_collision"):
            moved_srcs.add(os.path.relpath(r["src"], root).replace("\\", "/"))
            moved_dests.add(rel_dest)
        elif r["status"] == "copied_original_retained":
            # src stays put (not expected-removed); dest is a new copy.
            moved_dests.add(rel_dest)
        # "failed" and "skipped_dest_exists" (legacy) change nothing - not
        # added to either set, so any actual change there still surfaces.

    removed = before - after
    added = after - before
    unexpected_removed = sorted(removed - moved_srcs)
    unexpected_added = sorted(added - moved_dests)
    expected_removed = sorted(removed & moved_srcs)

    report = {
        "expected_removed_count": len(expected_removed),
        "unexpected_removed": unexpected_removed,
        "unexpected_added": unexpected_added,
        "clean": len(unexpected_removed) == 0 and len(unexpected_added) == 0,
    }
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"diff: clean={report['clean']} unexpected_removed={len(unexpected_removed)} unexpected_added={len(unexpected_added)} -> {out_path}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "snapshot" and len(sys.argv) == 4:
        cmd_snapshot(sys.argv[2], sys.argv[3])
    elif cmd == "move" and len(sys.argv) == 4:
        cmd_move(sys.argv[2], sys.argv[3])
    elif cmd == "diff" and len(sys.argv) == 6:
        cmd_diff(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
