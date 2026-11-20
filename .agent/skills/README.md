# ThoughtsInWords Agent Skills Directory

Welcome to the agentic control plane for **ThoughtsInWords** ([Root Overview](../../README.md) | [Full Article Index](../../articles/README.md) | [Review Reports Index](../../reviews/README.md) | [Activity Changelog](../../articles/CHANGELOG.md) | [Repository Rules](../rules/AGENTS.md)).

The `.agent/skills/` folder houses **6 modular agent skills** (backed by 8 Markdown specification, reference, and template files totaling 546 lines plus 6 deterministic/orchestration scripts totaling 3,496 lines, statically indexed by [`pyrightconfig.json`](../../pyrightconfig.json) and managed via [`pyproject.toml`](../../pyproject.toml) / [`requirements.txt`](../../requirements.txt)) governed by the always-on workspace rule [`.agent/rules/AGENTS.md`](../rules/AGENTS.md) (34 lines). Together they form a **Pure Hybrid Control Plane (Option H3)** automating the complete lifecycle of the digital garden: ingesting, authoring, updating, and simplifying articles via scoped subagents and deterministic pre-handoff invariant/link-retention gates (`run_content_workflow.py` + `verify_article_mutation()`), running schema-validated multi-subagent `0–10` architectural audits (`run_review_workflow.py`), reconciling repository indexes and `reciprocal_articles_touched` trails via a single-writer engine (`reconcile_indexes.py`) executed through the `uv`-first / `pip`-fallback wrapper [`run_python.sh`](./organize_readme/scripts/run_python.sh), and publishing via Jujutsu (`jj`).

---

## 1. Technical & AI Architect Assessment (`0–10` Scale)

Before cataloging individual capabilities, this control plane is evaluated across **required architectural scale** and **per-skill engineering maturity** (`0.0–10.0`).

### 1.1 Scale Required Across AI & Technical System Parameters (`0–10`)

| # | Architectural Parameter | Scale Required (`0–10`) | Scope & Engineering Rationale |
| :-: | :--- | :---: | :--- |
| **1** | **Discovery & Context Window Scale** | `2.5` | Small, bounded markdown surface area: 1 always-on rule file (`AGENTS.md`, 34 lines) + 6 skill directories (8 Markdown files, 546 lines) + 6 scripts (`prepare_commit.sh`, `run_python.sh`, `reconcile_indexes.py`, `run_content_workflow.py`, `schemas.py`, `run_review_workflow.py`; 3,496 lines), easily indexed in one context pass. |
| **2** | **Agentic Compute & Orchestration Scale** | `2.0` / `8.0` | `2.0` for static index/skill discovery; peaks at `8.0` at runtime across [`review_article`](./review_article/SKILL.md) (3 stateful read-only reviewer handles across Stage 1/Stage 4 + batch `article_paths`) and [`run_content_workflow.py`](./create_article/scripts/run_content_workflow.py) (parallel scoped content subagents via `workspace: "share"`). |
| **3** | **State Mutation & Blast Radius Scale** | `1.5` / `8.0` | `1.5` for documenting `.agent/skills/README.md`; `8.0` across the skills themselves, partitioned so content workflows pass `verify_article_mutation()` before `reconcile_indexes.py` mutates singleton indexes (`README.md`, `articles/README.md`, `articles/CHANGELOG.md`, `reviews/README.md`). |
| **4** | **Cross-Skill Dependency & DAG Coupling Scale** | `8.0` | High workflow coupling: `create_article`, `update_article`, `simplify_article`, and `review_article` inherit invariants from `.agent/rules/AGENTS.md`, validate article mutations in `schemas.py`, and emit `INDEX_HANDOFF_SCHEMA` payloads (including `reciprocal_articles_touched`) to `reconcile_indexes.py` and `verify_links.sh`. |
| **5** | **Governance & Repository Invariant Scale** | `9.0` | Strict invariant surface centralized in `.agent/rules/AGENTS.md`: Hybrid Window `[NEW]` math, `[UPDATED]` exclusivity, Pure Open-Source Systems mandate, immutable `**Date:**`, zero-loss link retention, and a 12-parameter `0–10` review rubric. |
| **6** | **Verification & Deterministic Gate Scale** | `9.0` | Backed by [`verify_links.sh`](../../verify_links.sh) (Checks 1–8), `schemas.py --self-test` (5 schemas + link-retention/Invariant 3 gate + anti-inflation validation), `run_review_workflow.py --self-test` (single & batch 5-stage pipeline), `run_content_workflow.py --self-test` (create/update/batch simplify + link-drop rejection), and `reconcile_indexes.py --self-test`. |
| **7** | **Documentation Depth & Dual-Audience Ergonomics** | `8.0` | Must serve both **human maintainers** (navigating workflows, invariants, and VCS rules) and **AI agents** (fast capability routing, preconditions, and execution contracts). |
| **8** | **Operational Maintenance & Drift-Prevention Scale** | `6.5` | Centralizing declarative invariants in `.agent/rules/AGENTS.md`, article mutation checks in `schemas.py`, index writes in `reconcile_indexes.py`, and workflow orchestration in `run_content_workflow.py` / `run_review_workflow.py` prevents multi-file rule and arithmetic drift. |

