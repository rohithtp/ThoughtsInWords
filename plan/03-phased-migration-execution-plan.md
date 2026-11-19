# 03 — Phased Migration Execution Plan

**Parent Index:** [Architectural Plans Index](./README.md) | **Previous:** [02 — Evaluation & Target Architecture](./02-skills-to-agents-evaluation-and-architecture.md)
**Assessment Role:** Technical / AI Architect

---

## Execution Roadmap Overview

| Phase | Priority & ROI | Scope | Primary Deliverables | Risk Level |
| :--- | :---: | :--- | :--- | :---: |
| **Phase 1** | `9.5 / 10` | Formalize [`review_article`](../.agent/skills/review_article/SKILL.md) multi-agent pipeline | [`schemas.py`](../.agent/skills/review_article/scripts/schemas.py) (`BEFORE_SCORECARD_SCHEMA` / `AFTER_SCORECARD_SCHEMA`) + [`run_review_workflow.py`](../.agent/skills/review_article/scripts/run_review_workflow.py) *(Implemented — Option B4)* | **Low** |
| **Phase 2** | `8.5 / 10` | Shared rules & single-writer reconciliation | [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md) + `SKILL.md` deduplication *(Completed — Option 4)*; [`reconcile_indexes.py`](../.agent/skills/organize_readme/scripts/reconcile_indexes.py) + `INDEX_HANDOFF_SCHEMA` *(Implemented — Option A4)* | **Low–Medium** |
| **Phase 3** | `8.0 / 10` | Scoped content agents & VCS verification gate | Single-writer content skill partitioning (`create_article`, `update_article`, `simplify_article`) + pre-push [`prepare_commit.sh`](../.agent/skills/commit_and_push/scripts/prepare_commit.sh) *(Implemented — Options 4 + A4)*; optional standalone `.agent/agents/*.md` files *(Optional)* | **Medium** |

---

## Phase 1: Formalize `review_article` as a Deterministic Multi-Agent Workflow *(Implemented — Option B4)*

**Target Outcome:** Eliminate ad-hoc prompt synthesis and manual arithmetic in [`review_article`](../.agent/skills/review_article/SKILL.md) by orchestrating persistent read-only reviewer handles via `run_workflow` and schema-validated Python math/rendering.

### Step-by-Step Tasks

1. **Implement [`schemas.py`](../.agent/skills/review_article/scripts/schemas.py) *(Implemented)*:**
   * Defines Draft-07 compatible `BEFORE_SCORECARD_SCHEMA` (with `R-XX` / `S-XX` / `A-XX` recommendation IDs), `REMEDIATION_RESULT_SCHEMA`, `AFTER_SCORECARD_SCHEMA` (`Applied` vs. `Deferred`), and `INDEX_HANDOFF_SCHEMA`.
   * Implements `compute_scorecard()` with anti-inflation clamping (holding `After <= Before` if all linked Stage 1 recommendations remain `Deferred`), deterministic Python means/deltas, and `render_review_report()` generating Check 7 compliant Markdown from [`report-template.md`](../.agent/skills/review_article/resources/report-template.md).
2. **Implement [`run_review_workflow.py`](../.agent/skills/review_article/scripts/run_review_workflow.py) *(Implemented)*:**
   * **Stage 1 (`Before` Audit):** Instantiates 3 persistent read-only handles (`r_reader`, `r_sme`, `r_arch`) and executes `parallel()` with `BEFORE_SCORECARD_SCHEMA`.
   * **Stage 2 & 3 (Scoped Remediation):** Sorts prioritized findings and runs `Article Remediator` (`REMEDIATION_RESULT_SCHEMA`) scoped strictly to `articles/<category>/<slug>.md` (preserving `**Date:**`, adding `**Last Updated:**`, `**Review:**` link, `Scope & Licensing Note`, and bottom `## Changelog`).
   * **Stage 4 (`After` Re-Verification):** Reuses the **same 3 persistent handles** via `parallel()` against `AFTER_SCORECARD_SCHEMA`, computes exact scorecard math and renders `reviews/<category>/<slug>-review.md` in Python.
   * **Stage 5 (Single-Writer Handoff):** Emits `INDEX_HANDOFF_SCHEMA` to [`reconcile_indexes.py`](../.agent/skills/organize_readme/scripts/reconcile_indexes.py).
3. **Update [`review_article/SKILL.md`](../.agent/skills/review_article/SKILL.md) *(Implemented)*:** Points the skill directly to `run_review_workflow.py` via `run_workflow`.

### Phase 1 Acceptance Criteria
* `python3 .agent/skills/review_article/scripts/schemas.py --self-test` verifies schema contracts, anti-inflation clamping, arithmetic, and Check 7 heading integrity (`exit 0`).
* `bash verify_links.sh` Check 7 passes with exit code `0`.

---

## Phase 2: Centralize Rules & Deploy Single-Writer `reconcile_indexes.py` *(Implemented — Options 4 + A4)*

**Target Outcome:** Remove duplicated governance rules from individual skills and eliminate race conditions on singleton index/changelog files.

### Step-by-Step Tasks

