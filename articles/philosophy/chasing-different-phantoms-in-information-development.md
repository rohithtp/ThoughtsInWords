# Chasing Different Phantoms in Information Development

**Date:** March 3, 2026

---

## Introduction

Every practitioner of information development — technical writers, content strategists, documentation engineers — knows the feeling of chasing something that keeps moving. The target shifts before the ink dries. The audience changes before the guide is published. The product disappears before the user manual is complete.

We call this the **phantom problem**. But the singular framing is misleading.

There is not one phantom in information development. There are many — each with its own logic, its own allure, and its own particular way of staying just out of reach.

This article names them, examines why they persist, and asks what it means to chase each one well.

---

## The Taxonomy of Phantoms

### Phantom 1: The Complete Document

The most familiar phantom is **completeness** — the belief that a document can, with sufficient effort, cover everything a reader might ever need.

The complete document is always one section away. One more edge case. One more FAQ. One more clarification.

**Why it persists:**

- Products are fractal. The deeper you document, the more undocumented depth appears.
- Users ask questions the original author never anticipated.
- Completeness is reader-relative: what satisfies an expert baffles a novice, and vice versa.

The complete document has never existed. It never will. But the attempt to approach completeness produces documents far better than those written without the ambition.

---

### Phantom 2: The Perfectly Accurate Document

Accuracy is the second phantom — the idea that documentation can be made permanently correct and then left alone.

The moment a document is published, its accuracy begins to decay. APIs change. UX flows are redesigned. Terminology shifts. An accurate document becomes a misleading one not through any writer's failure, but through the relentless motion of the world it describes.

What makes this phantom particularly insidious:

- **It fails silently.** Unlike broken code, stale documentation does not throw an error. It misleads quietly, costing users time and trust.
- **The decay rate is invisible.** Writers rarely know how many users read an outdated page before anyone notices.
- **Verification is expensive.** Confirming accuracy requires access to the product, to SMEs, and to the time budget — all of which are perennially scarce.

The practices that come closest to catching this phantom are continuous review cycles, docs-as-code tooling with drift detection, and tight engineering-writer collaboration.

---

### Phantom 3: The Universally Understandable Document

Every documentation team eventually confronts an uncomfortable truth: you cannot write one document that serves everyone.

The **universally understandable document** is the phantom of audience inclusivity — the wish that a single artifact could simultaneously guide the beginner, satisfy the expert, and address the integrator, the administrator, the analyst, and the casual curious reader.

The Diataxis framework recognizes this tension explicitly: tutorials, how-to guides, explanations, and reference material serve different cognitive modes and should not be collapsed into a single undifferentiated artifact. Yet organizations routinely demand single documents that do all things at once — and writers comply, producing documents that satisfy no one.

The phantom here is the fantasy of a universal reader, a person who does not exist.

Chasing this phantom well means resisting it: segmenting audiences, creating content variants, accepting that a document perfectly suited to a beginner will bore an expert — and that this is not a defect to be fixed.

---

### Phantom 4: The Frictionless Discovery Experience

Documentation exists to be found. But the **frictionless discovery experience** — where every user instantly locates exactly what they need — remains perpetually elusive.

**Why it persists:**

- Search is a lossy interface. Users search with their vocabulary, not the author's.
- Information architecture is always a bet on how users think, and users think differently.
- A site reorganization that improves findability for 80% of users typically degrades it for the remaining 20%.

Every generation of tooling promises to solve this. Full-text search, faceted filtering, AI-powered semantic search, contextual help, in-product guidance — each moves the needle. None closes the gap entirely.

The phantom shifts its form with every technological generation: once it was a better index, then a better search engine, now a smarter AI assistant. The goal of zero-friction discovery remains just ahead.

---

### Phantom 5: The Self-Maintaining Documentation System

Automation promises liberation from the drudgery of maintenance. The **self-maintaining documentation system** is the phantom of perpetual currency — a system where content updates itself, gaps fill automatically, and human effort approaches zero.

Each decade brings a new candidate:

| Era | Promise |
|-----|---------|
| 2000s | Wikis (crowdsourced maintenance) |
| 2010s | Docs-as-code (treat docs like software) |
| 2020s | AI-generated content (auto-draft, auto-update) |

Each candidate delivers real improvements. Wikis surfaced community knowledge. Docs-as-code brought version control and CI/CD discipline to content. AI tools accelerate drafting and gap identification.

**But none achieves self-maintenance:**

- Wikis require moderation and become outdated and inconsistent without it.
- Docs-as-code requires writer investment in tooling, often exceeding the savings.
- AI tools generate plausible-sounding but factually unreliable content that still requires expert review.

The phantom retreats with every advance. The pursuit is valuable. The destination is fictional.

---

### Phantom 6: The Perfectly Structured Taxonomy

Information architecture is the art of organizing knowledge. The **perfectly structured taxonomy** is the phantom that haunts every content strategist: a classification system so intuitive, so natural, so perfectly mapped to user mental models that navigation becomes effortless.

The challenge is fundamental: a taxonomy is a single structure imposed on knowledge that is inherently multi-dimensional.

