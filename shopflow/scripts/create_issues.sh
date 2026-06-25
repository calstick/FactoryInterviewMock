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

trim() { echo "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'; }

# 1. Collect every unique label used across the issue files.
declare -A LABELSET
for f in "$DIR"/ISSUE-*.md; do
  labels=$(grep -m1 '^labels:' "$f" | sed 's/^labels:[[:space:]]*//')
  IFS=',' read -ra parts <<< "$labels"
  for l in "${parts[@]}"; do
    t="$(trim "$l")"
    [[ -n "$t" ]] && LABELSET["$t"]=1
  done
done

# 2. Ensure each label exists. `--force` creates it, or updates it if present,
#    so this never errors on labels that already exist (e.g. bug, enhancement).
echo "Ensuring ${#LABELSET[@]} labels exist..."
for label in "${!LABELSET[@]}"; do
  gh label create "$label" --force "${REPO_ARG[@]}" >/dev/null
done

# 3. Create the issues, passing each label as its own --label flag.
for f in "$DIR"/ISSUE-*.md; do
  title=$(grep -m1 '^title:' "$f" | sed 's/^title:[[:space:]]*//')
  labels=$(grep -m1 '^labels:' "$f" | sed 's/^labels:[[:space:]]*//')
  body=$(awk 'found{print} /^---$/{found=1}' "$f")

  label_args=()
  IFS=',' read -ra parts <<< "$labels"
  for l in "${parts[@]}"; do
    t="$(trim "$l")"
    [[ -n "$t" ]] && label_args+=(--label "$t")
  done

  echo "Creating issue: $title"
  gh issue create --title "$title" --body "$body" "${label_args[@]}" "${REPO_ARG[@]}"
done

echo "Done. All seeded issues created."