### 1.2 Architectural Maturity Scorecard of Existing Skills (`0–10`)

Each skill in `.agent/skills/` is rated below across 5 architectural dimensions (`0.0–10.0`):

| Skill | Determinism | Invariant Coverage | Multi-Agent Orchestration | Verification Coupling | Idempotency & Safety | Composite (`0–10`) | Key Architectural Observation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| [`review_article`](./review_article/SKILL.md) | `10.0` | `9.9` | `9.9` | `9.9` | `9.8` | **`9.9`** | *(Upgraded `9.1 → 9.7 → 9.9` via Options B4 + A4 + H3)* Stateful `run_workflow` module ([`run_review_workflow.py`](./review_article/scripts/run_review_workflow.py)) with configurable `reviewer_type` / model tiering, batch `article_paths`, Stage 3 `verify_article_mutation()` gate, [`schemas.py`](./review_article/scripts/schemas.py) anti-inflation clamping, and single-writer `reconcile_indexes.py` handoff. |
| [`organize_readme`](./organize_readme/SKILL.md) | `9.9` | `9.9` | `9.6` | `9.8` | `9.8` | **`9.8`** | *(Upgraded `7.8 → 9.5 → 9.8` via Options A4 + H3)* Deterministic single-writer [`reconcile_indexes.py`](./organize_readme/scripts/reconcile_indexes.py) expanding `reciprocal_articles_touched` into validated `"Updated"` handoffs, computing `[NEW]`/`[UPDATED]` parity, updating counts/changelogs/reviews, and verified via `--self-test` + `verify_links.sh`. |
| [`create_article`](./create_article/SKILL.md) | `9.6` | `9.6` | `9.6` | `9.8` | `9.4` | **`9.6`** | *(Upgraded `7.3 → 8.8 → 9.6` via Options A4 + H3)* Scoped authoring backed by [`run_content_workflow.py`](./create_article/scripts/run_content_workflow.py) (`mode="create"`), `CONTENT_MUTATION_RESULT_SCHEMA` + `verify_article_mutation()`, optional `chain_review`, and atomic `reconcile_indexes.py` handoff. |
| [`update_article`](./update_article/SKILL.md) | `9.6` | `9.6` | `9.5` | `9.8` | `9.5` | **`9.6`** | *(Upgraded `7.7 → 8.9 → 9.6` via Options A4 + H3)* Scoped edits backed by [`run_content_workflow.py`](./create_article/scripts/run_content_workflow.py) (`mode="update"`), immutable `**Date:**` & link-retention diffing, reciprocal backfill sync, and `reconcile_indexes.py` handoff. |
| [`simplify_article`](./simplify_article/SKILL.md) | `9.6` | `9.6` | `9.5` | `9.8` | `9.5` | **`9.6`** | *(Upgraded `7.0 → 8.8 → 9.6` via Options A4 + H3)* Parallel batch-ready (`workspace: "share"`) structural refactoring via [`run_content_workflow.py`](./create_article/scripts/run_content_workflow.py) (`mode="simplify"`), deterministic 100% link-retention diff gate, and single-writer handoff. |
| [`commit_and_push`](./commit_and_push/SKILL.md) | `9.6` | `9.2` | `2.0` | `9.8` | `9.4` | **`8.0`** | Two-phase guarded `jj` workflow via [`prepare_commit.sh`](./commit_and_push/scripts/prepare_commit.sh): enforces `verify_links.sh` (Checks 1–8 across all 4 Python engines) before `jj describe` / `jj bookmark set`, parameterizes target bookmark (default `main`), and routes failures to `organize_readme`. |

