#!/usr/bin/env bash
# Create or update PR with description from PR_DESCRIPTION.md (no copy-paste).
set -e
cd "$(dirname "$0")/.."
if [[ ! -f PR_DESCRIPTION.md ]]; then
  echo "PR_DESCRIPTION.md not found."
  exit 1
fi
PR_NUM=$(gh pr view --json number -q .number 2>/dev/null || true)
if [[ -n "$PR_NUM" ]]; then
  echo "Updating existing PR #$PR_NUM..."
  gh pr edit "$PR_NUM" --body-file PR_DESCRIPTION.md
else
  echo "Creating new PR..."
  gh pr create --title "fix: E501 line length, imports model_api, pre-commit et CI" --body-file PR_DESCRIPTION.md
fi
