# Architectural Plans: Agent Skills & Skill-to-Agent Migration

Welcome to the `plan/` directory for **ThoughtsInWords** ([Root Overview](../README.md) | [Skills Capability Index](../.agent/skills/README.md) | [Full Article Index](../articles/README.md) | [Review Reports Index](../reviews/README.md)).

This folder captures the complete Technical / AI Architect assessment (`0–10` scale) of the repository's `.agent/skills/` control plane, the architectural blueprint for converting procedural skills into isolated subagents and `run_workflow` pipelines, and the phased execution roadmap.

---

## Plan Documents Index

| Order | Document | Scope & Focus | Key Outputs | Status |
| :-: | :--- | :--- | :--- | :--- |
| **01** | [Skills Capability & Scale Assessment](./01-skills-capability-and-scale-assessment.md) | Prompt evaluation (`0–10`), 8-parameter AI/technical scale requirements, and current maturity scorecard of all 6 skills | Prompt `4.2 → 9.2` refinement, `0–10` scale matrix, Options 4 + A4/B4 remediations (`review_article` `9.7`, `organize_readme` `9.5`) | Implemented (Options 4, A4 & B4) |
| **02** | [Skills-to-Agents Evaluation & Target Architecture](./02-skills-to-agents-evaluation-and-architecture.md) | Paradigm comparison, 6-parameter conversion ROI (`0–10`), Option A1–A4 & B1–B4 `0–10` trade-off matrices, and hybrid topology | Conversion ROI (`9.5` to `2.0`), Option A4 (`9.6`) & Option B4 (`9.7`) matrices, live schemas & Mermaid topology | Implemented (Options 4, A4 & B4) |
| **03** | [Phased Migration Execution Plan](./03-phased-migration-execution-plan.md) | Actionable 3-phase implementation plan, file deliverables, invariants migration, and verification gates | Phase 1 (`schemas.py` + `run_review_workflow.py` **Done**), Phase 2 (`.agent/rules/AGENTS.md` + `reconcile_indexes.py` **Done**), Phase 3 (`prepare_commit.sh` + scoped content handoffs **Done**) | Implemented (Options 4, A4 & B4) |

---

## Executive Architectural Summary

1. **Do not convert skills 1-to-1 into unconstrained write-enabled agents.** Converting all 6 skills into independent agents that mutate singleton indexes ([`README.md`](../README.md), [`articles/README.md`](../articles/README.md), [`articles/CHANGELOG.md`](../articles/CHANGELOG.md), [`reviews/README.md`](../reviews/README.md)) introduces write contention and badge-rotation drift.
2. **Adopt a Hybrid Control Plane (Thin Routing Skills + Scoped Workflows + Script-Backed Single-Writer Reconciler):**
   * **High ROI (`9.7 / 10` — Option B4):** [`review_article`](../.agent/skills/review_article/SKILL.md) runs via [`run_review_workflow.py`](../.agent/skills/review_article/scripts/run_review_workflow.py) with 3 stateful read-only reviewer handles across Stage 1 (`BEFORE_SCORECARD_SCHEMA`) and Stage 4 (`AFTER_SCORECARD_SCHEMA`), deterministic Python math/Check 7 rendering, and anti-inflation clamping in [`schemas.py`](../.agent/skills/review_article/scripts/schemas.py).
   * **Concurrency Safety (`9.6 / 10` — Option A4):** [`organize_readme`](../.agent/skills/organize_readme/SKILL.md) executes via the deterministic single-writer [`reconcile_indexes.py`](../.agent/skills/organize_readme/scripts/reconcile_indexes.py), consuming validated `INDEX_HANDOFF_SCHEMA` payloads to own all index, badge, review table, and changelog mutations and running [`verify_links.sh`](../verify_links.sh).
   * **Scoped Authoring (`8.8–8.9 / 10` — Option A4):** [`create_article`](../.agent/skills/create_article/SKILL.md), [`simplify_article`](../.agent/skills/simplify_article/SKILL.md), and [`update_article`](../.agent/skills/update_article/SKILL.md) restrict mutations strictly to article files and hand off `INDEX_HANDOFF_SCHEMA` payloads to [`reconcile_indexes.py`](../.agent/skills/organize_readme/scripts/reconcile_indexes.py).
   * **Keep as Guarded Skill (`2.0 / 10` ROI — Option 4):** Keep [`commit_and_push`](../.agent/skills/commit_and_push/SKILL.md) as a two-phase procedural skill gated by [`prepare_commit.sh`](../.agent/skills/commit_and_push/scripts/prepare_commit.sh) (`bash verify_links.sh` Checks 1–8 before `jj describe`, `jj bookmark set`, and `jj git push --bookmark`).
   * **IDE & `uv`/`pip` Dependency Integrity (Strategy S4):** [`run_review_workflow.py`](../.agent/skills/review_article/scripts/run_review_workflow.py) runs as a standard-Python module (via `runpy.run_path` inside `run_workflow` + offline mock `--self-test`), paired with [`pyproject.toml`](../pyproject.toml), [`requirements.txt`](../requirements.txt), [`pyrightconfig.json`](../pyrightconfig.json), [`.gitignore`](../.gitignore) Python ignores, [`run_python.sh`](../.agent/skills/organize_readme/scripts/run_python.sh) (`uv` primary / `pip` fallback), and `verify_links.sh` Check 8.