> **Architect's Note on Scoring:** The `Multi-Agent Orchestration` score reflects whether a skill requires subagent fan-out (`review_article` and batch content workflows do; atomic skills like `commit_and_push` intentionally do not, scoring `9.5` ex-orchestration). `Composite` is the equal-weighted mean across the 5 columns.

---

## 2. End-to-End Agentic Workflow & Skill Topology

All content skills form a directed **Pure Hybrid** workflow converging on deterministic Python validation (`verify_article_mutation()` + `reconcile_indexes.py`) and [`verify_links.sh`](../../verify_links.sh) before publication through Jujutsu (`jj`).

```mermaid
flowchart TD
    User["User Intent / Request"] --> Route{"Route to Thin Skill"}

    Route -->|"New topic or URL"| Create["create_article"]
    Route -->|"Expand or revise"| Update["update_article"]
    Route -->|"Reformat or clean prose"| Simplify["simplify_article"]
    Route -->|"Audit quality (0-10)"| Review["review_article"]
    Route -->|"Repair index or badges"| Organize["organize_readme"]
    Route -->|"Publish changes"| Push["commit_and_push"]

    Create & Update & Simplify -->|"mode: create / update / simplify"| ContentWF["run_content_workflow.py (Scoped Agent / Batch Parallel)"]
    ContentWF -->|"verify_article_mutation() (Invariants 1-3 + 100% Link Retention)"| ContentGate{"Pre-Handoff Gate"}
    ContentWF -.->|"Optional chain_review=True"| Review

    subgraph FanOut["review_article: run_review_workflow.py (Single or Batch article_paths)"]
        Reviewer["Stage 1 & 4 Read-Only Handles (Reader, SME, Architect)"]
        Remediator["Stage 2 & 3 Scoped Remediator + verify_article_mutation()"]
        Reviewer -->|"BEFORE_SCORECARD_SCHEMA"| Remediator
        Remediator -->|"AFTER_SCORECARD_SCHEMA + Check 7 Report"| Reviewer
    end

    Review --> FanOut
    ContentGate -->|"INDEX_HANDOFF_SCHEMA (+ reciprocal_articles_touched)"| Sync["Single-Writer: reconcile_indexes.py"]
    FanOut -->|"INDEX_HANDOFF_SCHEMA (Single or Batch)"| Sync
    Organize --> Sync

    Sync --> Gate["verify_links.sh (Checks 1-8)"]
    Gate -->|"Exit 0"| Push
    Gate -->|"Errors found"| Organize
    Push -->|"prepare_commit.sh (verify_links.sh -> describe -> bookmark)"| Remote["jj git push --bookmark"]
    Push -->|"Checks 1-8 fail"| Organize
```

---

## 3. Skills Capability Directory

| Skill | Folder | Trigger Intents | Primary Mutated Targets | Verification Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Create Article** | [`create_article/`](./create_article/SKILL.md) | "create a new article", "add a summary of [URL]" | `articles/<category>/<slug>.md` (via `run_content_workflow.py` -> `reconcile_indexes.py`) | `verify_article_mutation()` + `reconcile_indexes.py` + `verify_links.sh` (Checks 1–8) |
| **Update Article** | [`update_article/`](./update_article/SKILL.md) | "update article", "expand", "revise", "add a section to" | Existing article (+ optional reciprocal siblings -> `reconcile_indexes.py`) | `verify_article_mutation()` (100% link retention) + `reconcile_indexes.py` + `verify_links.sh` |
| **Simplify Article** | [`simplify_article/`](./simplify_article/SKILL.md) | "simplify article", "make readable", "clean up format" | Existing article(s) via batch `workspace: "share"` -> `reconcile_indexes.py` | `verify_article_mutation()` (100% link retention) + `reconcile_indexes.py` + `verify_links.sh` |
| **Review and Verify Article** | [`review_article/`](./review_article/SKILL.md) | Multi-persona quality audit, `0–10` scoring, architectural review | Target article(s), `reviews/<category>/<slug>-review.md` (`run_review_workflow.py` -> `reconcile_indexes.py`) | Stage 3 `verify_article_mutation()` + 4 `--self-test` gates + `verify_links.sh` |
| **Organize README** | [`organize_readme/`](./organize_readme/SKILL.md) | "organize readme", "fix links", "update index" | Single-writer owner of `README.md`, `articles/README.md`, `reviews/README.md`, `articles/CHANGELOG.md` | `reconcile_indexes.py --self-test` + `bash verify_links.sh` (Checks 1–8) |
| **Commit and Push with JJ** | [`commit_and_push/`](./commit_and_push/SKILL.md) | Save progress and push working copy to git remote | Jujutsu (`jj`) revision description, target bookmark (default `main`), remote git repository | `prepare_commit.sh` (`bash verify_links.sh` Checks 1–8) before `jj describe` / `bookmark set` / `jj git push` |

