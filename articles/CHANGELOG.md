# Garden Activity Log & Changelog

This log permanently records additions, substantive updates, simplifications, and `[NEW]` / `[UPDATED]` index rotations across the **ThoughtsInWords** digital garden. While the root [README.md](../README.md) highlights only the most recent active cohorts, this changelog preserves the full revision trail over time.

## How the Revision Trail Works

1. **Article-Level Trail:** Every article preserves its immutable creation `**Date:**`. When revised, it sets/updates `**Last Updated:** Month Day, Year` in the header and appends a summary bullet to its in-article `## Changelog` section.
2. **Index Badges (`[NEW]` & `[UPDATED]`):** Newly published articles appear under **Recent Additions** (7-day Hybrid Window, min 3 / max 5). Substantively updated articles appear under **Recently Updated** (max 5) with an `[UPDATED]` badge.
3. **Permanent Archive:** Every creation, update, simplification, and badge rotation is recorded chronologically below so historical context is never lost.

---

## November 2026




### November 24, 2026
* **Reviewed & Updated:** [Java Evolution (JDK 1.0 to Java 27): Version Milestones, LTS Support, and Modern JVM Architecture](tools/java-evolution-versions-and-lts-timeline.md) — Completed multi-persona review (Reader, SME, Technical Architect); re-anchored LTS support horizons strictly to pure open-source Eclipse Temurin / OpenJDK Updates timelines with a security blast-radius warning, added Java 6 and Java 22–24 runtime milestones, corrected technical precision across Generational ZGC, JEP 491 unpinning, JEP 512/511 example, JEP 534 benchmarks, and JEP 536 naming, added an architectural trade-offs and GC NFR section, expanded upgrade diagnostics/decision visuals/socio-technical context, and added primary-source JEP and RFC references ([Review Report](../reviews/tools/java-evolution-versions-and-lts-timeline-review.md)). *(Retains active `[NEW]` badge.)*
* **Added:** [Java Evolution (JDK 1.0 to Java 27): Version Milestones, LTS Support, and Modern JVM Architecture](tools/java-evolution-versions-and-lts-timeline.md) — Three-decade evolution of OpenJDK from JDK 1.0 to Java 27 covering release milestones, 6-month vs. LTS support horizons, Virtual Threads, Scoped Values, Compact Object Headers, HTTP/3, AOT object caching, post-quantum TLS 1.3, and upgrade strategy.
* **Rotated (`[NEW]`):** [Local LLM Lifecycle: Mastering Model Management and Updates in Ollama](ai/local-llm-lifecycle-ollama-model-management.md) rotated out of the 5-article `Recent Additions` cap.
* **Rotated (`[NEW]`):** [Design-First Partner APIs: Treating Your OpenAPI Specification as an Independent Product](devops/design-first-partner-api-openapi-architecture.md) rotated out of the 5-article `Recent Additions` cap.
* **Rotated (`[NEW]`):** [The Quick-Commerce Architecture Divide: When Physical Delivery Outpaces Eventual Consistency](distributed-systems/quick-commerce-eventual-consistency-architecture-gap.md) rotated out of the 5-article `Recent Additions` cap.
* **Reviewed & Updated:** [Why I Chose WezTerm over Alacritty and Kitty](tools/wezterm-choice.md) — Completed multi-persona review (Reader, SME, Technical Architect); added Invariant 1 Scope & Licensing Note and OSI license accuracy, corrected Alacritty/Kitty/GPU technical claims, added multiplexing failure-domain architecture with Mermaid diagram, NFR comparison tables, protocols/security boundaries, 2026 nightly packaging and starter ~/.wezterm.lua, anti-use-cases, human constraints, decision checklist, Related Articles, References, and Changelog ([Review Report](../reviews/tools/wezterm-choice-review.md)).
### November 23, 2026
* **Reviewed & Updated:** [Go 1.26: Key Changes and Features](tools/go-1-26-changes.md) — Completed multi-persona review; expanded new(expr) escape analysis, Green Tea GC locality pipeline, RFC 9180 / FIPS 203 cryptography, architectural trade-offs, and upgrade checklist ([Review Report](../reviews/tools/go-1-26-changes-review.md)).
### November 22, 2026
* **Reviewed & Updated:** [CORS, CORB, and ORB: How Modern Browsers Enforce Cross-Origin Isolation](frontend/cors-corb-and-orb-browser-isolation.md) — Added credentialed CORS/Vary: Origin rules, ORB 206/nosniff edge cases, CORP/COOP/COEP & Site Isolation, DevTools triage matrix, NGINX Open Source headers, and architectural trade-offs ([Review Report](../reviews/frontend/cors-corb-and-orb-browser-isolation-review.md)). *(Retains active `[NEW]` badge.)*
* **Simplified:** [CORS, CORB, and ORB: How Modern Browsers Enforce Cross-Origin Isolation](frontend/cors-corb-and-orb-browser-isolation.md) — Simplified structure and readability while preserving all references.
* **Added:** [CORS, CORB, and ORB: How Modern Browsers Enforce Cross-Origin Isolation](frontend/cors-corb-and-orb-browser-isolation.md) — how the Same-Origin Policy (SOP), CORS, CORB, and Opaque Response Blocking (ORB) defend against unauthorized cross-origin reads and Spectre side-channel memory leaks across the browser stack.
* **Rotated (`[NEW]`):** [The Split Inside the Human Mind](philosophy/the-split-inside-the-human-mind.md) rotated out of the 5-article `Recent Additions` cap.
### November 18, 2026
* **Added:** [Energy Resolving into Stillness: State Transitions Within a Single Consciousness](philosophy/energy-resolving-into-stillness.md) — internal mechanics of kinetic force vs. unshakable stillness, the illusion of duality, and transmutation into effortless potency (*Shanta*).
* **Rotated (`[NEW]`):** [The Slow Navigator: Guardrails Against Stalls, Swerves, and Cognitive Sabotage](philosophy/the-slow-navigator-framework.md) rotated out of the 5-article `Recent Additions` cap.

