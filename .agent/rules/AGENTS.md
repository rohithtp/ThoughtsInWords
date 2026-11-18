# ThoughtsInWords Repository Governance Rules

This rule governs all article authoring, updating, simplification, multi-persona review, and index reconciliation workflows in **ThoughtsInWords**.

## Invariant 1 — Pure Open-Source Systems Mandate & `Scope & Licensing Note`

* When an article covers tools, libraries, frameworks, platforms, or software architectures, include **only pure open-source systems** governed by OSI-approved open-source licenses with the full feature set self-hostable and free of vendor lock-in or paywalled tiers.
* **Exclude:** Premium/commercial-only systems, proprietary/vendor-locked systems, and community-based/open-core ("Community Edition") systems. Omit or replace non-qualifying systems in prose, tables, and diagrams with pure open-source equivalents (while preserving valid open standard/specification references).
* Qualifying articles covering systems or tooling **MUST** include this exact callout if not already stated:
  ```markdown
  > **Scope & Licensing Note:** This article strictly covers pure open-source systems. Premium, proprietary/vendor-locked, and community-edition (open-core) systems are currently not included.
  ```

## Invariant 2 — Directory Layout & `kebab-case.md` Naming

* Store articles inside an existing topic category folder at `articles/<category>/<kebab-case-slug>.md`. Never use date-based (`YYYY/MM/DD`) directories, uppercase letters, underscores (`_`), or empty directories.
* Store review reports at `reviews/<category>/<kebab-case-slug>-review.md`.

## Invariant 3 — Immutable Header Metadata & Bottom Section Ordering

* Every article **MUST** include `**Date:** Month Day, Year` at the top (e.g., `**Date:** November 18, 2026`). **Never** overwrite or alter the original `**Date:**` once published.
* Every subsequent edit **MUST** add or update `**Last Updated:** Month Day, Year` directly beneath `**Date:**`.
* Reviewed articles **MUST** include ``**Review:** [Expert & Architecture Review Report](../../reviews/<category>/<slug>-review.md)`` directly beneath the date headers.
* Bottom sections **MUST** appear in this exact order at the end of the file:
  1. `## Related Articles` — 2–3 relative `.md` links with brief connection notes.
  2. `## References` — (if present) existing citations, footnotes, and inline links must **never** be deleted.
  3. `## Changelog` — at the **very bottom**, in reverse chronological order (`- **Mon DD, YYYY:** <summary>`), seeded with `- **Mon DD, YYYY:** Initial publication.` matching `**Date:**` when created.

## Invariant 4 — Hybrid Window `[NEW]`, `[UPDATED]` Exclusivity & Trail Parity

* **Hybrid Window `[NEW]` Formula:** Keep `[NEW]` on all articles published within **7 days** of the newest article's `**Date:**`, bounded by a minimum of `3` and maximum of `5`: `expected_count = min(5, max(3, count_within_7_days))`.
* **`[UPDATED]` Exclusivity & Cap:** Maintain at most `5` revised entries under `* **Recently Updated (Revision Trail, Max 5):**` in [`README.md`](../../README.md) and [`articles/README.md`](../../articles/README.md). An article holding `[NEW]` must **never** simultaneously hold `[UPDATED]`.
* **1-to-1 Index & Changelog Parity:** `[NEW]`, `[UPDATED]`, and category/total article counts must match 1-to-1 between [`README.md`](../../README.md) and [`articles/README.md`](../../articles/README.md), and every lifecycle event (`Added`, `Updated`, `Simplified`, `Reviewed & Updated`, `Rotated (\`[NEW]\`)`) must be recorded under `### Month Day, Year` in [`articles/CHANGELOG.md`](../../articles/CHANGELOG.md) per [`organize_readme/SKILL.md`](../skills/organize_readme/SKILL.md).
* **Mandatory Verification Gate:** Every content or index mutation must pass `bash verify_links.sh` ([`verify_links.sh`](../../verify_links.sh) Checks 1–7 == exit code `0`).
