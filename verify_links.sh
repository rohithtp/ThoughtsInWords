#!/bin/bash

README_FILE="articles/README.md"
MISSING_FILES=0

echo "Checking links in $README_FILE..."

# Extract links using grep and sed
# Pattern matches standard markdown links [text](path)
# We assume paths are relative to the root or relative to the README. 
# based on the README content: `articles/ai/vercel_ai_sdk_6.md`, these are relative to workspace root if running from root, 
# OR relative to README if they are `ai/vercel...`?
# Let's check the content of README again.
# " [`ai/vercel_ai_sdk_6.md`](ai/vercel_ai_sdk_6.md)"
# So the link is `ai/vercel_ai_sdk_6.md`.
# The README is in `articles/`.
# So `articles/ai/vercel_ai_sdk_6.md` relative to `articles/` is `ai/vercel_ai_sdk_6.md`.
# So the paths in README are relative to `articles/`.

grep -o ']([^)]*)' "$README_FILE" | sed 's/](//;s/)//' | while read -r link; do
  # Skip http links
  if [[ "$link" == http* ]]; then
    continue
  fi

  # Construct full path
  # The README is in `articles/`, so we prepend `articles/` to the link path
  FULL_PATH="articles/$link"

  if [ ! -f "$FULL_PATH" ]; then
    echo "❌ Missing: $FULL_PATH (referenced as $link)"
    MISSING_FILES=1
  else
    echo "✅ Found: $FULL_PATH"
  fi
done

if [ $MISSING_FILES -eq 0 ]; then
  echo "All links are valid!"
  exit 0
else
  echo "Some links are broken."
  exit 1
fi
