---
name: Update Article
description: Update, expand, or revise an existing article while preserving its creation date, updating its in-article changelog, and syncing repository-level revision trails.
---

# Update Article

This skill guides the agent when modifying, expanding, or correcting an existing article in `ThoughtsInWords` so that neither the article-level history nor the repository-level activity trail is lost.

## Usage

When the user asks to "update article", "expand", "revise", or "add a section to" an existing article:

1. **Read & Preserve Immutable Metadata**:
   * Read the target article completely.
   * Keep the original `**Date:** Month Day, Year` header intact—never overwrite the original publication date.
   * Add or update `**Last Updated:** Month Day, Year` directly beneath `**Date:**` using the current date (e.g., `**Last Updated:** November 16, 2026`).

2. **Apply Content Changes**:
   * Edit or expand the article sections cleanly while preserving existing `## References` and inline links.
   * Check whether `## Related Articles` needs new cross-links for any newly added concepts.

3. **Update the In-Article `## Changelog`**:
   * Place `## Changelog` at the very bottom of the article (after `## References`, if present).
   * If the article does not yet have a `## Changelog` section, create it with today's update bullet first and an initial publication bullet using the article's `**Date:**`:
     ```markdown
     ## Changelog

     - **Mon DD, YYYY:** Summary of what was added, updated, or fixed.
     - **Mon DD, YYYY:** Initial publication.
     ```
   * If `## Changelog` already exists, prepend the new `- **Mon DD, YYYY:** ...` bullet at the top of the list (reverse chronological order).

4. **Update Repository-Level Trails (`README.md`, `articles/README.md`, `articles/CHANGELOG.md`)**:
   * **Check `[NEW]` vs. `[UPDATED]` exclusivity**: If the article currently holds `[NEW]` (within the active `Recent Additions` cohort), keep `[NEW]` instead of adding `[UPDATED]`—still update `**Last Updated:**`, in-article `## Changelog`, and `articles/CHANGELOG.md`.
   * **Root `README.md`** (for articles without `[NEW]`):
     * Under `* **Recently Updated (Revision Trail, Max 5):**`, prepend (or move to the top if already present):
       `* [Article Title](./articles/[category]/[kebab-case-slug].md) *(Updated Mon DD, YYYY — brief summary)* \`[UPDATED]\``
     * If the list exceeds 5 entries, evict the oldest entry beyond the cap of 5 and track what was evicted.
   * **`articles/README.md`**:
     * Add `[UPDATED]` after the article's link under `## Article Index` (e.g., `- [Article Title](category/slug.md) [UPDATED]`), if it does not hold `[NEW]`.
     * Remove `[UPDATED]` from any entry evicted from `Recently Updated` in `README.md`.
   * **`articles/CHANGELOG.md`**:
     * Add an entry under `### Month Day, Year` (creating the date header in reverse chronological order if needed):
       `* **Updated:** [Article Title](category/slug.md) — brief summary of changes.`
     * If any `[UPDATED]` entry was rotated out of `Recently Updated`, note the rotation if appropriate.

5. **Verify Repository Health**:
   * Run `bash verify_links.sh` and confirm Checks 1–7 pass with exit code `0`.
   * *(Optional)* Run `.agent/skills/review_article/SKILL.md` to perform a full Reader Mode, Subject Matter Expert, and Technical Architect review and link a `0–10` Before/After report under `reviews/<category>/<slug>-review.md`.