### 3.1 Create Article (`create_article`)

* **Specification:** [`create_article/SKILL.md`](./create_article/SKILL.md)
* **Supporting Script:** [`create_article/scripts/run_content_workflow.py`](./create_article/scripts/run_content_workflow.py)
* **Core Capabilities:**
  * **Topic Classification:** Inspects existing subdirectories under `articles/` (`ai`, `cloud-native`, `design`, `devops`, `distributed-systems`, `environment`, `frontend`, `licensing`, `philosophy`, `testing`, `tools`, `travel`) and assigns a matching category—forbidding date-based folders per [`.agent/rules/AGENTS.md`](../rules/AGENTS.md) Invariant 2.
  * **Hybrid Workflow Authoring & Validation:** Executes via [`run_content_workflow.py`](./create_article/scripts/run_content_workflow.py) (`mode="create"`) or direct authoring to `articles/<category>/<kebab-case-slug>.md`, enforcing Invariants 1–3 (`**Date:** Month Day, Year`, `Scope & Licensing Note`, `## Summary`, `## Key Points`, `## Related Articles`, initial `## Changelog`) via `CONTENT_MUTATION_RESULT_SCHEMA` and `verify_article_mutation()`.
  * **Trail Reconciliation Handoff & Review Chain:** Never edits singleton indexes directly; emits `INDEX_HANDOFF_SCHEMA` (`"Added"`, including `reciprocal_articles_touched`) to [`reconcile_indexes.py`](./organize_readme/scripts/reconcile_indexes.py) and optionally sets `chain_review=True` to chain directly into [`run_review_workflow.py`](./review_article/scripts/run_review_workflow.py).

### 3.2 Update Article (`update_article`)

* **Specification:** [`update_article/SKILL.md`](./update_article/SKILL.md)
* **Core Capabilities:**
  * **Hybrid Workflow & Immutable Metadata:** Runs via [`run_content_workflow.py`](./create_article/scripts/run_content_workflow.py) (`mode="update"`) or direct edit—enforcing [`.agent/rules/AGENTS.md`](../rules/AGENTS.md) Invariant 3 (preserving original `**Date:**`, adding/updating `**Last Updated:**`, prepending reverse-chronological entries to bottom `## Changelog`) and verifying zero dropped links via `verify_article_mutation()`.
  * **Licensing & Reciprocal Cross-Linking:** Validates Invariant 1 (Pure Open-Source Systems Mandate & `Scope & Licensing Note`) across existing and added content, and refreshes `## Related Articles`.
  * **Trail Reconciliation Handoff:** Never edits singleton indexes directly; emits `INDEX_HANDOFF_SCHEMA` (`"Updated"`, with `reciprocal_articles_touched`) to [`reconcile_indexes.py`](./organize_readme/scripts/reconcile_indexes.py) so both primary and reciprocal articles receive `[UPDATED]` cohort evaluation and `articles/CHANGELOG.md` entries.

### 3.3 Simplify Article (`simplify_article`)

* **Specification:** [`simplify_article/SKILL.md`](./simplify_article/SKILL.md)
* **Core Capabilities:**
  * **Parallel Batch Structural Refactoring:** Runs single or multi-article (`article_paths`, `workspace: "share"`) structural cleanup via [`run_content_workflow.py`](./create_article/scripts/run_content_workflow.py) (`mode="simplify"`), normalizing header hierarchy (`#` → `##` → `###`), breaking up dense prose walls, separating cluttered lists, adding blank lines around headers/lists, and adding Mermaid diagrams where helpful.
  * **Deterministic Zero-Loss Reference Guarantee:** `verify_article_mutation()` diffs `extract_markdown_links(before_text)` against `extract_markdown_links(after_text)` and aborts the handoff if any citation, footnote, or link was dropped.
  * **Governance & Trail Sync:** Enforces Invariants 1 & 3 (`**Last Updated:**`, `## Changelog` prepending) and emits single or batch `INDEX_HANDOFF_SCHEMA` (`"Simplified"`) payloads to [`reconcile_indexes.py`](./organize_readme/scripts/reconcile_indexes.py).