1. **Create `.agent/rules/AGENTS.md` & Deduplicate `SKILL.md` Governance *(Completed — Option 4)*:**
   * Consolidated the **Pure Open-Source Systems Mandate** and exact `Scope & Licensing Note` callout, **`kebab-case.md` naming**, **immutable `**Date:**` / `**Last Updated:**` / bottom `## Changelog` ordering**, and **Hybrid Window `[NEW]` / `[UPDATED]` exclusivity** into [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md).
   * Consolidated procedural `README.md`, `articles/README.md`, and `articles/CHANGELOG.md` trail updates into [`organize_readme/SKILL.md`](../.agent/skills/organize_readme/SKILL.md) and deduplicated [`create_article`](../.agent/skills/create_article/SKILL.md), [`update_article`](../.agent/skills/update_article/SKILL.md), [`simplify_article`](../.agent/skills/simplify_article/SKILL.md), and [`review_article`](../.agent/skills/review_article/SKILL.md).
2. **Implement [`reconcile_indexes.py`](../.agent/skills/organize_readme/scripts/reconcile_indexes.py) *(Implemented — Option A4)*:**
   * Single-writer deterministic engine owning all edits to [`README.md`](../README.md), [`articles/README.md`](../articles/README.md), [`articles/CHANGELOG.md`](../articles/CHANGELOG.md), and [`reviews/README.md`](../reviews/README.md).
   * Accepts `--handoff` / `--handoff-file` (`INDEX_HANDOFF_SCHEMA` object or array) or runs standalone tree discovery.
   * Inserts unlisted articles alphabetically, self-heals uniquely moved paths, computes Hybrid Window `[NEW]` and top-5 `[UPDATED]` cohorts, updates all counts, records idempotent `articles/CHANGELOG.md` entries, and executes `bash verify_links.sh` as its completion gate.
3. **Update [`organize_readme/SKILL.md`](../.agent/skills/organize_readme/SKILL.md) *(Implemented)*:** Configured around `reconcile_indexes.py` handoff and standalone modes with LLM fallback for ambiguous broken cross-links.

### Phase 2 Acceptance Criteria
* `python3 .agent/skills/organize_readme/scripts/reconcile_indexes.py --dry-run` and live execution pass idempotently (`exit 0`) with zero unintended diffs and `verify_links.sh` Checks 1–7 == `0`.
* All subagents and workflows inherit repository invariants via `.agent/rules/AGENTS.md`.

---

## Phase 3: Scope Content Workflows & Guard `commit_and_push` *(Core Implemented — Options 4 + A4)*

**Target Outcome:** Partition content workflows so they mutate only target article files, hand off indexes via `INDEX_HANDOFF_SCHEMA`, and secure the Jujutsu (`jj`) publication path.

### Step-by-Step Tasks

1. **Scope [`create_article/SKILL.md`](../.agent/skills/create_article/SKILL.md) *(Implemented — Option A4)*:**
   * Restricted writes strictly to `articles/<category>/<kebab-case>.md` (and optional reciprocal cross-links) with `INDEX_HANDOFF_SCHEMA` (`"Added"`) handoff to `reconcile_indexes.py`. *(Optional future extension: `.agent/agents/article-author.md` wrapper.)*
2. **Scope [`simplify_article/SKILL.md`](../.agent/skills/simplify_article/SKILL.md) *(Implemented — Options 4 + A4)*:**
   * Tool-agnostic structural cleanup preserving 100% of links/citations, supporting parallel batches via `workspace: "share"` merged at fan-in via `--handoff '[...]'` to `reconcile_indexes.py`. *(Optional future extension: `.agent/agents/article-refactor.md` wrapper.)*
3. **Scope [`update_article/SKILL.md`](../.agent/skills/update_article/SKILL.md) *(Implemented — Option A4)*:**
   * Restricted writes to target article edits with `INDEX_HANDOFF_SCHEMA` (`"Updated"`) handoff to `reconcile_indexes.py`.
4. **Add Pre-Push Gate to [`commit_and_push/SKILL.md`](../.agent/skills/commit_and_push/SKILL.md) *(Completed — Option 4)*:**
   * Kept `commit_and_push` as a Skill (`2.0 / 10` conversion ROI—no subagent needed).
   * Added atomic local staging script [`prepare_commit.sh`](../.agent/skills/commit_and_push/scripts/prepare_commit.sh) (`set -euo pipefail`) that enforces `bash verify_links.sh` (Checks 1–7 == exit `0`) **before** `jj describe -m` and `jj bookmark set <bookmark> -r @` (default `main`), isolating network access strictly to Phase 2 (`jj git push --bookmark <bookmark>`) and routing Check 1–7 failures to [`organize_readme`](../.agent/skills/organize_readme/SKILL.md).
5. **Sync Documentation *(Implemented)*:** Updated [`.agent/skills/README.md`](../.agent/skills/README.md) and [`plan/`](./README.md) for `.agent/rules/AGENTS.md`, `prepare_commit.sh`, `reconcile_indexes.py`, `schemas.py`, and `run_review_workflow.py`.

### Phase 3 Acceptance Criteria
* `schemas.py --self-test`, `reconcile_indexes.py`, AST/syntax checks, and `bash verify_links.sh` (Checks 1–7) all pass with exit code `0`.
* Batch refactoring via `simplify_article` with `workspace: "share"` merges cleanly via `--handoff '[...]'` to `reconcile_indexes.py` without singleton contention.
