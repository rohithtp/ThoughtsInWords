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
   * Create a summary or full article in Markdown format.
   * Include metadata at the top:
     ```markdown
     # Title of Article

     **Source:** [Hostname](URL) (if applicable)
     **Date:** Month Day, Year
     ```
   * Structure the content with clear headers (`## Summary`, `## Key Points`, `## Conclusion`, etc.).
   * **Add Related Articles**: Include a `## Related Articles` section at the bottom (before `## References`, if present) linking to 2–3 related existing articles using relative `.md` paths:
     ```markdown
     ## Related Articles

     - [Related Article Title](sibling-article.md) — brief note on how it connects.
     - [Cross-Topic Article Title](../other-category/article-slug.md) — brief note on how it connects.
     ```
   * Where appropriate, add a reciprocal link back in closely related existing articles to strengthen the digital garden mesh.

3. **Create File (`kebab-case.md`)**:
   * Always use lowercase `kebab-case.md` for the filename: `articles/[category]/[kebab-case-slug].md`.
   * Never use underscores (`_`) or uppercase characters in article filenames.

4. **Update Index & Manage `[NEW]` Tag**:
   * Open `articles/README.md`.
   * **Remove Existing Tags**: Remove any existing `[NEW]` tags across all entries in `articles/README.md` (and update the Latest Addition callout in root `README.md`).
   * **Find Category Header**: Locate the appropriate category (and subsection, if applicable) under `## Article Index`.
   * **Add Title-First Entry**: Insert a title-first link in alphabetical order within the section, with `[NEW]` placed after the link:
     `- [Article Title / Summary]([category]/[kebab-case-slug].md) [NEW]`
   * **Update Counts**: Increment the total and category article counts in `articles/README.md` (`## Organization`, `## Category Directory`) and root `README.md` (`## Explore the Digital Garden`).

5. **Verify Repository Health**:
   * Run `bash verify_links.sh` and confirm all checks pass with exit code `0`.

## Example

**User:** "Create an article about the new React compiler from this link..."

**Action:**
1. Read URL.
2. Write `articles/frontend/react-compiler-overview.md` with a `## Related Articles` footer.
3. Remove any existing `[NEW]` tags in `articles/README.md`.
4. Add entry to `articles/README.md` under `### Frontend`:
   `- [React Compiler Overview](frontend/react-compiler-overview.md) [NEW]`
5. Update counts in `articles/README.md` and `README.md`, then run `bash verify_links.sh`.
