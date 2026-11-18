# 01 — Skills Capability & Scale Assessment (`0–10`)

**Parent Index:** [Architectural Plans Index](./README.md) | **Control Plane:** [`.agent/skills/README.md`](../.agent/skills/README.md)
**Assessment Role:** Technical / AI Architect

---

## 1. Architectural Evaluation of the Capability Request (`0–10` Raw vs. Refined Spec)

Evaluating the initial problem statement (*"review the skills and create a readme about capabilities in skills folder"*) across 6 architectural specification parameters establishes why simple file listing is insufficient and defines the target specification implemented in [`.agent/skills/README.md`](../.agent/skills/README.md).

| # | Architecture Parameter | Raw Statement (`0–10`) | Refined Spec (`0–10`) | Architectural Gap & Clarification Applied |
| :-: | :--- | :---: | :---: | :--- |
| **1** | **Scope Boundary Precision** | `4.0` | `9.5` | *"skills folder"* could ambiguously refer to global plugin skills or workspace skills. Scoped strictly to the 6 skills (8 Markdown files, 520 lines) inside `.agent/skills/`. |
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
| **1** | **Discovery & Context Window Scale** | `2.5` | Bounded workspace surface: 6 skill directories, 8 Markdown files, 520 total lines—easily read in a single context pass without RAG or chunking. |
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
| [`review_article`](../.agent/skills/review_article/SKILL.md) | `8.5` | `9.5` | `9.5` | `9.5` | `8.5` | **`9.1`** | Most mature architecture: 5-stage parallel fan-out/fan-in pipeline, cleanly separated [`rubric-and-repo-alignment.md`](../.agent/skills/review_article/references/rubric-and-repo-alignment.md) and [`report-template.md`](../.agent/skills/review_article/resources/report-template.md), and Checks 1–7 validation. |
| [`organize_readme`](../.agent/skills/organize_readme/SKILL.md) | `9.0` | `9.5` | `2.0` | `9.5` | `9.0` | **`7.8`** | Deterministic reconciliation engine: resolves broken paths, registers orphan articles, enforces `kebab-case.md`, and syncs `[NEW]`/`[UPDATED]` parity across READMEs. |
| [`update_article`](../.agent/skills/update_article/SKILL.md) | `8.5` | `9.0` | `3.0` | `9.0` | `8.0` | **`7.7`** | Protects immutable `**Date:**`, enforces `[NEW]` vs. `[UPDATED]` mutual exclusivity, and syncs in-article `## Changelog` with [`articles/CHANGELOG.md`](../articles/CHANGELOG.md). |
| [`create_article`](../.agent/skills/create_article/SKILL.md) | `8.0` | `9.0` | `3.0` | `9.0` | `7.5` | **`7.3`** | Clear category routing, Pure Open-Source filtering, and Hybrid Window `[NEW]` lifecycle management; optionally delegates to `review_article`. |
| [`simplify_article`](../.agent/skills/simplify_article/SKILL.md) | `7.5` | `8.5` | `2.0` | `9.0` | `8.0` | **`7.0`** | Strict zero-loss link/reference preservation contract; minor tool-coupling gap: references `view_file` explicitly on line 16 instead of staying tool-agnostic. |
| [`commit_and_push`](../.agent/skills/commit_and_push/SKILL.md) | `8.5` | `5.0` | `1.0` | `4.0` | `6.5` | **`5.0`** | Clean 3-step `jj` sequence (`describe`, `bookmark set main`, `git push`), but lacks a pre-push `bash verify_links.sh` gate and hardcodes `main`. |

### Key Structural Bottlenecks Observed Across the Current Skill Suite

1. **Duplicated Governance Logic:** The Pure Open-Source Systems Mandate, `Scope & Licensing Note` boilerplate, `[NEW]`/`[UPDATED]` badge rules, and `articles/CHANGELOG.md` update rules are repeated across 4 separate `SKILL.md` files.
2. **Multi-Writer Contention Risk:** All 4 content skills directly mutate singleton repository files ([`README.md`](../README.md), [`articles/README.md`](../articles/README.md), [`articles/CHANGELOG.md`](../articles/CHANGELOG.md)), blocking safe parallel execution across multiple articles.
3. **Unstructured Inter-Agent Outputs:** `review_article` currently relies on ad-hoc subagent prompt generation and free-text score extraction rather than schema-validated JSON contracts.
4. **Missing Pre-Push Gate:** `commit_and_push` can push a broken repository state if executed directly without first running `bash verify_links.sh`.

**Next Document:** [02 — Skills-to-Agents Evaluation & Target Architecture](./02-skills-to-agents-evaluation-and-architecture.md)
