# 01 — Skills Capability & Scale Assessment (`0–10`)

**Parent Index:** [Architectural Plans Index](./README.md) | **Control Plane:** [`.agent/skills/README.md`](../.agent/skills/README.md)
**Assessment Role:** Technical / AI Architect

---

## 1. Architectural Evaluation of the Capability Request (`0–10` Raw vs. Refined Spec)

Evaluating the initial problem statement (*"review the skills and create a readme about capabilities in skills folder"*) across 6 architectural specification parameters establishes why simple file listing is insufficient and defines the target specification implemented in [`.agent/skills/README.md`](../.agent/skills/README.md).

| # | Architecture Parameter | Raw Statement (`0–10`) | Refined Spec (`0–10`) | Architectural Gap & Clarification Applied |
| :-: | :--- | :---: | :---: | :--- |
| **1** | **Scope Boundary Precision** | `4.0` | `9.5` | *"skills folder"* could ambiguously refer to global plugin skills or workspace skills. Scoped strictly to the 6 skills (8 Markdown files + 1 gate script; `539` baseline lines, `486` lines post-Option 4 deduplication) inside `.agent/skills/` plus [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md). |
| **2** | **Dual-Audience Definition** | `5.0` | `9.0` | Needed explicit framing for both **human maintainers** (workflows, governance, VCS rules) and **AI agents** (intent triggers, preconditions, mutated targets). |
| **3** | **Lifecycle & DAG Topology Coverage** | `4.5` | `9.0` | Listing skills in isolation omits how `create_article`, `update_article`, `simplify_article`, and `review_article` converge on `organize_readme` and [`verify_links.sh`](../verify_links.sh). Modeled via a Mermaid `flowchart TD`. |
| **4** | **Governance & Invariant Surface** | `3.5` | `9.5` | Needed explicit capture of shared contracts: Pure Open-Source Systems Mandate, Hybrid Window `[NEW]` math, `[UPDATED]` mutual exclusivity, and the 12-parameter `0–10` rubric. |
| **5** | **Verification Contract** | `3.0` | `9.5` | Bound documentation accuracy to automated link resolution (29 links checked in `.agent/skills/README.md`) and [`verify_links.sh`](../verify_links.sh) (Checks 1–7). |
| **6** | **Schema & Extensibility** | `5.0` | `8.5` | Standardized capability routing tables, frontmatter triggers, directory tree layout, and scoring criteria for onboarding future skills. |
| — | **Composite Prompt Readiness** | **`4.2`** | **`9.2`** | **`+5.0` delta** after architectural refinement. |

---

## 2. Scale Required Across Technical & AI System Parameters (`0–10`)

Before modifying or automating the skills control plane, the system requirements are quantified on a `0.0–10.0` scale across 8 dimensions:

| # | System Parameter | Scale Required (`0–10`) | Engineering & AI Architecture Rationale |
| :-: | :--- | :---: | :--- |
| **1** | **Discovery & Context Window Scale** | `2.5` | Bounded workspace surface: 1 rule file (`.agent/rules/AGENTS.md`, 34 lines) + 6 skill directories (8 Markdown files + 1 gate script, 486 lines post-Option 4)—easily read in a single context pass without RAG or chunking. |
| **2** | **Agentic Compute & Orchestration Scale** | `2.0` / `7.5` | `2.0` for static README synthesis; peaks at `7.5` at runtime inside [`review_article`](../.agent/skills/review_article/SKILL.md), which spawns 3 parallel independent subagents and re-verifies **After** scores. |
| **3** | **State Mutation & Blast Radius Scale** | `1.5` / `8.0` | `1.5` for authoring `.agent/skills/README.md`; `8.0` across the documented skills that mutate articles, root/category/review indexes, changelogs, and remote `jj` bookmarks. |
| **4** | **Cross-Skill Dependency & DAG Coupling Scale** | `8.0` | High workflow coupling: [`create_article`](../.agent/skills/create_article/SKILL.md), [`update_article`](../.agent/skills/update_article/SKILL.md), [`simplify_article`](../.agent/skills/simplify_article/SKILL.md), and [`review_article`](../.agent/skills/review_article/SKILL.md) share badge exclusivity, changelog sync, and index contracts enforced by [`organize_readme`](../.agent/skills/organize_readme/SKILL.md) and [`verify_links.sh`](../verify_links.sh). |
| **5** | **Governance & Repository Invariant Scale** | `9.0` | Strict invariant surface: Hybrid Window `[NEW]` formula `min(5, max(3, count_within_7_days))`, `[UPDATED]` exclusivity (max 5), Pure Open-Source Systems mandate, immutable `**Date:**`, and a 12-parameter `0–10` rubric. |
| **6** | **Verification & Deterministic Gate Scale** | `8.5` | Backed by a deterministic Python validation suite inside [`verify_links.sh`](../verify_links.sh) running Checks 1–7 across all articles, indexes, cross-links, and review reports. |
| **7** | **Documentation Depth & Dual-Audience Ergonomics** | `8.0` | Must provide fast intent-routing tables for AI agents while maintaining clear architectural and governance explanations for human maintainers. |
| **8** | **Operational Maintenance & Drift-Prevention Scale** | `6.5` | Low churn, but changes to badge rules, rubric weights, or `verify_links.sh` checks require synchronized updates across skills, plans, and `.agent/skills/README.md`. |

---

## 3. Architectural Maturity Scorecard of Existing Skills (`0–10`)

Each of the 6 skills currently in `.agent/skills/` is assessed across 5 engineering dimensions (`0.0–10.0`):

