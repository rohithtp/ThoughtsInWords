---
name: Organize README
description: Scans the `articles/` directory for broken links, unlisted files, naming issues, or stale counts in `articles/README.md` and fixes them.
---

# Organize README (Single-Writer Index Reconciler)

This skill is the canonical **single-writer** owner for mutating `README.md`, `articles/README.md`, `articles/CHANGELOG.md`, and `reviews/README.md`. Backed by [`reconcile_indexes.py`](./scripts/reconcile_indexes.py), the `uv`-first / `pip`-fallback Python runner [`run_python.sh`](./scripts/run_python.sh), and [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md), it ensures index entries, category/total counts, Hybrid Window `[NEW]` / `[UPDATED]` cohorts, review rows, and changelog trails stay synchronized without multi-writer contention.

## Single-Writer Execution Engine (`reconcile_indexes.py`)

Content workflows (`create_article`, `update_article`, `simplify_article`, `review_article`) **must never edit singleton index files directly**. Instead, they restrict edits to target article files and pass a structured [`INDEX_HANDOFF_SCHEMA`](../review_article/scripts/schemas.py) payload to [`reconcile_indexes.py`](./scripts/reconcile_indexes.py) via [`run_python.sh`](./scripts/run_python.sh):

### 1. Handoff Mode (Called by Content Workflows)

Run with a single JSON object or JSON array of handoff payloads:

```bash
bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff '{
  "action": "Added",
  "article_path": "articles/<category>/<kebab-case-slug>.md",
  "title": "Article Title",
  "date": "November 19, 2026",
  "changelog_summary": "Concise summary of the addition or change"
}'
```

* Accepted `action` values: `"Added"`, `"Updated"`, `"Simplified"`, `"Reviewed & Updated"`.
* For `"Reviewed & Updated"`, include `"review_move": {"report_path": "reviews/<category>/<slug>-review.md", "before_score": 7.5, "after_score": 9.0, "delta": "+1.5", "review_date": "Nov 19, 2026"}`.
* When `"reciprocal_articles_touched"` is provided, `reconcile_indexes.py` verifies each touched sibling article exists on disk, synthesizes `"Updated"` handoffs for siblings carrying `**Last Updated:**` and `## Changelog`, promotes them into `[UPDATED]` (respecting `[NEW]` exclusivity), and logs their entries in `articles/CHANGELOG.md`.
* For batch runs (multiple concurrent scoped agents), pass `--handoff '[...]'` or `--handoff-file <path>` once at fan-in to reconcile all changes atomically.
* Run offline unit verification via `bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --self-test`.

### 2. Standalone Discovery & Audit Mode

When the user asks to `"organize readme"`, `"fix links"`, or `"update index"`:

1. **Run the Deterministic Reconciler:**
   ```bash
   bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py
   ```
   The script automatically:
   * Scans all `.md` files under `articles/` (excluding `articles/README.md` and `articles/CHANGELOG.md`) and enforces [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 2** (`articles/<category>/<kebab-case-slug>.md`, zero empty directories).
   * Inserts unlisted files alphabetically into `articles/README.md` (`- [Title](category/slug.md)`), self-heals uniquely moved article paths, and updates `## Organization` tree counts and `## Category Directory` totals.
   * Recomputes the exact **Hybrid Window `[NEW]`** cohort (`min(5, max(3, count_within_7_days))` anchored to the newest `**Date:**`) and top-5 **`[UPDATED]`** revision trail (**Invariant 4** exclusivity), enforcing 1-to-1 parity between `README.md` and `articles/README.md` and recording `* **Rotated (\`[NEW]\`):**` notices in `articles/CHANGELOG.md`.
   * Syncs unlisted `reviews/<category>/<slug>-review.md` reports into `reviews/README.md`.
   * Executes `bash verify_links.sh` (Checks 1–8) as its completion gate.

2. **LLM Fallback for Ambiguous Cross-Links or Deletions:**
   * If `verify_links.sh` reports Check 1/3 internal cross-link failures inside article bodies or deleted/ambiguous targets that cannot be auto-resolved by unique filename matching, inspect the reported files, repair the broken relative `.md` paths (or check `## Related Articles`), and re-run `bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py` until Checks 1–8 exit `0`.