### 3.4 Review and Verify Article (`review_article`)

* **Specification:** [`review_article/SKILL.md`](./review_article/SKILL.md)
* **Supporting Artifacts:**
  * Always-on invariants: [`.agent/rules/AGENTS.md`](../rules/AGENTS.md)
  * Evaluation rubric & philosophy alignment rules: [`review_article/references/rubric-and-repo-alignment.md`](./review_article/references/rubric-and-repo-alignment.md)
  * Canonical report schema: [`review_article/resources/report-template.md`](./review_article/resources/report-template.md)
  * JSON Schemas, article mutation gate, anti-inflation clamp & Check 7 renderer: [`review_article/scripts/schemas.py`](./review_article/scripts/schemas.py)
  * Stateful multi-turn `run_workflow` orchestrator: [`review_article/scripts/run_review_workflow.py`](./review_article/scripts/run_review_workflow.py)
* **Core Capabilities (5-Stage Stateful `run_workflow` Pipeline — Options B4 + A4 + H3):**
  1. **Stage 1 — Parallel Read-Only "Before" Audit:** Instantiates 3 persistent read-only reviewer handles (`r_reader` Params 1–4, `r_sme` Params 5–8, `r_arch` Params 9–12; supports configurable `reviewer_type` such as `"research"` or `"self"` and `reviewer_model` tiering) and runs them via `parallel()` against `BEFORE_SCORECARD_SCHEMA` across single (`article_path`) or batch (`article_paths`) targets.
  2. **Stage 2 & 3 — Scoped Article Remediation & Mutation Gate:** Sorts findings (`Critical`, `High`, `Medium`, `Low`), invokes a scoped `Article Remediator` (`REMEDIATION_RESULT_SCHEMA`, optional `remediator_model`) mutating **only** `articles/<category>/<slug>.md`, and enforces `verify_article_mutation()` (immutable `**Date:**`, `**Last Updated:**`, `**Review:**`, bottom section order) before Stage 4 runs.
  3. **Stage 4 — Multi-Turn "After" Re-Verification & Deterministic Report Rendering:** Re-invokes the **same 3 persistent handles** via `parallel()` against `AFTER_SCORECARD_SCHEMA`, enforces anti-inflation clamping, computes sub-averages/composite/deltas in Python (`compute_scorecard()`), and renders `reviews/<category>/<slug>-review.md` (`render_review_report()`).
  4. **Stage 5 — Single-Writer Index Reconciliation:** Emits validated single or batch `INDEX_HANDOFF_SCHEMA` payloads to [`reconcile_indexes.py`](./organize_readme/scripts/reconcile_indexes.py) to sync `reviews/README.md`, `README.md`, `articles/README.md`, `articles/CHANGELOG.md`, and run `bash verify_links.sh`.

### 3.5 Organize README (`organize_readme`)

* **Specification:** [`organize_readme/SKILL.md`](./organize_readme/SKILL.md)
* **Supporting Scripts:** [`organize_readme/scripts/run_python.sh`](./organize_readme/scripts/run_python.sh), [`organize_readme/scripts/reconcile_indexes.py`](./organize_readme/scripts/reconcile_indexes.py)
* **Core Capabilities (Single-Writer Index Engine — Options A4 + H3):**
  * **Structured Handoff, Reciprocal Expansion & Standalone Discovery:** Consumes validated `INDEX_HANDOFF_SCHEMA` payloads (`--handoff` / `--handoff-file`), expands `reciprocal_articles_touched` via `expand_reciprocal_handoffs()` into validated `"Updated"` handoffs, or scans `articles/` standalone, enforcing [`.agent/rules/AGENTS.md`](../rules/AGENTS.md) Invariant 2.
  * **Self-Healing & Deterministic Index Sync:** Inserts unlisted articles alphabetically (`- [Title](category/slug.md)`), self-heals uniquely moved paths, updates `reviews/README.md`, computes the exact Hybrid Window `[NEW]` cohort and top-5 `[UPDATED]` exclusivity trail (Invariant 4), writes `articles/CHANGELOG.md` events idempotently, updates category/total counts across both READMEs, validates via `--self-test`, and gates on `bash verify_links.sh`.

