---
name: Review and Verify Article
description: Verify, critique, improve, and rate an article on a 0-10 scale (Before and After) using a multi-subagent pipeline (Reader Mode, Subject Matter Expert, and Technical Architect / Repo Concept Reviewer), apply recommended changes, and generate a linked report in reviews/<category>/<slug>-review.md.
---

# Review and Verify Article

This skill orchestrates a multi-persona verification, architectural audit, and continuous-improvement loop for any article in **ThoughtsInWords**. It spawns three specialized subagents in parallel (**Reader Mode**, **Subject Matter Expert**, and **Technical Architect & Repo Concept Reviewer**), establishes baseline `0–10` ratings across 12 parameters, applies the synthesized improvements to the target article, re-verifies **After** `0–10` scores, and publishes a bidirectionally linked review report in `reviews/<category>/<slug>-review.md`.

## Prerequisites & References

Before starting, read:
1. Repository governance invariants: [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md)
2. Target article: `articles/<category>/<slug>.md`
3. Evaluation rubric & philosophy alignment rules: [rubric-and-repo-alignment.md](./references/rubric-and-repo-alignment.md)
4. Canonical report template: [report-template.md](./resources/report-template.md)
5. Repository philosophy & index context: `README.md` and `articles/README.md`

---

## Workflow (5 Stages)

### Stage 1: Context Discovery & Multi-Subagent "Before" Audit

1. Read the target article (`articles/<category>/<slug>.md`), `README.md`, `articles/README.md`, and `./references/rubric-and-repo-alignment.md`.
2. Check existing sibling and cross-category articles in `articles/README.md` so the Technical Architect subagent can validate or recommend digital garden cross-links accurately.
3. Define (using `define_subagent` with `EnableWriteTools: false`, or invoke using `invoke_subagent` with `TypeName: "research"`) and launch **three independent subagents in parallel**, assigning each its dedicated persona and 4 rubric parameters:
   * **`Reader Mode Reviewer`** (Parameters 1–4):
     * Reads the article fresh as a target reader.
     * Scores Parameters 1–4 (`0–10`) with concise justification and specific, actionable edits for hook/clarity, narrative flow, visual aids (Mermaid/tables), and jargon accessibility.
   * **`Subject Matter Expert Reviewer`** (Parameters 5–8):
     * Audits technical/domain claims, protocols, edge cases, production failure modes, references/citations, currency, and compliance with [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 1 (Pure Open-Source Systems Mandate)** (suggesting pure open-source equivalents where needed).
     * Scores Parameters 5–8 (`0–10`) and provides prioritized technical corrections, missing failure scenarios, or authoritative citations.
   * **`Technical Architect & Repo Concept Reviewer`** (Parameters 9–12):
     * Evaluates architectural trade-offs (scalability, consistency, NFRs, blast radius, lock-in) and audits compliance with [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariants 1–3** and [`rubric-and-repo-alignment.md`](./references/rubric-and-repo-alignment.md).
     * Audits alignment with the **ThoughtsInWords** philosophy in `README.md` (*Intersection of Logic and Emotion*, *Optimistic Nihilism*, *Intellectual Humility*, *Radical Responsibility*, and explicitly guarding against the *Engineer's Philosophy* weakness of over-simplifying systemic/psychological problems as trivial "bugs").
     * Audits Digital Garden interconnectivity (`## Related Articles`, cross-cutting reading trails) and lifecycle metadata.
     * Scores Parameters 9–12 (`0–10`) and lists concrete architectural/repo-alignment recommendations.
4. Wait for all three subagents to return their structured "Before" scores and recommendations.

### Stage 2: Synthesize Recommendations

Merge all findings into a deduplicated, conflict-free remediation plan tagged by priority (`Critical`, `High`, `Medium`, `Low`):
* Ensure every SME technical addition or Technical Architect trade-off table respects Reader Mode pacing (use clean tables, Mermaid diagrams, or concise bullet lists rather than dense prose walls).
* Ensure existing valid citations, `## References`, and original `**Date:**` are strictly preserved.
* Flag any violations of [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 1 (Pure Open-Source Systems Mandate & `Scope & Licensing Note`)** in text, tables, or Mermaid diagrams as `Critical`/`High` remediation items.

### Stage 3: Apply Recommended Changes & Link Report in the Article

Edit `articles/<category>/<slug>.md` to apply the synthesized improvements in compliance with [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariants 1–3**:
1. **Preserve & Update Header Metadata (Invariant 3)**:
   * Keep `**Date:** Month Day, Year` untouched, update `**Last Updated:** Month Day, Year`, and add or update the bidirectional review link directly beneath the date block:
     ```markdown
     **Date:** Month Day, Year
     **Last Updated:** Month Day, Year
     **Review:** [Expert & Architecture Review Report](../../reviews/<category>/<slug>-review.md)
     ```
2. **Apply Body Improvements**:
   * Implement all prioritized Reader, SME, and Technical Architect recommendations (e.g., sharper `## Summary` / `## Key Points`, trade-off matrices, edge-case handling, Mermaid architecture visuals, philosophy/systemic nuance, pure open-source replacements, `Scope & Licensing Note` per Invariant 1 if missing, and enriched `## Related Articles`).
3. **Update In-Article `## Changelog` (Invariant 3)**:
   * Ensure `## Changelog` sits at the very bottom (after `## Related Articles` and `## References`) and prepend:
     ```markdown
     - **Mon DD, YYYY:** Completed multi-persona review (Reader, SME, Technical Architect); applied architectural and readability improvements ([Review Report](../../reviews/<category>/<slug>-review.md)).
     ```

### Stage 4: Re-Verify ("After" 0–10 Scoring) & Write Report

1. Send the revised `articles/<category>/<slug>.md` back to the three active subagents using `send_message` (or re-verify strictly against `./references/rubric-and-repo-alignment.md`) to obtain verified **After** scores (`0–10`) across all 12 parameters and confirm no regressions were introduced.
2. Calculate exact **Persona Sub-Averages**, **Overall Composite Score** (Before and After), and **Deltas** (`After - Before`).
3. Create `reviews/<category>/<slug>-review.md` using `./resources/report-template.md`, ensuring:
   * Links back to `../../articles/<category>/<slug>.md`.
   * Contains `## 2. Before vs. After Scorecard (0–10)` with all 12 parameters, sub-averages, and composite score.
   * Contains `## 3. Reader Mode Review`, `## 4. Subject Matter Expert (SME) Review`, `## 5. Technical Architect & Repo Concept Review`, and `## 6. Recommended Changes & Execution Log`.

### Stage 5: Update Repository Indexes & Verify Health

1. **Update `reviews/README.md`**:
   * Add or update the row for `<Article Title>` in the `## Review Reports Index` table with links to `../articles/<category>/<slug>.md` and `<category>/<slug>-review.md`, Before score, After score, Delta, and Review Date.
2. **Sync Article Revision Trails** (via [`organize_readme/SKILL.md`](../organize_readme/SKILL.md) and [`.agent/rules/AGENTS.md`](../../rules/AGENTS.md) **Invariant 4**):
   * Sync `[UPDATED]` (or preserve `[NEW]` exclusively) in `README.md` and `articles/README.md`, and log ``* **Reviewed & Updated:** [Article Title](category/slug.md) — ... ([Review Report](../reviews/<category>/<slug>-review.md)).`` under today's date in `articles/CHANGELOG.md`.
3. **Run Repository Health Check**:
   * Execute `bash verify_links.sh` and confirm **all 7 checks (Checks 1–7)** pass with exit code `0`.
