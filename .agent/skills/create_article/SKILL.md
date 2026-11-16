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
   * Include metadata at the top — every new article **MUST** include `**Date:** Month Day, Year` (e.g., `**Date:** November 15, 2026`) so the Hybrid Window `[NEW]` lifecycle and verification checks can rank recency accurately:
     ```markdown
     # Title of Article

     **Source:** [Hostname](URL) (if applicable)
     **Date:** Month Day, Year
     ```
   * Structure the content with clear headers (`## Summary`, `## Key Points`, `## Conclusion`, etc.).
   * **Add Related Articles & Initial Changelog**: Include a `## Related Articles` section at the bottom (before `## References`, if present) linking to 2–3 related existing articles using relative `.md` paths, followed by an initial `## Changelog` at the very bottom:
     ```markdown
     ## Related Articles

     - [Related Article Title](sibling-article.md) — brief note on how it connects.
     - [Cross-Topic Article Title](../other-category/article-slug.md) — brief note on how it connects.

     ## Changelog

     - **Mon DD, YYYY:** Initial publication.
     ```
   * Where appropriate, add a reciprocal link back in closely related existing articles to strengthen the digital garden mesh. Whenever editing an existing article published on an earlier date, also update its `**Last Updated:** Month Day, Year` header, its in-article `## Changelog`, the `Recently Updated` / `[UPDATED]` trail in `README.md` and `articles/README.md`, and `articles/CHANGELOG.md`.

3. **Create File (`kebab-case.md`)**:
   * Always use lowercase `kebab-case.md` for the filename: `articles/[category]/[kebab-case-slug].md`.
   * Never use underscores (`_`) or uppercase characters in article filenames.

4. **Update Index & Manage `[NEW]` Tags (Hybrid Window Policy)**:
   * **Hybrid Window `[NEW]` Policy**: Multiple articles can hold `[NEW]` simultaneously. Keep `[NEW]` on all articles published within **7 days** of the newest article's `**Date:**`, bounded by a **minimum of 3** and a **maximum of 5** articles (`expected_count = min(5, max(3, count_within_7_days))`).
   * **Update Root `README.md`**:
     * Open `README.md` and prepend the new article(s) to `* **Recent Additions (7-Day Window, Min 3 / Max 5):**` in reverse chronological order (newest first), formatted as:
       `* [Article Title](./articles/[category]/[kebab-case-slug].md) *(Mon DD, YYYY)* \`[NEW]\``
     * Evict any older entries from `Recent Additions` that fall outside the 7-day window (while keeping at least 3) or exceed the maximum cap of 5. Track which entries were evicted.
   * **Update `articles/README.md` & `articles/CHANGELOG.md`**:
     * Remove `[NEW]` **only** from the entries that were evicted from `Recent Additions` (leave `[NEW]` intact on articles still within the active cohort).
     * Locate the appropriate category (and subsection, if applicable) under `## Article Index` and insert a title-first link in alphabetical order, with `[NEW]` placed after the link:
       `- [Article Title / Summary]([category]/[kebab-case-slug].md) [NEW]`
     * Increment the total and category article counts in `articles/README.md` (`## Organization`, `## Category Directory`) and root `README.md` (`## Explore the Digital Garden`).
     * Record the new article under today's date in `articles/CHANGELOG.md` (`* **Added:** [Article Title](category/kebab-case-slug.md)`), along with any evicted `[NEW]` rotation notes (`* **Rotated (\`[NEW]\`):** ...`) so no trail is lost.

5. **Verify Repository Health**:
   * Run `bash verify_links.sh` and confirm all 7 checks pass with exit code `0`.
   * *(Optional)* Run `.agent/skills/review_article/SKILL.md` to perform a full Reader Mode, Subject Matter Expert, and Technical Architect review and link a `0–10` Before/After report under `reviews/<category>/<slug>-review.md`.

## Example

**User:** "Create an article about the new React compiler from this link..."

**Action:**
1. Read URL.
2. Write `articles/frontend/react-compiler-overview.md` with `**Date:** Month Day, Year` at the top and a `## Related Articles` footer.
3. Prepend the article to `* **Recent Additions (7-Day Window, Min 3 / Max 5):**` in `README.md`, keeping all entries within 7 days of the latest date (min 3, max 5) and noting any evicted entry.
4. Remove `[NEW]` only from any evicted entry in `articles/README.md`, and add the new entry under `### Frontend`:
   `- [React Compiler Overview](frontend/react-compiler-overview.md) [NEW]`
5. Update counts in `articles/README.md` and `README.md`, then run `bash verify_links.sh` (Checks 1–7 pass).