### November 17, 2026
* **Reviewed & Updated:** [Design-First Partner APIs: Treating Your OpenAPI Specification as an Independent Product](devops/design-first-partner-api-openapi-architecture.md) — re-architected all four distribution channels, edge validation, and staging testing onto pure `Apache-2.0`/`MIT`/`BSD-2-Clause` open-source foundations; added airgap provenance (`Syft` + offline `Cosign`), zero-egress portal flags, `0–10` architectural re-evaluation (`8.2` → `9.0`), and cross-links ([Review Report](../reviews/devops/design-first-partner-api-openapi-architecture-review.md)). *(Retains active `[NEW]` badge.)*

### November 16, 2026
* **Added:** [Design-First Partner APIs: Treating Your OpenAPI Specification as an Independent Product](devops/design-first-partner-api-openapi-architecture.md) — decoupled OpenAPI 3.1 repository architecture, automated PR gates, multi-channel partner distribution, and edge/staging contract verification.
* **Updated:** [OpenAPI Specification v3.2.0: Highlights and Changes](devops/openapi-spec-v3-2-0-highlights.md) — added reciprocal cross-links to the Design-First Partner API architecture and API NFR articles, plus `**Last Updated:**` and `## Changelog` revision tracking.
* **Rotated (`[NEW]`):** [The Silent Architecture of Utility Modules: Designing Small Helpers That Don’t Break Large Systems](design/silent-architecture-of-utility-modules.md) rotated out of the 5-article `Recent Additions` cap.
* **Infrastructure:** Introduced two-layer article & repository revision tracking (`**Last Updated:**`, in-article `## Changelog`, `[UPDATED]` badges, `articles/CHANGELOG.md`, `update_article` skill, and `verify_links.sh` Check 6).

### November 15, 2026
* **Added:** [Local LLM Lifecycle: Mastering Model Management and Updates in Ollama](ai/local-llm-lifecycle-ollama-model-management.md)
* **Added:** [The Quick-Commerce Architecture Divide: When Physical Delivery Outpaces Eventual Consistency](distributed-systems/quick-commerce-eventual-consistency-architecture-gap.md)

### November 14, 2026
* **Added:** [The Split Inside the Human Mind](philosophy/the-split-inside-the-human-mind.md)
* **Added:** [The Slow Navigator: Guardrails Against Stalls, Swerves, and Cognitive Sabotage](philosophy/the-slow-navigator-framework.md)

### November 13, 2026
* **Added:** [The Silent Architecture of Utility Modules: Designing Small Helpers That Don’t Break Large Systems](design/silent-architecture-of-utility-modules.md)

### November 12, 2026
* **Added:** [Architectural Risk Assessment: Public Font CDNs in Airgapped Environments](frontend/airgapped-font-cdn-anti-pattern.md)
* **Added:** [From One Machine to Many: The Complete Guide to Learning Docker Compose and Kubernetes](devops/docker-compose-to-kubernetes-guide.md)

### November 11, 2026
* **Added:** [Airgapped Production Font Deployment Guide](frontend/airgapped-production-font-deployment.md)
