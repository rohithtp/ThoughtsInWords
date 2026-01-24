---
name: Create Article
description: Create a new article from a given topic or URL, summarize content, and update the repository index.
---

# Create Article

This skill guides the agent in creating a new article within the `ThoughtsInWords` repository. It involves reading source material (if provided), creating a markdown file in the appropriate category, and updating the main README index.

## Usage

When the user asks to "create a new article" or "add a summary of [URL]":

1.  **Analyze Request & Determine Category**:
    *   **List the subdirectories** in `articles/` to see available categories (e.g., run `list_dir` on `articles/`).
    *   **Select the best matching category** from the existing folders based on the article's content or topic.
    *   If a URL is provided, use `read_url_content` to fetch and understand the content.
    *   Determine the current date.

2.  **Generate Content**:
    *   Create a summary or full article in Markdown format.
    *   Include metadata at the top:
        ```markdown
        # Title of Article

        **Source:** [Hostname](URL) (if applicable)
        **Date:** Month Day, Year
        ```
    *   Structure the content with clear headers (`## Summary`, `## Key Points`, `## Conclusion`, etc.).

3.  **create File**:
    *   Determine the file path: `articles/[category]/[slug-title].md`.
    *   Use `write_to_file` to create the file.

4.  **Update Index**:
    *   Open `articles/README.md`.
    *   Find the appropriate category header (e.g., `### Frontend`).
    *   Append a link to the new article in the list:
        `- [[category]/[slug-title].md]([category]/[slug-title].md) - Brief description`

## Example

**User:** "Create an article about the new React compiler from this link..."

**Action:**
1.  Read URL.
2.  Write `articles/frontend/react-compiler-overview.md`.
3.  Add entry to `articles/README.md` under `### Frontend`.
