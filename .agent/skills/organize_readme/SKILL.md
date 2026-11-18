---
name: Organize README
description: Scans the `articles/` directory for broken links, unlisted files, naming issues, or stale counts in `articles/README.md` and fixes them.
---

# Organize README

This skill is the canonical procedural owner for updating `README.md`, `articles/README.md`, and `articles/CHANGELOG.md` so repository indexes, badge cohorts, and activity logs stay synchronized with the `articles/` tree and the declarative invariants in [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md).

## Usage

When the user asks to "organize readme", "fix links", or "update index", or when a content skill (`create_article`, `update_article`, `simplify_article`, `review_article`) hands off trail reconciliation:

1. **Scan Files & Naming (Invariant 2)**:
   * List all `.md` files in `articles/` recursively (excluding `articles/README.md` and `articles/CHANGELOG.md`).
   * Enforce [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) Invariant 2: topic category folders (`articles/<category>/<kebab-case>.md`), lowercase `kebab-case.md` filenames, no date-based folders, and zero empty directories.
   * Read `articles/README.md`, `articles/CHANGELOG.md`, and root `README.md`.

2. **Verify & Fix Links**:
   * Check every link in `articles/README.md`, `articles/CHANGELOG.md`, root `README.md`, and internal cross-links across articles.
   * If a link points to a missing path, check if the file was moved or renamed in `articles/` and update the link to point to the existing file path.

3. **Reconcile Index, `[NEW]` / `[UPDATED]` Badges & `articles/CHANGELOG.md` (Invariant 4)**:
   * Identify unlisted files found in the scan and insert title-first entries alphabetically under the appropriate category (and subsection) in `articles/README.md`:
     `- [Article Title / Summary]([category]/[kebab-case-slug].md)`
   * Apply the **Hybrid Window `[NEW]` Policy** from [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) Invariant 4 (`expected_count = min(5, max(3, count_within_7_days))` anchored to the newest article's `**Date:**`):
     * Ensure root `README.md` lists those exact cohort articles (newest first) under `* **Recent Additions (7-Day Window, Min 3 / Max 5):**` formatted as `* [Article Title](./articles/[category]/[kebab-case-slug].md) *(Mon DD, YYYY)* \`[NEW]\``.
     * Ensure `articles/README.md` carries `[NEW]` on those exact same cohort entries under `## Article Index`, and remove `[NEW]` from any evicted entries outside the cohort.
   * Sync the **Recently Updated Revision Trail (`[UPDATED]`, Max 5)**:
     * Scan articles for `**Last Updated:** Month Day, Year` and `## Changelog` (and consume any trail handoffs from upstream content skills).
     * Ensure root `README.md` lists up to the 5 most recently updated articles (excluding any holding `[NEW]` per Invariant 4 exclusivity) under `* **Recently Updated (Revision Trail, Max 5):**` formatted as `* [Article Title](./articles/[category]/[kebab-case-slug].md) *(Updated Mon DD, YYYY — brief summary)* \`[UPDATED]\``.
     * Ensure `articles/README.md` carries `[UPDATED]` on those exact same entries (removing `[UPDATED]` from evicted 6th+ entries, and never combining `[NEW]` and `[UPDATED]`).
   * **Record in `articles/CHANGELOG.md`**: Under `### Month Day, Year` (creating the date header in reverse chronological order if needed), log events using the canonical action prefixes:
     * ``* **Added:** [Article Title](category/slug.md)``
     * ``* **Updated:** [Article Title](category/slug.md) — <brief summary>.``
     * ``* **Simplified:** [Article Title](category/slug.md) — <brief summary>.``
     * ``* **Reviewed & Updated:** [Article Title](category/slug.md) — <brief summary> ([Review Report](../reviews/<category>/<slug>-review.md)).``
     * ``* **Rotated (`[NEW]`):** Removed `[NEW]` from [Article Title](category/slug.md) ...`` *(note badge rotations when entries leave the active cohort)*.

4. **Sync Counts & Verify**:
   * Update category and total article counts in `articles/README.md` (`## Organization`, `## Category Directory`) and root `README.md` (`## Explore the Digital Garden`).
   * Verify that the `[NEW]` and `[UPDATED]` sets in `README.md` match `articles/README.md` 1-to-1.
   * Run `bash verify_links.sh` and confirm all 7 checks pass with exit code `0`.