### 3.6 Commit and Push with JJ (`commit_and_push`)

* **Specification:** [`commit_and_push/SKILL.md`](./commit_and_push/SKILL.md)
* **Supporting Scripts:** [`commit_and_push/scripts/prepare_commit.sh`](./commit_and_push/scripts/prepare_commit.sh)
* **Core Capabilities:**
  * **Two-Phase Guarded `jj` Publication Flow:** Phase 1 executes `prepare_commit.sh` locally (`set -euo pipefail`) to run `bash verify_links.sh` (Checks 1–8) **before** executing `jj describe -m "..."` and `jj bookmark set <bookmark> -r @` (default `main`). Phase 2 executes `jj git push --bookmark <bookmark>` only after Phase 1 exits `0`, isolating network access strictly to the push step.
  * **Hard Gate & Self-Healing Routing:** Aborts before any bookmark mutation if Checks 1–8 fail, forbids manual bypass, and routes index/badge/link drift to [`organize_readme`](./organize_readme/SKILL.md) before retrying.

---

## 4. Cross-Skill Repository Invariants & Governance Contract

Declarative repository invariants are centralized as an always-on workspace rule in [`.agent/rules/AGENTS.md`](../rules/AGENTS.md) (eliminating per-skill boilerplate), while article pre-handoff mutation validation (`verify_article_mutation()`) lives in [`schemas.py`](./review_article/scripts/schemas.py) and single-writer index/badge/changelog reconciliation lives in [`organize_readme/SKILL.md`](./organize_readme/SKILL.md) / [`reconcile_indexes.py`](./organize_readme/scripts/reconcile_indexes.py) and is enforced by [`verify_links.sh`](../../verify_links.sh):

1. **Invariant 1 — Pure Open-Source Systems Mandate & `Scope & Licensing Note`:** Articles covering tools, frameworks, or platforms must exclusively feature OSI-approved pure open-source systems (full feature set self-hostable without vendor lock-in or paywalled tiers), excluding proprietary, commercial-only, and open-core ("Community Edition") systems and carrying the canonical `Scope & Licensing Note` callout defined in [`.agent/rules/AGENTS.md`](../rules/AGENTS.md).
2. **Invariant 2 — Naming & Layout Discipline:** All articles live at `articles/<category>/<kebab-case>.md`; all review reports live at `reviews/<category>/<kebab-case>-review.md`. Date-based directories, uppercase letters, underscores in article filenames, and empty directories are prohibited.
3. **Invariant 3 — Immutable Metadata & Section Ordering:** Immutable `**Date:** Month Day, Year`, updated `**Last Updated:** Month Day, Year` (when revised), optional `**Review:**` link, and bottom section order (`## Related Articles` → `## References` → `## Changelog`).
4. **Invariant 4 — Hybrid Window `[NEW]`, `[UPDATED]` Exclusivity & Trail Parity:**
   * `[NEW]` applies to all articles published within **7 days** of the newest article's `**Date:**`, clamped to min `3` and max `5`: `expected_count = min(5, max(3, count_within_7_days))`.
   * `[UPDATED]` applies to at most **5** revised articles (`**Last Updated:**` + `## Changelog`) that do **not** currently hold `[NEW]`.
   * Both badge sets and counts must match 1-to-1 between root [`README.md`](../../README.md) and [`articles/README.md`](../../articles/README.md), with events logged via [`organize_readme`](./organize_readme/SKILL.md) in [`articles/CHANGELOG.md`](../../articles/CHANGELOG.md).
