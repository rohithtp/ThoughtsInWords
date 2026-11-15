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

3. **Add Unlisted Files, Enforce Title-First Formatting & Sync Hybrid Window `[NEW]` Tags**:
   * Identify files found in the scan that are not listed in `articles/README.md`.
   * Ensure all index entries use title-first formatting:
     `- [Article Title / Summary]([category]/[kebab-case-slug].md)`
   * Apply the **Hybrid Window `[NEW]` Policy** across all dated articles:
     * Compute the active cohort from each article's `**Date:** Month Day, Year` header: include all articles published within **7 days** of the newest article's `**Date:**`, bounded by a **minimum of 3** and a **maximum of 5** articles (`expected_count = min(5, max(3, count_within_7_days))`).
     * Ensure `README.md` lists those exact cohort articles (newest first) under `* **Recent Additions (7-Day Window, Min 3 / Max 5):**` with `` `[NEW]` ``.
     * Ensure `articles/README.md` carries `[NEW]` on those exact same cohort entries under `## Article Index`, and remove `[NEW]` from any entries outside the cohort.
   * For any newly discovered unlisted files, determine the appropriate category (and subsection) from the parent folder name and content, then insert the title-first entry alphabetically (with `[NEW]` if it belongs to the active cohort).

4. **Sync Counts & Verify**:
   * Update category and total article counts in `articles/README.md` (`## Organization`, `## Category Directory`) and root `README.md` (`## Explore the Digital Garden`).
   * Verify that the `[NEW]` set in `README.md` (`Recent Additions`) matches `articles/README.md` 1-to-1.
   * Run `bash verify_links.sh` and confirm all 5 checks pass with exit code `0`.
