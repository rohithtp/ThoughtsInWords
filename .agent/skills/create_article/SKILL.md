---
name: Create Article
description: Create a new article from a given topic or URL, summarize content, and update the repository index.
---

# Create Article

This skill guides the agent in creating a new article within the `ThoughtsInWords` repository. It involves reading source material (if provided), creating a markdown file in the appropriate topic directory, adding bidirectional cross-links, and updating the README indexes.

## Usage

When the user asks to "create a new article" or "add a summary of [URL]":

1. **Analyze Request & Determine Category**:
   * **List the subdirectories** in `articles/` to see available topic categories (e.g., `ai`, `cloud-native`, `design`, `devops`, `distributed-systems`, `environment`, `frontend`, `licensing`, `philosophy`, `testing`, `tools`, `travel`).
   * **Select the best matching category** from the existing topic folders based on the article's content or topic. Never place articles in date-based directories (e.g., `YYYY/MM/DD`).
   * If a URL is provided, read and summarize its content.
   * Determine the current date.

2. **Generate Content & Cross-Links**:
   * Create a summary or full article in Markdown format with clear headers (`## Summary`, `## Key Points`, `## Conclusion`, etc.).
   * Follow [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 1 (Pure Open-Source Systems Mandate)** when discussing tools, frameworks, or platforms, and include the exact `Scope & Licensing Note` callout if applicable.
   * Follow [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 3 (Header Metadata & Bottom Section Ordering)**:
     ```markdown
     # Title of Article

     **Source:** [Hostname](URL) (if applicable)
     **Date:** Month Day, Year
     ```
     Include `## Related Articles` (2–3 relative `.md` links), preserve `## References` if present, and end with an initial `## Changelog`:
     ```markdown
     ## Related Articles

     - [Related Article Title](sibling-article.md) — brief note on how it connects.
     - [Cross-Topic Article Title](../other-category/article-slug.md) — brief note on how it connects.

     ## Changelog

     - **Mon DD, YYYY:** Initial publication.
     ```
   * Where appropriate, add a reciprocal link back in closely related existing articles; when editing an existing article from an earlier date, update its metadata and trail per [`update_article/SKILL.md`](../update_article/SKILL.md).

3. **Create File (`kebab-case.md`)**:
   * Per [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 2**, save to `articles/[category]/[kebab-case-slug].md` using lowercase `kebab-case.md` (no underscores or uppercase characters).

4. **Reconcile Indexes, `[NEW]` Tags & Changelog (Single-Writer Handoff — Option A4)**:
   * **Write Scope Partition:** Never edit `README.md`, `articles/README.md`, or `articles/CHANGELOG.md` directly. Emit an [`INDEX_HANDOFF_SCHEMA`](../review_article/scripts/schemas.py) payload to [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py) via [`run_python.sh`](../organize_readme/scripts/run_python.sh) (enforcing [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 4**):
     ```bash
     bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff '{
       "action": "Added",
       "article_path": "articles/<category>/<kebab-case-slug>.md",
       "title": "Title of Article",
       "date": "Month Day, Year",
       "changelog_summary": "Brief summary of the new article",
       "reciprocal_articles_touched": []
     }'
     ```
   * [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py) inserts the article alphabetically in `articles/README.md`, recomputes the Hybrid Window `[NEW]` cohort (`README.md` + `articles/README.md`), syncs counts, logs `* **Added:**` / `* **Rotated (\`[NEW]\`):**` in `articles/CHANGELOG.md`, and runs `bash verify_links.sh` (Checks 1–8 == exit `0`).

5. **Optional Quality Audit**:
   * *(Optional)* Run [`review_article/SKILL.md`](../review_article/SKILL.md) (`run_review_workflow.py`) to perform a schema-validated Reader Mode, Subject Matter Expert, and Technical Architect review and link a `0–10` Before/After report under `reviews/<category>/<slug>-review.md`.

## Example

**User:** "Create an article about the new React compiler from this link..."

**Action:**
1. Read URL.
2. Write `articles/frontend/react-compiler-overview.md` complying with [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) Invariants 1–3 (`**Date:** Month Day, Year`, `Scope & Licensing Note` if tooling-focused, `## Related Articles`, and initial `## Changelog`).
3. Execute `bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff '...'` (updates `README.md`, `articles/README.md`, `articles/CHANGELOG.md`, and runs `bash verify_links.sh` Checks 1–8).
