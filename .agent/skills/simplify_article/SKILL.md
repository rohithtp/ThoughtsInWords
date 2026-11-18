---
name: Simplify Article
description: Reformat a markdown article to improve readability, simplify structure, and fix formatting, while strictly preserving all references and links.
---

# Simplify Article

This skill guides you through the process of cleaning up and simplifying a markdown article.

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

4.  **Update Repository Trail & Verify**
    - Delegate repository trail reconciliation to [`organize_readme/SKILL.md`](../organize_readme/SKILL.md) (per [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 4**) with `articles/CHANGELOG.md` action ``* **Simplified:** [Article Title](category/slug.md) — ...``.
    - Run `bash verify_links.sh` and confirm Checks 1–7 pass with exit code `0`.
    - Confirm that ALL references/links appearing in the original text are present in the new text.
