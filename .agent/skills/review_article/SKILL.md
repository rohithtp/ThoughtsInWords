---
name: Review and Verify Article
description: Verify, critique, improve, and rate an article on a 0-10 scale (Before and After) using a multi-subagent pipeline (Reader Mode, Subject Matter Expert, and Technical Architect / Repo Concept Reviewer), apply recommended changes, and generate a linked report in reviews/<category>/<slug>-review.md.
---

# Review and Verify Article

This skill orchestrates a schema-validated, stateful multi-persona verification, architectural audit, and continuous-improvement pipeline for any article in **ThoughtsInWords** (Option B4 + Option A4). It executes [`run_review_workflow.py`](./scripts/run_review_workflow.py) via `run_workflow`, enforcing dual JSON Schema contracts (`BEFORE_SCORECARD_SCHEMA` and `AFTER_SCORECARD_SCHEMA` in [`schemas.py`](./scripts/schemas.py)), deterministic Python score/delta arithmetic, and single-writer index reconciliation via [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py).

## Prerequisites & Supporting Artifacts

* Repository governance invariants: [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md)
* Evaluation rubric & philosophy alignment rules: [`rubric-and-repo-alignment.md`](./references/rubric-and-repo-alignment.md)
* Canonical report template: [`report-template.md`](./resources/report-template.md)
* JSON Schemas, anti-inflation clamp & Check 7 renderer: [`schemas.py`](./scripts/schemas.py)
* Deterministic `run_workflow` orchestrator: [`run_review_workflow.py`](./scripts/run_review_workflow.py)
* Single-writer reconciler: [`reconcile_indexes.py`](../organize_readme/scripts/reconcile_indexes.py)

---

## Primary Execution Path (`run_workflow`)

Run the deterministic pipeline directly using `run_workflow` with the `runpy.run_path` bootstrapper and target `article_path`:

```python
run_workflow(
    Script=(
        "import runpy\n"
        "mod = runpy.run_path('.agent/skills/review_article/scripts/run_review_workflow.py', init_globals=globals())\n"
        "await mod['run_pipeline'](globals())\n"
    ),
    Args={"article_path": "articles/<category>/<slug>.md"},
    Description="Run 5-stage schema-validated multi-persona article review",
)
```

### Pipeline Stages Executed by `run_review_workflow.py`

1. **Stage 1 — Stateful Read-Only "Before" Audit (`parallel` + `BEFORE_SCORECARD_SCHEMA`):**
   * Creates three persistent read-only reviewer handles (`r_reader` Params 1–4, `r_sme` Params 5–8, `r_arch` Params 9–12) and invokes them concurrently via `parallel()`.
   * Each reviewer evaluates [`rubric-and-repo-alignment.md`](./references/rubric-and-repo-alignment.md), [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) (including **Invariant 1** Pure Open-Source Systems Mandate), `README.md` philosophy alignment (guarding against the *Engineer's Philosophy* pitfall), and `articles/README.md` cross-links, returning strict `BEFORE_SCORECARD_SCHEMA` JSON with `R-XX` / `S-XX` / `A-XX` recommendation IDs.

2. **Stage 2 & 3 — Scoped Synthesis & Article Remediation (`REMEDIATION_RESULT_SCHEMA`):**
   * Python sorts all Stage 1 recommendations by priority (`Critical`, `High`, `Medium`, `Low`) and launches a scoped `Article Remediator` turn.
   * **Single-Writer Partitioning (Option A4):** The remediator mutates **only** `articles/<category>/<slug>.md`—preserving immutable `**Date:**`, updating `**Last Updated:**`, adding `**Review:** [Expert & Architecture Review Report](../../reviews/<category>/<slug>-review.md)`, applying prioritized fixes, enforcing `Scope & Licensing Note`, preserving `## References` and links, ordering bottom sections per **Invariant 3**, and prepending to `## Changelog`.

3. **Stage 4 — Multi-Turn "After" Re-Verification & Deterministic Report Rendering (`AFTER_SCORECARD_SCHEMA`):**
   * Sends the revised article back to the **same three persistent handles** (`r_reader`, `r_sme`, `r_arch`) via `parallel()` so Stage 4 verification retains full memory of Stage 1 deductions and validates every `R-XX` / `S-XX` / `A-XX` item (`Applied` vs. `Deferred`).
   * `compute_scorecard()` in [`schemas.py`](./scripts/schemas.py) enforces anti-inflation clamping (holding `After <= Before` if all recommendations for a parameter remained `Deferred`), computes exact Persona Sub-Averages, Overall Composite Scores, and Deltas in Python, and `render_review_report()` writes `reviews/<category>/<slug>-review.md` matching [`report-template.md`](./resources/report-template.md).

4. **Stage 5 — Single-Writer Index Reconciliation & Verification Gate (`INDEX_HANDOFF_SCHEMA`):**
   * Emits a validated `INDEX_HANDOFF_SCHEMA` payload (`action: "Reviewed & Updated"`, including `review_move` scores/delta) to:
     ```bash
     bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff '<json>'
     ```
   * Updates `reviews/README.md`, syncs `README.md`, `articles/README.md`, and `articles/CHANGELOG.md` without multi-writer contention, and confirms `bash verify_links.sh` (Checks 1–8) passes with exit code `0`.

## Validation Self-Tests

Before modifying schemas, workflow orchestration, or templates, run (via [`run_python.sh`](../organize_readme/scripts/run_python.sh) `uv` → `pip` runner):
```bash
bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/review_article/scripts/schemas.py --self-test
bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/review_article/scripts/run_review_workflow.py --self-test
```
