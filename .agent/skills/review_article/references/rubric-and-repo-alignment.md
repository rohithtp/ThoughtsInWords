# Evaluation Rubric & Repository Concept Alignment Reference

This reference defines the `0–10` rating scale, the 12 evaluation parameters across three distinct reviewer personas, and the **ThoughtsInWords** philosophical and architectural standards used during article verification.

---

## 1. Scoring Scale Definition (`0–10`)

Every parameter is scored independently on a `0.0` to `10.0` scale (using increments of `0.5` or `1.0`) both **Before** and **After** applying recommended improvements:

| Score Band | Tier | Interpretation |
| :--- | :--- | :--- |
| **9.0 – 10.0** | **Evergreen / Exemplary** | Publication-grade clarity, rigorous architectural trade-offs, zero technical or factual gaps, and deeply integrated into the digital garden mesh. |
| **7.0 – 8.9** | **Strong / Production-Ready** | Solid structure and genuine technical or philosophical substance, with only minor gaps in edge cases, visual aids, or cross-linking. |
| **5.0 – 6.9** | **Seedling / Developing** | Core thesis is visible, but the article lacks architectural trade-off rigor, concrete operational evidence, or smooth narrative pacing. |
| **0.0 – 4.9** | **Draft / Needs Rework** | Superficial, technically inaccurate, disorganized, missing required lifecycle metadata, or misaligned with repository philosophy. |

### Score Aggregation Rules

* **Persona Sub-Average:** Mean of the 4 parameters owned by that persona (rounded to 1 decimal place).
* **Overall Composite Score:** Equal-weighted mean of all 12 parameters across the three personas (rounded to 1 decimal place, out of `10.0`).
* **Scoring Integrity:** Never inflate **After** scores artificially. Only raise a parameter score when specific, verifiable edits were applied to the target article and confirmed upon re-verification.

---

## 2. The 12 Evaluation Parameters (4 per Persona)

### Lens 1: Reader Mode (`reader-mode-reviewer`)

Evaluates the article from the perspective of an intelligent, time-constrained technical or general reader encountering the piece for the first time.

| # | Parameter | What to Assess (`0–10`) |
| :-: | :--- | :--- |
| **1** | **Executive Clarity & Hook (`## Summary` & `## Key Points`)** | Does the title, `## Summary`, and `## Key Points` immediately communicate why the topic matters and deliver a crisp 30-second takeaway? |
| **2** | **Narrative Flow & Cognitive Load** | Does the article progress logically from problem framing to mental model to solution? Are paragraphs well-paced without walls of text or abrupt jumps? |
| **3** | **Visual Aids & Scannability** | Are Mermaid diagrams, ASCII architecture flows, comparison tables, callouts, and structured bullet lists used effectively to reduce cognitive friction? |
| **4** | **Accessibility & Actionable Takeaway** | Is domain jargon contextualized cleanly? Does the reader leave with a memorable mental model, checklist, or concrete decision framework they can apply? |

### Lens 2: Subject Matter Expert (`subject-expert-reviewer`)

Evaluates the article from the perspective of a domain practitioner verifying factual accuracy, operational depth, and currency.

| # | Parameter | What to Assess (`0–10`) |
| :-: | :--- | :--- |
| **5** | **Technical & Domain Accuracy** | Are protocols, APIs, CLI flags, system mechanics, specifications, or philosophical arguments factually sound and free of misleading simplifications? |
| **6** | **Depth of Insight & Edge Cases** | Does the piece address non-obvious nuances, production failure modes, race conditions, security boundaries, or real-world operational constraints? |
| **7** | **Citations, Specifications & Evidence** | Are claims backed by authoritative primary sources, standards (e.g., RFCs, official specs), concrete examples, and preserved intact in `## References`? |
| **8** | **Domain Completeness & Currency** | Does the article reflect current industry standards, lifecycle realities (observability, rollout, deprecation, maintenance), and avoid glaring omissions? |

### Lens 3: Technical Architect & Repo Concept Steward (`technical-architect-reviewer`)

Evaluates both the technical viability of proposed solutions and the article's alignment with the **ThoughtsInWords** digital garden philosophy and repository mechanics.

| # | Parameter | What to Assess (`0–10`) |
| :-: | :--- | :--- |
| **9** | **Architectural Soundness & Trade-Off Rigor** | Are proposed architectures evaluated for scalability, latency/consistency boundaries, blast radius, NFRs (cost, maintainability, lock-in), and tooling licensing/monetization realities? Does it specify *when not to use* an approach? |
| **10** | **ThoughtsInWords Philosophy Alignment** | Does the article embody the core philosophy documented in [README.md](../../../../README.md) without falling into its documented anti-patterns? (See Section 3 below.) |
| **11** | **Digital Garden Interconnectivity** | Does `## Related Articles` meaningfully connect to 2–4 sibling and cross-category notes using relative `.md` paths, strengthening the cross-cutting reading trails in [articles/README.md](../../../../articles/README.md)? |
| **12** | **Repository Lifecycle & Standards Compliance** | Does the file satisfy lowercase `kebab-case.md` naming, immutable `**Date:** Month Day, Year`, `**Last Updated:** Month Day, Year` (when revised), `**Review:**` link, `## Related Articles`, `## References` (if applicable), `## Changelog`, and `verify_links.sh` health? |

---

## 3. Repository Concept & Philosophy Alignment Checklist

Per the root [README.md](../../../../README.md) and [articles/README.md](../../../../articles/README.md), the Technical Architect & Repo Concept Steward must verify solutions and framing against these core pillars:

1. **The Intersection of Logic and Emotion ("Rational Dreamer"):**
   * Balances analytical, scientific rigor with human context—acknowledging how real people (developers, operators, users) experience the system, not just idealized components.
2. **Optimistic Nihilism & Pragmatic Agency:**
   * Acknowledges messy, chaotic real-world constraints without cynicism, converting limitations into clear, deliberate design agency.
3. **Intellectual Humility & Constant Evolution (Digital Garden Ethos):**
   * Treats knowledge as evolving rather than dogmatic. Avoids "one-size-fits-all" absolutes; states assumptions, boundary conditions, and where perspectives must adapt as new experience/data arrives.
4. **Solitude, Inner Architecture & Connective Tissue:**
   * Connects isolated technical mechanisms back to broader systems, teams, or cross-domain patterns rather than treating components in a vacuum.
5. **Guarding Against the "Engineer's Philosophy" Pitfall:**
   * *Critical check from `README.md`:* While analytical deconstruction makes abstract ideas grounded, it **risks over-simplifying deep-seated systemic, organizational, or psychological problems by treating them as simple "bugs" fixed by a quick perspective shift or silver-bullet pattern.**
   * **Verify:** Does the article acknowledge organizational incentives, legacy constraints, socio-technical friction, or migration costs—rather than pretending a diagram or single abstraction magically eliminates systemic complexity?
6. **Radical Responsibility & Craft:**
   * Takes ownership of precision in language ("words") and architecture ("thoughts"), ensuring references, trade-offs, and failure modes are explicitly named.
