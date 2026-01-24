---
name: Organize README
description: Scans the `articles/` directory for broken links or unlisted files in `articles/README.md` and fixes them.
---

# Organize README

This skill ensures that the `articles/README.md` file accurately reflects the contents of the `articles/` directory. It handles fixing broken links and adding missing articles to the index.

## Usage

When the user asks to "organize readme", "fix links", or "update index":

1.  **Scan Files**:
    *   List all `.md` files in `articles/` recursively.
    *   Command: `find articles -type f -name "*.md"` (or similar).
    *   Read `articles/README.md`.

2.  **Verify & Fix Links**:
    *   Check every link in `articles/README.md`.
    *   If a link points to a file that does not exist at that path, check if the file exists elsewhere in the `articles/` directory (e.g., in a date-based folder like `2026/01/...`).
    *   **Update the link** in `articles/README.md` to point to the correct, existing file path.
    *   **Do not move the file** unless explicitly instructed; prefer updating the link to match reality.

3.  **Add Unlisted Files**:
    *   Identify files found in the scan that are NOT listed in `articles/README.md`.
    *   For each unlisted file:
        *   Determine the appropriate category from the parent folder name or by analyzing the file content.
        *   If the file is in a date-based folder (e.g., `2026/01/19/`), infer the category from the content or filename, or add it to a "New/Uncategorized" section if unsure.
        *   Add a list entry to the corresponding section in `articles/README.md`:
            `- [relative/path/to/file.md](relative/path/to/file.md) - Description or Title`

4.  **Formatting**:
    *   Ensure the `articles/README.md` maintains a clean, categorized structure.
    *   Sort entries alphabetically or chronologically if appropriate.
