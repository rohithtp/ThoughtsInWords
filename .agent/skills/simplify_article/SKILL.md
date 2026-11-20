---
name: Simplify Article
description: Reformat a markdown article to improve readability, simplify structure, and fix formatting, while strictly preserving all references and links.
---

# Simplify Article

This skill guides you through the process of cleaning up and simplifying a markdown article.

## Primary Hybrid `run_workflow` Execution Path (Option H3)

For isolated single or parallel batch simplification (`article_paths`, defaulting to `workspace: "share"` for multi-article batches) with deterministic **100% link-retention diffing**, execute [`run_content_workflow.py`](../create_article/scripts/run_content_workflow.py) via `run_workflow`:

```python
run_workflow(
    Script=(
        "import runpy\n"
        "mod = runpy.run_path('.agent/skills/create_article/scripts/run_content_workflow.py', init_globals=globals())\n"
        "await mod['run_pipeline'](globals())\n"
    ),
    Args={
        "mode": "simplify",
        "article_paths": ["articles/<category>/<slug>.md"],
    },
    Description="Run scoped hybrid article simplification with link-retention gate",
)
```

* Before index reconciliation runs, `verify_article_mutation()` in [`schemas.py`](../review_article/scripts/schemas.py) compares pre- and post-edit links (`extract_markdown_links()`) and aborts if any citation, link, `**Date:**`, or Invariant 3 section order was dropped.

## Usage
When the user asks to "simplify article", "make readable", or "clean up format" for a specific file.

## Steps

1.  **Read the File**
    - Read the entire content of the target article.

2.  **Analyze and Reformat**
    - Analyze the content for:
        - Inconsistent header hierarchy (ensure `#` -> `##` -> `###` structure).
        - Cluttered lists (ensure items are on separate lines).
        - Poor spacing (add blank lines between sections).
        - Long, complex paragraphs (break them down if possible, but be careful not to change the meaning).
    - **Governance & Metadata Compliance**: Enforce [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 1 (Pure Open-Source Systems Mandate & `Scope & Licensing Note`)** and **Invariant 3** (preserve immutable `**Date:**`, add/update `**Last Updated:**`, keep `## Related Articles` → `## References` → `## Changelog` at the bottom):
        - Prepend `- **Mon DD, YYYY:** Simplified formatting and structure (preserving all references and links).` to `## Changelog`.
    - **CRITICAL — Zero-Loss Reference & Link Guarantee**:
        - **You MUST NOT delete any `## References`, `## Related Articles`, `## Changelog` history, footnotes, or inline links/citations.**
        - Ensure links remain attached to the relevant information and point to valid targets.

3.  **Apply Changes**
    - Rewrite or edit the file cleanly with:
        - A clear Title (`# Title`).
        - Logical Sections (`## Section`).
        - Bullet points for lists.
        - A Mermaid flow diagram to visualize complex structures, processes, or workflows if required.
    - Ensure there is a newline before and after headers and lists.

4.  **Single-Writer Trail Reconciliation & Verification (Option A4)**
    - **Write Scope Partition:** Never edit `README.md`, `articles/README.md`, or `articles/CHANGELOG.md` directly. Hand off an [`INDEX_HANDOFF_SCHEMA`](../review_article/scripts/schemas.py) payload to [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py) via [`run_python.sh`](../organize_readme/scripts/run_python.sh) (per [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 4**):
      ```bash
      bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff '{
        "action": "Simplified",
        "article_path": "articles/<category>/<slug>.md",
        "title": "Article Title",
        "date": "<original Date>",
        "last_updated": "<today Month Day, Year>",
        "changelog_summary": "Simplified structure and readability while preserving all references"
      }'
      ```
    - [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py) syncs `[UPDATED]` exclusivity, records `* **Simplified:**` in `articles/CHANGELOG.md`, and executes `bash verify_links.sh` (Checks 1–8 == exit `0`).
    - Confirm that ALL references/links appearing in the original text are present in the new text (use `workspace: "share"` when running batch simplification across multiple articles concurrently, merging into `--handoff '[...]'` at fan-in).
