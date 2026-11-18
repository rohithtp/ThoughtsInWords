# 03 — Phased Migration Execution Plan

**Parent Index:** [Architectural Plans Index](./README.md) | **Previous:** [02 — Evaluation & Target Architecture](./02-skills-to-agents-evaluation-and-architecture.md)
**Assessment Role:** Technical / AI Architect

---

## Execution Roadmap Overview

| Phase | Priority & ROI | Scope | Primary Deliverables | Risk Level |
| :--- | :---: | :--- | :--- | :---: |
| **Phase 1** | `9.5 / 10` | Formalize [`review_article`](../.agent/skills/review_article/SKILL.md) multi-agent pipeline | 3 read-only reviewer agent specs + `run_review_workflow.py` + JSON Scorecard schema | **Low** |
| **Phase 2** | `8.5 / 10` | Shared rules & single-writer reconciliation | `.agent/rules/AGENTS.md` + `index-reconciler` agent replacing multi-writer index edits | **Low–Medium** |
| **Phase 3** | `8.0 / 10` | Scoped content agents & VCS verification gate | `article-author`, `article-refactor`, tool-agnostic cleanup, pre-push `verify_links.sh` gate | **Medium** |

---

## Phase 1: Formalize `review_article` as a Deterministic Multi-Agent Workflow

**Target Outcome:** Eliminate ad-hoc prompt synthesis and manual arithmetic in [`review_article`](../.agent/skills/review_article/SKILL.md) by moving Stages 1–4 into reusable read-only reviewer definitions orchestrated by `run_workflow`.

### Step-by-Step Tasks

1. **Create Persistent Read-Only Reviewer Definitions (`.agent/agents/`):**
   * `reader-mode-reviewer.md`: Owns Parameters 1–4 from [`rubric-and-repo-alignment.md`](../.agent/skills/review_article/references/rubric-and-repo-alignment.md); `EnableWriteTools: false`.
   * `subject-expert-reviewer.md`: Owns Parameters 5–8 (accuracy, failure modes, citations, pure open-source compliance); `EnableWriteTools: false`.
   * `technical-architect-reviewer.md`: Owns Parameters 9–12 (trade-offs, ThoughtsInWords philosophy & anti-oversimplification check, interconnectivity, metadata compliance); `EnableWriteTools: false`.
2. **Implement `.agent/skills/review_article/scripts/run_review_workflow.py`:**
   * **Stage 1 (`Before` Audit):** Use `parallel()` to invoke persistent `agent()` handles with `SCORECARD_SCHEMA` so all 3 personas return structured `0–10` scores and prioritized recommendations (`Critical`, `High`, `Medium`, `Low`).
   * **Stage 2 & 3 (Remediation):** Merge recommendations and pass them to the remediator turn to update `articles/<category>/<slug>.md` (preserving `**Date:**`, updating `**Last Updated:**`, adding `**Review:**` link, ensuring `Scope & Licensing Note`, prepending `## Changelog`).
   * **Stage 4 (`After` Re-Verification):** Reuse the **same 3 persistent agent handles** (`await r1(after_prompt)`, `await r2(after_prompt)`, `await r3(after_prompt)`) to score the revised article against Stage 1 findings.
   * **Deterministic Score Math:** Compute Persona Sub-Averages, Overall Composite Score, and exact Deltas (`After - Before`) in Python, and render `reviews/<category>/<slug>-review.md` using [`report-template.md`](../.agent/skills/review_article/resources/report-template.md).
3. **Update `.agent/skills/review_article/SKILL.md`:** Point the skill directly to `run_review_workflow.py` via `run_workflow`.

### Phase 1 Acceptance Criteria
* Running `review_article` on a sample article produces a valid `SCORECARD_SCHEMA` payload for all 3 personas (Before and After) with zero manual score arithmetic errors.
* `bash verify_links.sh` Check 7 passes with exit code `0`.

---

## Phase 2: Centralize Rules & Deploy Single-Writer `index-reconciler`

**Target Outcome:** Remove duplicated governance rules from individual skills and eliminate race conditions on singleton index/changelog files.

### Step-by-Step Tasks

