---
name: Update Article
description: Update, expand, or revise an existing article while preserving its creation date, updating its in-article changelog, and syncing repository-level revision trails.
---

# Update Article

This skill guides the agent when modifying, expanding, or correcting an existing article in `ThoughtsInWords` so that neither the article-level history nor the repository-level activity trail is lost.

## Primary Hybrid `run_workflow` Execution Path (Option H3)

For isolated revisions, batch cross-link backfills (`article_paths`), or deterministic immutable-date and link-retention checks prior to index reconciliation, execute [`run_content_workflow.py`](../create_article/scripts/run_content_workflow.py) via `run_workflow`:

```python
run_workflow(
    Script=(
        "import runpy\n"
        "mod = runpy.run_path('.agent/skills/create_article/scripts/run_content_workflow.py', init_globals=globals())\n"
        "await mod['run_pipeline'](globals())\n"
    ),
    Args={
        "mode": "update",
        "article_path": "articles/<category>/<slug>.md",
        "instructions": "Expand failure modes and refresh reciprocal links.",
    },
    Description="Run scoped hybrid article update workflow",
)
```

* `run_content_workflow.py` snapshots baseline links and `**Date:**`, validates updates against [`CONTENT_MUTATION_RESULT_SCHEMA`](../review_article/scripts/schemas.py) and `verify_article_mutation()`, and reconciles both the target article and `reciprocal_articles_touched` via [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py).

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

4. **Single-Writer Index & Trail Reconciliation (`README.md`, `articles/README.md`, `articles/CHANGELOG.md`)**:
   * **Write Scope Partition (Option A4):** Never edit `README.md`, `articles/README.md`, or `articles/CHANGELOG.md` directly. Emit an [`INDEX_HANDOFF_SCHEMA`](../review_article/scripts/schemas.py) payload to [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py) via [`run_python.sh`](../organize_readme/scripts/run_python.sh) (enforcing [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 4**):
     ```bash
     bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff '{
       "action": "Updated",
       "article_path": "articles/<category>/<slug>.md",
       "title": "Article Title",
       "date": "<original Date>",
       "last_updated": "<today Month Day, Year>",
       "changelog_summary": "Brief summary of changes",
       "reciprocal_articles_touched": []
     }'
     ```
   * [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py) enforces `[NEW]` vs. `[UPDATED]` exclusivity, updates `Recently Updated (Max 5)` across both READMEs, appends `* **Updated:**` in `articles/CHANGELOG.md`, and runs `bash verify_links.sh` (Checks 1–8 == exit `0`).

5. **Optional Quality Audit**:
   * *(Optional)* Run [`review_article/SKILL.md`](../review_article/SKILL.md) (`run_review_workflow.py`) to perform a schema-validated Reader Mode, Subject Matter Expert, and Technical Architect review and link a `0–10` Before/After report under `reviews/<category>/<slug>-review.md`.
