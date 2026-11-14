---
name: Organize README
description: Scans the `articles/` directory for broken links, unlisted files, naming issues, or stale counts in `articles/README.md` and fixes them.
---

# Organize README

This skill ensures that `articles/README.md` and root `README.md` accurately reflect the contents and structure of the `articles/` directory.

## Usage

When the user asks to "organize readme", "fix links", or "update index":

1. **Scan Files & Naming**:
   * List all `.md` files in `articles/` recursively (excluding `articles/README.md`).
   * Ensure every article lives inside a topic category folder (`articles/<category>/<kebab-case>.md`), not date-based folders.
   * Ensure all filenames strictly follow lowercase `kebab-case.md` and there are no empty directories.
   * Read `articles/README.md` and root `README.md`.

2. **Verify & Fix Links**:
   * Check every link in `articles/README.md`, root `README.md`, and internal cross-links across articles.
   * If a link points to a missing path, check if the file was moved or renamed in `articles/` and update the link to point to the existing file path.

3. **Add Unlisted Files & Enforce Title-First Formatting**:
   * Identify files found in the scan that are not listed in `articles/README.md`.
   * Ensure all index entries use title-first formatting:
     `- [Article Title / Summary]([category]/[kebab-case-slug].md)`
   * If unlisted files are added:
     * **Remove Existing Tags**: Strip any existing `[NEW]` tags from all entries in `articles/README.md` so only the newest entry carries `[NEW]` after the link.
     * Determine the appropriate category (and subsection) from the parent folder name and content, then insert the title-first entry alphabetically.
     * *(If multiple unlisted files are added at once, apply `[NEW]` only to the latest one.)*
   * If no new files are added, ensure at most one `[NEW]` tag remains in `articles/README.md`.

4. **Sync Counts & Verify**:
   * Update category and total article counts in `articles/README.md` (`## Organization`, `## Category Directory`) and root `README.md` (`## Explore the Digital Garden`).
   * Update the Latest Addition link in root `README.md` to match the entry marked `[NEW]`.
   * Run `bash verify_links.sh` and confirm all 4 checks pass with exit code `0`.
