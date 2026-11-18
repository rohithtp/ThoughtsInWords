# Architectural Plans: Agent Skills & Skill-to-Agent Migration

Welcome to the `plan/` directory for **ThoughtsInWords** ([Root Overview](../README.md) | [Skills Capability Index](../.agent/skills/README.md) | [Full Article Index](../articles/README.md) | [Review Reports Index](../reviews/README.md)).

This folder captures the complete Technical / AI Architect assessment (`0–10` scale) of the repository's `.agent/skills/` control plane, the architectural blueprint for converting procedural skills into isolated subagents and `run_workflow` pipelines, and the phased execution roadmap.

---

## Plan Documents Index

| Order | Document | Scope & Focus | Key Outputs | Status |
| :-: | :--- | :--- | :--- | :--- |
| **01** | [Skills Capability & Scale Assessment](./01-skills-capability-and-scale-assessment.md) | Prompt evaluation (`0–10`), 8-parameter AI/technical scale requirements, and current maturity scorecard of all 6 skills | Prompt `4.2 → 9.2` refinement, `0–10` scale matrix, Option 4 governance & pre-push remediations | Updated (Option 4) |
| **02** | [Skills-to-Agents Evaluation & Target Architecture](./02-skills-to-agents-evaluation-and-architecture.md) | Paradigm comparison, 6-parameter conversion ROI (`0–10`), 6 required architectural changes, and hybrid topology | Conversion ROI scores (`9.5` down to `2.0`), JSON contracts, Mermaid architecture (`AGENTS.md` + `prepare_commit.sh` live) | In Progress |
| **03** | [Phased Migration Execution Plan](./03-phased-migration-execution-plan.md) | Actionable 3-phase implementation plan, file deliverables, invariants migration, and verification gates | Phase 1 (`review_article`), Phase 2 (`.agent/rules/AGENTS.md` **Done**; `index-reconciler` pending), Phase 3 (`prepare_commit.sh` & cleanup **Done**; content agents pending) | Partially Implemented |

---

## Executive Architectural Summary

1. **Do not convert skills 1-to-1 into unconstrained write-enabled agents.** Converting all 6 skills into independent agents that mutate singleton indexes ([`README.md`](../README.md), [`articles/README.md`](../articles/README.md), [`articles/CHANGELOG.md`](../articles/CHANGELOG.md), [`reviews/README.md`](../reviews/README.md)) introduces write contention and badge-rotation drift.
2. **Adopt a Hybrid Control Plane (Thin Routing Skills + Scoped Agents + Single-Writer Reconciler):**
   * **High ROI (`9.5 / 10`):** Convert [`review_article`](../.agent/skills/review_article/SKILL.md) into 3 persistent read-only reviewer agents orchestrated via `run_workflow` with strict JSON Schema validation (`SCORECARD_SCHEMA`).
   * **Concurrency Safety (`8.5 / 10`):** Convert [`organize_readme`](../.agent/skills/organize_readme/SKILL.md) into a single-writer **`index-reconciler`** agent (`flash` tier) owning all index, badge, and changelog mutations and running [`verify_links.sh`](../verify_links.sh).
   * **Scoped Authoring (`7.5–8.0 / 10`):** Scope [`create_article`](../.agent/skills/create_article/SKILL.md), [`simplify_article`](../.agent/skills/simplify_article/SKILL.md), and batch [`update_article`](../.agent/skills/update_article/SKILL.md) subagents to article files only, emitting JSON handoff payloads to `index-reconciler`.
   * **Keep as Guarded Skill (`2.0 / 10`):** Keep [`commit_and_push`](../.agent/skills/commit_and_push/SKILL.md) as a two-phase procedural skill gated by [`prepare_commit.sh`](../.agent/skills/commit_and_push/scripts/prepare_commit.sh) (`bash verify_links.sh` Checks 1–7 before `jj describe`, `jj bookmark set`, and `jj git push --bookmark`) *(Implemented)*.
