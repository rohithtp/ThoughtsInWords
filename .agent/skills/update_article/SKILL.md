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
   * Per [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 3**, keep the original `**Date:** Month Day, Year` intact and add or update `**Last Updated:** Month Day, Year` directly beneath it (e.g., `**Last Updated:** November 16, 2026`).

2. **Apply Content Changes**:
   * Edit or expand the article sections cleanly while preserving existing `## References` and inline links.
   * Verify compliance with [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 1 (Pure Open-Source Systems Mandate & `Scope & Licensing Note`)** across both existing and newly added content.
   * Check whether `## Related Articles` needs new cross-links for any newly added concepts.

3. **Update the In-Article `## Changelog`**:
   * Per [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 3**, ensure `## Changelog` sits at the very bottom (after `## Related Articles` and `## References`), prepending `- **Mon DD, YYYY:** <summary>.` in reverse chronological order (seeding `- **Mon DD, YYYY:** Initial publication.` from `**Date:**` if creating `## Changelog` for the first time).

4. **Update Repository-Level Trails (`README.md`, `articles/README.md`, `articles/CHANGELOG.md`)**:
   * Delegate trail reconciliation to [`organize_readme/SKILL.md`](../organize_readme/SKILL.md) (enforcing [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 4**):
     * Enforce `[NEW]` vs. `[UPDATED]` exclusivity (keep `[NEW]` if already in the active `Recent Additions` cohort; otherwise promote to `Recently Updated (Revision Trail, Max 5)` with `` `[UPDATED]` `` and sync both READMEs).
     * Record the update under `### Month Day, Year` in `articles/CHANGELOG.md` using ``* **Updated:** [Article Title](category/slug.md) — brief summary of changes.``

5. **Verify Repository Health**:
   * Run `bash verify_links.sh` and confirm Checks 1–7 pass with exit code `0`.
   * *(Optional)* Run [`review_article/SKILL.md`](../review_article/SKILL.md) to perform a full Reader Mode, Subject Matter Expert, and Technical Architect review and link a `0–10` Before/After report under `reviews/<category>/<slug>-review.md`.
