#!/usr/bin/env bash
set -euo pipefail

COMMIT_MSG="${1:-}"
BOOKMARK="${2:-main}"

if [[ -z "${COMMIT_MSG// }" ]]; then
  echo "❌ Error: Commit message is required." >&2
  echo "Usage: bash .agent/skills/commit_and_push/scripts/prepare_commit.sh \"<commit_message>\" [bookmark]" >&2
  exit 2
fi

echo "🔍 [Step 1/3] Running repository verification gate (verify_links.sh Checks 1-8)..."
bash verify_links.sh

echo "📝 [Step 2/3] Describing working copy revision (@)..."
jj describe -m "$COMMIT_MSG"

echo "🔖 [Step 3/3] Advancing bookmark '${BOOKMARK}' to current revision (@)..."
jj bookmark set "$BOOKMARK" -r @

echo "✅ Pre-push gate passed and bookmark '${BOOKMARK}' staged at @. Ready for: jj git push --bookmark ${BOOKMARK}"