| Skill | Determinism | Invariant Coverage | Multi-Agent Orchestration | Verification Coupling | Idempotency & Safety | Composite (`0–10`) | Key Architectural Observation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| [`review_article`](../.agent/skills/review_article/SKILL.md) | `8.5` | `9.5` | `9.5` | `9.5` | `8.5` | **`9.1`** | Most mature architecture: 5-stage parallel fan-out/fan-in pipeline backed by [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md), cleanly separated [`rubric-and-repo-alignment.md`](../.agent/skills/review_article/references/rubric-and-repo-alignment.md) and [`report-template.md`](../.agent/skills/review_article/resources/report-template.md), [`organize_readme`](../.agent/skills/organize_readme/SKILL.md) trail handoff, and Checks 1–7 validation. |
| [`organize_readme`](../.agent/skills/organize_readme/SKILL.md) | `9.5` | `9.5` | `3.0` | `9.5` | `9.5` | **`8.2`** | *(Remediated from `7.8` via Option 4)* Canonical procedural owner for `README.md`, `articles/README.md`, and `articles/CHANGELOG.md` updates, resolving broken paths, registering orphan articles, enforcing `kebab-case.md`, and syncing `[NEW]`/`[UPDATED]` parity. |
| [`update_article`](../.agent/skills/update_article/SKILL.md) | `9.0` | `9.5` | `4.0` | `9.5` | `9.0` | **`8.2`** | *(Remediated from `7.7` via Option 4)* Deduplicated via [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md); protects immutable `**Date:**`, manages in-article `## Changelog`, and delegates `[NEW]`/`[UPDATED]` and `articles/CHANGELOG.md` sync to [`organize_readme`](../.agent/skills/organize_readme/SKILL.md). |
| [`create_article`](../.agent/skills/create_article/SKILL.md) | `8.5` | `9.5` | `4.0` | `9.5` | `8.5` | **`8.0`** | *(Remediated from `7.3` via Option 4)* Deduplicated authoring workflow inheriting Invariants 1–3 from [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md), delegating Hybrid Window `[NEW]` and index reconciliation to [`organize_readme`](../.agent/skills/organize_readme/SKILL.md), and optionally chaining into `review_article`. |
| [`simplify_article`](../.agent/skills/simplify_article/SKILL.md) | `8.5` | `9.5` | `3.5` | `9.5` | `9.0` | **`8.0`** | *(Remediated from `7.0` via Option 4)* Removed legacy `view_file` tool-specific coupling, inherits Pure Open-Source and metadata invariants from [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md), strictly preserves 100% of links/references, and delegates trail sync to [`organize_readme`](../.agent/skills/organize_readme/SKILL.md). |
| [`commit_and_push`](../.agent/skills/commit_and_push/SKILL.md) | `9.5` | `9.0` | `2.0` | `9.5` | `9.0` | **`7.8`** | *(Remediated from `5.0` via Option 4)* Two-phase guarded `jj` workflow backed by [`prepare_commit.sh`](../.agent/skills/commit_and_push/scripts/prepare_commit.sh): enforces `bash verify_links.sh` before `jj describe` / `jj bookmark set`, parameterizes target bookmark (default `main`), and routes failures to `organize_readme`. |

### Key Structural Bottlenecks Observed Across the Current Skill Suite

1. ~~**Duplicated Governance Logic:** The Pure Open-Source Systems Mandate, `Scope & Licensing Note` boilerplate, `[NEW]`/`[UPDATED]` badge rules, and `articles/CHANGELOG.md` update rules are repeated across 4 separate `SKILL.md` files.~~ **Resolved (Option 4):** Declarative invariants (Pure Open-Source Systems Mandate & `Scope & Licensing Note`, `kebab-case.md` layout, immutable `**Date:**` / `**Last Updated:**` / `## Changelog` ordering, and Hybrid Window `[NEW]` / `[UPDATED]` formulas) are centralized in always-on [`.agent/rules/AGENTS.md`](../.agent/rules/AGENTS.md), procedural index/badge/changelog mutation is consolidated into [`organize_readme`](../.agent/skills/organize_readme/SKILL.md), and legacy `view_file` tool coupling was removed from [`simplify_article`](../.agent/skills/simplify_article/SKILL.md).
2. **Multi-Writer Contention Risk:** All 4 content skills still trigger singleton file mutations ([`README.md`](../README.md), [`articles/README.md`](../articles/README.md), [`articles/CHANGELOG.md`](../articles/CHANGELOG.md)) at runtime via `organize_readme` until converted to scoped subagents + the single-writer `index-reconciler` agent.
3. **Unstructured Inter-Agent Outputs:** `review_article` currently relies on ad-hoc subagent prompt generation and free-text score extraction rather than schema-validated JSON contracts.
4. ~~**Missing Pre-Push Gate:** `commit_and_push` can push a broken repository state if executed directly without first running `bash verify_links.sh`.~~ **Resolved (Option 4):** [`commit_and_push`](../.agent/skills/commit_and_push/SKILL.md) now gates `jj describe`, `jj bookmark set`, and `jj git push --bookmark` behind [`prepare_commit.sh`](../.agent/skills/commit_and_push/scripts/prepare_commit.sh) (`verify_links.sh` Checks 1–7 == exit `0`), raising its composite maturity score from `5.0` to `7.8` (`9.25` ex-orchestration).

**Next Document:** [02 — Skills-to-Agents Evaluation & Target Architecture](./02-skills-to-agents-evaluation-and-architecture.md)
