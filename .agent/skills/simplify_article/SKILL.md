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
    - Use `view_file` to read the entire content of the target article.

2.  **Analyze and Reformat**
    - Analyze the content for:
        - Inconsistent header hierarchy (ensure `#` -> `##` -> `###` structure).
        - Cluttered lists (ensure items are on separate lines).
        - Poor spacing (add blank lines between sections).
        - Long, complex paragraphs (break them down if possible, but be careful not to change the meaning).
    - **Pure Open-Source Systems & Scope Check**: Verify that any tools, libraries, frameworks, or systems mentioned in the article are **pure open-source systems** only, and do **not** refer to premium/commercial-only systems, proprietary/vendor-locked systems, or community-based/open-core ("Community Edition") systems (remove or replace non-qualifying systems with pure open-source equivalents while preserving valid standard/specification references). If the article covers systems/tooling and does not already state that these categories are excluded, add:
        `> **Scope & Licensing Note:** This article strictly covers pure open-source systems. Premium, proprietary/vendor-locked, and community-edition (open-core) systems are currently not included.`
    - **Preserve Metadata & Update Trail**:
        - Keep the original `**Date:** Month Day, Year` unchanged.
        - Add or update `**Last Updated:** Month Day, Year` directly below `**Date:**` using today's date.
    - **CRITICAL**: Check for `## References`, `## Related Articles`, `## Changelog`, or any inline links/citations.
        - **You MUST NOT delete any references, footnotes, changelog history, or links.**
        - Ensure links are present and refer to working locations if possible.
        - Keep `## Related Articles`, `## References`, and `## Changelog` at the bottom of the file (with `## Changelog` last).
        - If you simplify text, ensure the anchor links or citations remain attached to the relevant information.
        - Prepend a new entry to `## Changelog` (creating the section if missing, seeded with the original `**Date:**` as `Initial publication.`):
          `- **Mon DD, YYYY:** Simplified formatting and structure (preserving all references and links).`

3.  **Apply Changes**
    - Use `edit_file` (or `write_file` with `Overwrite: true` if rewriting the whole file is cleaner) to update the file.
    - Structure the document with:
        - A clear Title (`# Title`).
        - Logical Sections (`## Section`).
        - Bullet points for lists.
        - A Mermaid flow diagram to visualize complex structures, processes, or workflows if required.
    - Ensure there is a newline before and after headers and lists.

4.  **Update Repository Trail & Verify**
    - Follow the repo-level trail rules in `.agent/skills/update_article/SKILL.md`:
        - Unless the article already holds `[NEW]`, prepend it to `* **Recently Updated (Revision Trail, Max 5):**` in `README.md` with `` `[UPDATED]` `` (capping at 5) and sync `[UPDATED]` in `articles/README.md`.
        - Record the simplification under today's date in `articles/CHANGELOG.md` (`* **Simplified:** [Article Title](category/slug.md) — ...`).
    - Run `bash verify_links.sh` and confirm Checks 1–7 pass with exit code `0`.
    - Confirm that ALL references/links appearing in the original text are present in the new text.
