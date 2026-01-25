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
    - **CRITICAL**: Check for a "References" section or any inline links/citations.
        - **You MUST NOT delete any references, footnotes, or links.**
        - Ensure the "References" section remains at the bottom of the file if it exists.
        - If you simplify text, ensure the anchor links or citations remain attached to the relevant information.

3.  **Apply Changes**
    - Use `replace_file_content` (if rewriting the whole file is safer/easier to ensure structure) or `multi_replace_file_content` to update the file.
    - Structure the document with:
        - A clear Title (`# Title`).
        - Logical Sections (`## Section`).
        - Bullet points for lists.
    - Ensure there is a newline before and after headers and lists.

4.  **Verify**
    - Briefly confirm that the content is more readable.
    - Confirm that ALL references/links appearing in the original text are present in the new text.