5. **Automated Verification Gate ([`verify_links.sh`](../../verify_links.sh)):**
   * **Check 1 / 1b / 1c:** Every relative `.md` link in `articles/README.md`, `README.md`, and `articles/CHANGELOG.md` resolves on disk.
   * **Check 2:** Zero orphan articles (every article on disk is indexed in `articles/README.md`).
   * **Check 3:** Every internal relative `.md` cross-link inside every article resolves cleanly.
   * **Check 4:** Zero empty directories under `articles/` and 100% lowercase `kebab-case.md` compliance.
   * **Check 5:** Hybrid Window `[NEW]` cohort accuracy and article count parity across both READMEs.
   * **Check 6:** Revision trail integrity (`**Last Updated:**` format and date ordering, `## Changelog` entries, `[UPDATED]` cap of 5, mutual exclusivity with `[NEW]`, and `articles/CHANGELOG.md` presence).
   * **Check 7:** Review report structure (`reviews/<category>/<slug>-review.md`), `reviews/README.md` indexing, bidirectional article ↔ report linking, and required `0–10` scorecard/persona sections.
   * **Check 8:** `uv`/`pip` manifests ([`pyproject.toml`](../../pyproject.toml), [`requirements.txt`](../../requirements.txt), [`pyrightconfig.json`](../../pyrightconfig.json), [`.gitignore`](../../.gitignore) Python patterns), Python compilation (`py_compile` across `.agent/skills/**/*.py`), offline `--self-test` gates across all 4 Python engines (`schemas.py`, `run_review_workflow.py`, `run_content_workflow.py`, `reconcile_indexes.py`) via [`run_python.sh`](./organize_readme/scripts/run_python.sh), and control-plane/plan relative link resolution.

---

## 5. Directory Structure

```text
.agent/
├── rules/
│   └── AGENTS.md                                      # Always-on governance invariants (OS-only, layout, metadata, badges)
└── skills/
    ├── README.md                                      # This architectural overview & capability index
    ├── commit_and_push/
    │   ├── SKILL.md                                   # Two-phase guarded Jujutsu (jj) publication workflow
    │   └── scripts/
    │       └── prepare_commit.sh                      # Atomic pre-push verify_links.sh gate & jj bookmark stager
    ├── create_article/
    │   ├── SKILL.md                                   # Thin router -> run_content_workflow.py (create) & reconcile_indexes.py
    │   └── scripts/
    │       └── run_content_workflow.py                # Unified single/batch hybrid content orchestrator (create/update/simplify)
    ├── organize_readme/
    │   ├── SKILL.md                                   # Single-writer index, badge, reciprocal & CHANGELOG trigger
    │   └── scripts/
    │       ├── run_python.sh                          # uv-first / pip-fallback dependency & Python runner
    │       └── reconcile_indexes.py                   # Deterministic single-writer index, reciprocal & verify_links.sh engine
    ├── review_article/
    │   ├── SKILL.md                                   # Thin trigger -> runpy.run_path('...run_review_workflow.py')
    │   ├── references/
    │   │   └── rubric-and-repo-alignment.md           # 12-parameter 0-10 rubric & ThoughtsInWords philosophy checks
    │   ├── resources/
    │   │   └── report-template.md                     # Canonical Before/After review report template
    │   └── scripts/
    │       ├── schemas.py                             # 5 JSON Schemas, link-retention/Invariant 3 gate & Check 7 renderer
    │       └── run_review_workflow.py                 # Standard-Python single/batch run_pipeline() + offline mock --self-test
    ├── simplify_article/
    │   └── SKILL.md                                   # Thin router -> run_content_workflow.py (simplify, workspace="share")
    └── update_article/
        └── SKILL.md                                   # Thin router -> run_content_workflow.py (update) & reciprocal handoff
```

---

## 6. Architectural Plans & Skill-to-Agent Migration Roadmap (`plan/`)

Detailed `0–10` architectural assessments and the blueprint for growing these skills into a **Pure Hybrid Control Plane** (thin routing skills + scoped `run_workflow` subagents + deterministic Python mutation/index gates) live in the repository's [`plan/`](../../plan/README.md) folder:

* **[Architectural Plans Index](../../plan/README.md):** Overview and executive summary of Phases 1–4 (Options 4, A4, B4, Strategy S4, and Option H3).
* **[01 — Skills Capability & Scale Assessment (`0–10`)](../../plan/01-skills-capability-and-scale-assessment.md):** Prompt specification audit (`4.2 → 9.2`), 8-parameter AI/technical system scale evaluation, and current Phase 4 skill maturity scorecard.
* **[02 — Skills-to-Agents Evaluation & Target Architecture](../../plan/02-skills-to-agents-evaluation-and-architecture.md):** 6-parameter conversion ROI matrix (`9.5` down to `2.0`), Option A1–A4, B1–B4, and H1–H3 trade-off matrices, JSON handoff/mutation contracts, and target Pure Hybrid Mermaid topology.
* **[03 — Phased Migration Execution Plan](../../plan/03-phased-migration-execution-plan.md):** Step-by-step Phases 1–4 implementation tasks and verification acceptance criteria.