- A topic can belong to multiple categories simultaneously.
- Users carry different mental models shaped by their background and intent.
- The taxonomy that makes sense at 100 articles breaks at 1,000.

Faceted navigation, topic tagging, and graph-based knowledge architectures each offer partial solutions. None solves the underlying philosophical problem: an organization of knowledge reflects the mind of its organizer, not the mind of its seeker.

---

### Phantom 7: The Trusted Single Source of Truth

In mature documentation ecosystems, the demand arises for a **single source of truth** — one canonical location where all authoritative content lives, eliminating contradiction, duplication, and version drift.

Who has not seen this system in action:

- Engineering writes in code comments.
- Product writes in Confluence.
- Support writes in Zendesk.
- Marketing writes in the CMS.
- The public-facing docs pull from none of the above.

The four systems drift apart over time. Contradictions proliferate. Users cannot trust any single source because they have learned that no single source is reliable.

The phantom of a single trusted source is pursued through content consolidation projects, DITA architectures, headless CMS strategies, and now AI knowledge graphs. Each consolidation effort is real and valuable. But organizational entropy resists centralization. New silos form around new tools. The phantom scatters and reassembles.

---

## Why We Keep Chasing Them

The rational response to an uncatchable phantom might be to stop chasing it. But that would be a mistake.

Each phantom represents a **legitimate aspiration** that, even incompletely fulfilled, produces better outcomes:

- Chasing completeness produces more thorough documentation than abandoning the goal.
- Chasing accuracy produces fresher documentation than accepting decay.
- Chasing universal understanding produces a wider range of content variants.
- Chasing frictionless discovery produces better search and navigation.
- Chasing self-maintenance produces more automation and reduced toil.
- Chasing ideal taxonomy produces more navigable content hierarchies.
- Chasing a single source of truth reduces duplication and contradiction.

The value is not in reaching the destination. The value is in the direction.

---

## Chasing Well: Principles for the Pursuit

Given that the phantoms cannot be caught, the question becomes: how do we chase them in ways that maximize the value extracted from the pursuit?

### Know Which Phantom You Are Chasing

Teams often confuse their phantoms — investing in accuracy when the real problem is discovery, or reorganizing taxonomy when the real gap is completeness. Diagnosing the right phantom before investing in the chase prevents misallocated effort.

Ask: what is the actual failure mode users are experiencing? Where is friction produced? That diagnostic work reveals which phantom is currently most costly.

### Accept the Shape of the Gap

Every phantom leaves a characteristic gap. Understanding the shape of that gap — what success looks like at 80%, 90%, 95% — helps teams calibrate ambition and investment.

The gap between 0% and 80% accuracy is closable with dedicated effort. The gap between 95% and 100% accuracy may require disproportionate investment for marginal return. Knowing when to redirect effort is as important as knowing how to apply it.

### Build for Iteration, Not Finality

Phantom-resistant documentation systems are designed for continuous improvement, not one-time completion. Versioned content, date-stamped reviews, user feedback instrumentation, and regular audit cycles — these are the structural choices that sustain proximity to the phantom over time.

A documentation system designed to be finished will become a documentation system that is abandoned. A system designed to be tended will be tended.

### Surface the Gaps You Cannot Close

The most honest documentation systems acknowledge their own incompleteness. They direct users to support channels, community forums, or the product team for edge cases they cannot cover. Graceful incompleteness is more trustworthy than false completeness.

An honest signal that says "we do not have documentation for this yet — here is where to go" maintains more user trust than silence or broken pages.

---

## Conclusion

Information development is a discipline of perpetual approximation. The phantoms — completeness, accuracy, universal understanding, frictionless discovery, self-maintenance, ideal taxonomy, trusted single source — are not problems to be eliminated. They are the defining tensions of the craft.

Each phantom describes a form of knowledge that, in principle, could exist. The world is dynamic, audiences are plural, and organizations are complex — and these facts conspire to ensure that the ideal is always just ahead.

The best information developers understand this not as a limitation but as the nature of the work. They have made peace with incompleteness. They are energized by proximity, not paralyzed by distance.

They chase the phantom — all of them, in turn — because the act of chasing is how knowledge becomes more accessible, more accurate, and more useful than it would be if no one chased at all.

The phantoms are not the enemy of good documentation. They are the reason good documentation exists.

---

## References

- [The Diataxis Framework](https://diataxis.fr/) — A systematic approach to technical documentation
- [Every Page is Page One](https://everypageispageone.com/) — Mark Baker on topic-based authoring and audience-centricity
- [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/) — Write the Docs guide to treating documentation as software
- [Information Architecture for the Web and Beyond](https://www.oreilly.com/library/view/information-architecture-4th/9781491913529/) — Rosenfeld, Morville & Arango on the science of organizing information
- [The Paradox of Choice](https://www.ted.com/talks/barry_schwartz_the_paradox_of_choice) — Barry Schwartz on why more options can reduce satisfaction (applied to content breadth)
- [DITA XML Best Practices](https://www.oxygenxml.com/dita/1.3/specs/) — OASIS DITA specification for structured content reuse
- [Knowledgebase Optimization](https://idratherbewriting.com/) — Tom Johnson's blog on technical communication strategy
