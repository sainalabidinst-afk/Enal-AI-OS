#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="."
OUTDIR="$(pwd)/repo_inspect_output_$(date +%Y%m%d%H%M%S)"
mkdir -p "$OUTDIR"
echo "Collecting file tree..."
if command -v tree >/dev/null 2>&1; then
  tree -a -I 'node_modules|venv|.git' -L 3 > "$OUTDIR/tree.txt" || true
else
  find . -maxdepth 3 -not -path './.git/*' | sed 's/^\.\///' > "$OUTDIR/tree.txt"
fi
echo "Listing top-level files..."
ls -la > "$OUTDIR/ls.txt"
echo "Collecting package files..."
[ -f package.json ] && cp package.json "$OUTDIR/" || true
[ -f requirements.txt ] && cp requirements.txt "$OUTDIR/" || true
[ -f pyproject.toml ] && cp pyproject.toml "$OUTDIR/" || true
echo "Collecting git metadata..."
git rev-parse --abbrev-ref HEAD > "$OUTDIR/git_branch.txt" || true
git log -n 10 --pretty=format:'%h %ad %s' --date=short > "$OUTDIR/git_recent_commits.txt" || true
echo "Zipping output..."
zip -r "$OUTDIR.zip" "$(basename "$OUTDIR")" >/dev/null 2>&1 || true
echo "Done. Output: $OUTDIR.zip"