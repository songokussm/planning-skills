#!/usr/bin/env bash
# Pre-push check. Fails if any tracked file matches a private pattern.
# Patterns live outside the repo, one regex per line:
#   ../../planning-skills.private-patterns.txt
set -u
cd "$(dirname "$0")/.."
pat="../../planning-skills.private-patterns.txt"
[ -f "$pat" ] || { echo "missing $pat"; exit 2; }
hits=$(git ls-files -z | xargs -0 grep -nIiE -f "$pat" 2>/dev/null)
generic=$(git ls-files -z | xargs -0 grep -nIoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|\(?[0-9]{3}\)?[-. ][0-9]{3}[-. ][0-9]{4}|[A-Z]:\\\\' 2>/dev/null | grep -v noreply)
if [ -n "$hits$generic" ]; then echo "$hits"; echo "$generic"; echo "FAIL: private data found"; exit 1; fi
echo "PASS"
