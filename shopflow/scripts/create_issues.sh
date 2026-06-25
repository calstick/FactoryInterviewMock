#!/usr/bin/env bash
# Creates the seeded ShopFlow backlog as real GitHub issues.
# Prerequisites: GitHub CLI (`gh`) installed and authenticated (`gh auth login`),
# run from inside the repo (or set REPO=owner/name).
#
# Usage:  ./scripts/create_issues.sh
#         REPO="your-org/shopflow" ./scripts/create_issues.sh
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../issues" && pwd)"
REPO_ARG=()
if [[ -n "${REPO:-}" ]]; then
  REPO_ARG=(--repo "$REPO")
fi

for f in "$DIR"/ISSUE-*.md; do
  title=$(grep -m1 '^title:' "$f" | sed 's/^title:[[:space:]]*//')
  labels=$(grep -m1 '^labels:' "$f" | sed 's/^labels:[[:space:]]*//')
  body=$(awk 'found{print} /^---$/{found=1}' "$f")

  echo "Creating issue: $title"
  gh issue create --title "$title" --body "$body" --label "$labels" "${REPO_ARG[@]}"
done

echo "Done. All seeded issues created."