1. **Create `.agent/rules/AGENTS.md`:**
   * Consolidate the **Pure Open-Source Systems Mandate** and exact `Scope & Licensing Note` callout.
   * Consolidate the **`kebab-case.md` naming rule** and topic-directory policy (no date-based folders, no empty directories).
   * Consolidate the **immutable `**Date:**` header**, `**Last Updated:**`, and bottom `## Changelog` ordering contract.
   * Consolidate the **Hybrid Window `[NEW]` policy** (`min(5, max(3, count_within_7_days))`) and **`[UPDATED]` exclusivity** (max 5, never combined with `[NEW]`).
2. **Define `.agent/agents/index-reconciler.md` (Model Tier: `flash`):**
   * Owns all edits to [`README.md`](../README.md), [`articles/README.md`](../articles/README.md), [`articles/CHANGELOG.md`](../articles/CHANGELOG.md), and [`reviews/README.md`](../reviews/README.md).
   * Accepts a list of structured JSON handoff payloads from upstream content agents (or runs full discovery when invoked standalone via [`organize_readme`](../.agent/skills/organize_readme/SKILL.md)).
   * Resolves broken relative cross-links, verifies 1-to-1 `[NEW]` and `[UPDATED]` badge parity, updates category/total counts, and executes `bash verify_links.sh` as its mandatory completion gate.
3. **Update `.agent/skills/organize_readme/SKILL.md`:** Convert into a thin routing skill delegating reconciliation to `index-reconciler`.

### Phase 2 Acceptance Criteria
* Two simulated concurrent article handoffs processed through `index-reconciler` produce accurate counts, zero duplicate or missing `[NEW]`/`[UPDATED]` badges, and exit code `0` from `bash verify_links.sh` (Checks 1–7).
* All subagents automatically respect repository invariants via `.agent/rules/AGENTS.md` without inline prompt repetition.

---

## Phase 3: Scope Content Agents & Guard `commit_and_push`

**Target Outcome:** Complete the Hybrid Control Plane by isolating article authoring/refactoring into scoped subagents and securing the Jujutsu (`jj`) publication path.

### Step-by-Step Tasks

1. **Create `.agent/agents/article-author.md` (from [`create_article`](../.agent/skills/create_article/SKILL.md)):**
   * Scoped strictly to creating `articles/<category>/<kebab-case>.md` (and optional reciprocal cross-links in existing articles) and returning the JSON handoff payload to `index-reconciler`.
   * Keep URL ingestion and heavy synthesis isolated from the main user conversation.
2. **Create `.agent/agents/article-refactor.md` (from [`simplify_article`](../.agent/skills/simplify_article/SKILL.md)):**
   * Scoped strictly to structural cleanup, header hierarchy normalization, Mermaid flow injection, and **100% link/citation retention verification**, returning the JSON handoff payload to `index-reconciler`.
   * Remove the legacy tool reference (`view_file` on line 16 of [`simplify_article/SKILL.md`](../.agent/skills/simplify_article/SKILL.md)) in favor of tool-agnostic wording.
   * Use `workspace: "share"` when invoked across batches of multiple articles in parallel.
3. **Update [`update_article/SKILL.md`](../.agent/skills/update_article/SKILL.md):**
   * Retain as a lightweight hybrid skill for single-section edits in the active conversation, while routing index/badge updates through `index-reconciler` (or delegating multi-article cross-link updates to a subagent).
4. **Add Pre-Push Gate to [`commit_and_push/SKILL.md`](../.agent/skills/commit_and_push/SKILL.md):**
   * Keep `commit_and_push` as a Skill (`2.0 / 10` conversion ROI—no subagent needed).
   * Insert mandatory **Step 0: Verify Repository Health** (`bash verify_links.sh` must exit `0`) and confirm `jj status` before `jj describe -m`, `jj bookmark set main -r @`, and `jj git push`.
5. **Sync Documentation:** Update [`.agent/skills/README.md`](../.agent/skills/README.md) to reflect the active `.agent/agents/` and `.agent/rules/` components once each phase ships.

### Phase 3 Acceptance Criteria
* End-to-end smoke test (`article-author` → `run_review_workflow.py` → `index-reconciler` → `verify_links.sh` → `commit_and_push` dry run) executes with zero manual index edits and passes Checks 1–7.
* Batch refactoring via `article-refactor` with `workspace: "share"` executes without working-copy conflicts.
