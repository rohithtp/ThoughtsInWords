# ThoughtsInWords

A personal repository for organizing and archiving written thoughts, reflections, and articles by [Rohith T P](https://rohithtp.github.io/rohithtp-cv/).

## Author

* **Rohith T P**: [CV / Personal Site](https://rohithtp.github.io/rohithtp-cv/)

## Purpose

ThoughtsInWords is a structured space for capturing daily thoughts, ideas, articles, and reflections.

## Organization

Articles are organized by **topic** (domain folders) rather than chronologically, using lowercase `kebab-case.md` filenames. This aligns with a "digital garden" approach where content is grouped by context and connected across topics.

```text
articles/
├── README.md              # This index
├── ai/                    # Artificial Intelligence & ML (16)
│   ├── Agents & Tooling
│   └── Strategy & Impact
├── cloud-native/          # Cloud-native architecture & isolation (5)
├── design/                # UI/UX & software design (8)
├── devops/                # Infrastructure, APIs, Auth, Git, Platform (21)
│   ├── APIs & Specifications
│   ├── Authentication & Authorization
│   ├── Git & Version Control
│   ├── Observability & Operations
│   └── Platform & Scaling
├── distributed-systems/   # Distributed systems & messaging (4)
├── environment/           # Climate & planetary systems (2)
├── frontend/              # Web development, mobile & frameworks (16)
├── licensing/             # Open source licensing (1)
├── philosophy/            # Tech philosophy, thinking & wellness (20)
│   ├── Career & Growth
│   ├── Critical Thinking & Emotions
│   ├── Information & Thought
│   ├── Personal & Wellness
│   └── Programming Philosophy
├── testing/               # QA & testing strategies (2)
├── tools/                 # Productivity & developer tools (11)
└── travel/                # Travel guides & experiences (3)
```

## Digital Garden Approach

Unlike a traditional blog where posts are static and ordered by date, ThoughtsInWords follows the **Digital Garden** philosophy:

* **Growth over time**: Articles are not "finished" upon publication. They are seeds that grow as new information is learned and added.
* **Contextual Organization**: Content is linked and grouped by topic rather than timestamps, making it easier to explore related ideas.
* **Evolution**: Some notes may start as rough thoughts (seedlings) and evolve into comprehensive guides (evergreens).
* **Interconnectivity**: Bidirectional `## Related Articles` footers and cross-cutting reading trails connect ideas across folder boundaries.

## Getting Started

1. Navigate to the relevant topic folder (e.g., `articles/devops/`).
2. Create a new markdown file using `kebab-case.md` (e.g., `my-topic.md`) and include a `## Related Articles` footer.
3. Link it in the index below using title-first format and update the category count.

## Category Directory (109 Articles)

| Category | Articles | Subsections |
| :--- | :---: | :--- |
| [AI](#ai) | 16 | Agents & Tooling (7), Strategy & Impact (9) |
| [Cloud Native](#cloud-native) | 5 | — |
| [Design](#design) | 8 | — |
| [DevOps & Infrastructure](#devops--infrastructure) | 21 | APIs & Specs (6), Auth (4), Git (4), Ops (2), Platform (5) |
| [Distributed Systems](#distributed-systems) | 4 | — |
| [Environment](#environment) | 2 | — |
| [Frontend](#frontend) | 16 | — |
| [Licensing](#licensing) | 1 | — |
| [Philosophy](#philosophy) | 20 | Career (3), Critical Thinking (4), Info & Thought (6), Wellness (4), Programming (3) |
| [Testing](#testing) | 2 | — |
| [Tools](#tools) | 11 | — |
| [Travel](#travel) | 3 | — |

## Cross-Cutting Reading Trails

Topics that span multiple folders can be explored through these curated paths:

* **Security, Identity & Trust:**
  [Understanding OAuth 2.0](devops/understanding-oauth2.md) → [OIDC Introduction & History](devops/oidc-protocol-introduction-and-history.md) → [OIDC in OAuth 2.0 to 2.1](devops/oidc-changes-oauth2-to-oauth21.md) → [Policy Brain: ABAC](devops/policy-brain-abac-and-future.md) → [National-Scale SSO Requirements](design/national-sso-requirements.md) → [RBAC vs. Modular Role-Focused Apps](design/rbac-vs-modular-role-focused-applications.md) → [MITM in Distributed Apps](distributed-systems/mitm-in-heterogeneous-distributed-applications.md) → [Preventing MITM in React + Django](frontend/preventing-mitm-react-django.md)
* **Air-Gapped & Isolated Compute:**
  [Air-Gapped Environment Dev & Deployment](cloud-native/air-gapped-environment-development-deployment.md) → [Multi-Tenant Data Isolation](cloud-native/data-isolation-multi-tenant-multi-stage.md) → [Vercel Sandbox](cloud-native/vercel-sandbox.md) → [Sandbox & Ephemeral Identity Primitives](cloud-native/sandbox-ephemeral-identity-primitive.md) → [Public Font CDNs Anti-Pattern](frontend/airgapped-font-cdn-anti-pattern.md) → [Airgapped Production Font Deployment](frontend/airgapped-production-font-deployment.md)
* **Mental Models & Engineering Longevity:**
  [The Slow Navigator Framework](philosophy/the-slow-navigator-framework.md) → [Chasing Different Phantoms in Info Dev](philosophy/chasing-different-phantoms-in-information-development.md) → [Phantoms in Development & Debugging](philosophy/phantoms-in-development-and-debugging.md) → [Critical Thinking: Managing Emotions](philosophy/critical-thinking-managing-emotions.md) → [Ageless Programming](philosophy/ageless-programming.md) → [The Silent Architecture of Utility Modules](design/silent-architecture-of-utility-modules.md)

## Article Index

### AI

#### Agents & Tooling

- [Antigravity with Stitch: The AI-Powered Development Workflow](ai/antigravity-with-stitch.md)
- [Generative UI for Agents](ai/generative-ui-for-agents.md)
- [How to Connect Google Stitch to Your Workflow: A Step-by-Step Guide](ai/how-to-connect-google-stitch.md)
- [Human in the Loop (HITL) AI](ai/human-in-the-loop.md)
- [MCP: The Future of the Model Context Protocol and Its Alternatives](ai/mcp-future-and-alternatives.md)
- [Tools in AI: The Rise of MCP and the Future of Agentic Systems](ai/tools-in-ai-mcp-and-future.md)
- [Vercel AI SDK 6 Overview](ai/vercel-ai-sdk-6.md)

#### Strategy & Impact

- [AI in Hiring: The Arms Race](ai/ai-in-hiring-the-arms-race.md)
- [AI Microservices Architecture Explained](ai/ai-microservices-architecture-explained.md)
- [API Capabilities for Platforms and AI](ai/api-capabilities-platforms-and-ai.md)
- [Estimating GPU for AI Requirements: VRAM Formulas, Quantization, and Hardware Selection](ai/estimating-gpu-for-ai-requirements.md)
- [Ever-Changing Roles: Navigating Shifts with Tools and AI](ai/ever-changing-roles-tools-and-ai.md)
- [LLM Mindreading: Decoding Brains and Theory of Mind](ai/llm-mindreading.md)
- [Sarvam AI Models: A Comprehensive Guide to India's Sovereign AI Stack](ai/sarvam-ai-models-guide.md)
- [Shadow AI: The Hidden Risk Inside Your Organization](ai/shadow-ai.md)
- [Transitioning from CPU to GPU: A Scalable Deployment Strategy](ai/cpu-to-gpu-transition-strategy.md)

### Cloud Native

- [Air-Gapped Environment Development and Deployment: Data Isolation Behind the Wall](cloud-native/air-gapped-environment-development-deployment.md)
- [Cloud-Native Applications: Architecture, Resilience, and Migration](cloud-native/cloud-native-applications.md)
- [Data Isolation Strategies: Keeping Multi-Tenant and Multi-Stage Data in a Data Silo](cloud-native/data-isolation-multi-tenant-multi-stage.md)
- [Sandbox and Ephemeral Identity Primitives](cloud-native/sandbox-ephemeral-identity-primitive.md)
- [Vercel Sandbox: An Ephemeral Compute Primitive for Untrusted Code](cloud-native/vercel-sandbox.md)

### Design

- [Augmented Reality and Applications: From Healthcare to Entertainment](design/augmented-reality-and-applications.md)
- [National-Scale SSO Requirements: A Checklist for a Billion Users](design/national-sso-requirements.md)
- [Role-Based Access Control (RBAC) vs. Modular Role-Focused Applications](design/rbac-vs-modular-role-focused-applications.md)
- [The Architecture of the "Disposable" Core: Designing for Graceful Obsolescence](design/architecture-of-disposable-core.md)
- [The Evolution of UI Interactions and Aesthetics](design/evolution-of-ui-interactions-and-aesthetics.md)
- [The Purple Renaissance: Design Trends & Aesthetic Evolution (2025–2026)](design/purple-design-aesthetic-trends-2026.md)
- [The Silent Architecture of Utility Modules: Designing Small Helpers That Don’t Break Large Systems](design/silent-architecture-of-utility-modules.md)
- [Varying Goals and Actualities in Design: The Gap Between Intent and Delivery](design/varying-goals-and-actualities-in-design.md)

### DevOps & Infrastructure

#### APIs & Specifications

- [API Health and Future Capabilities: Non-Functional Requirements for APIs](devops/api-health-and-nfr.md)
- [API History and Future: From System Calls to AI-Native Meshes](devops/api-history-and-future.md)
- [Holy Grail: A Journey in Standardization of Strategies for Resource Bundle Consumption](devops/holy-grail-resource-bundle-standardization.md)
- [OpenAPI Specification v3.2.0: Highlights and Changes](devops/openapi-spec-v3-2-0-highlights.md)
- [OpenFeature API Specification: A Vendor-Agnostic Standard for Feature Flags](devops/openfeature-api-spec.md)
- [Understanding Headless Delivery Models: API-First Architecture for Multi-Channel Delivery](devops/understanding-headless-delivery-models.md)

#### Authentication & Authorization

- [OIDC Changes in the OAuth 2.0 to 2.1 Transition](devops/oidc-changes-oauth2-to-oauth21.md)
- [OpenID Connect (OIDC): Introduction, Walkthrough, and History](devops/oidc-protocol-introduction-and-history.md)
- [Policy Brain: ABAC and the Future of Authorization](devops/policy-brain-abac-and-future.md)
- [Understanding OAuth 2.0](devops/understanding-oauth2.md)

#### Git & Version Control

- [Git Worktree vs. Git Branches: Parallel vs. Sequential Workflow Strategies](devops/git-worktree-vs-branches.md)
- [How to Debug Windows Git Pull Issues](devops/debug-windows-git-pull-issues.md)
- [JJ Usage and Git Comparison](devops/jj-usage-and-git-comparison.md)
- [Monorepo vs. Polyrepo: Heterogeneous Projects and the Single Developer Journey](devops/monorepo-polyrepo-single-developer.md)

#### Observability & Operations

- [Replacing the On-Call Engineer with Clopus-Watcher](devops/replacing-on-call-with-clopus-watcher.md)
- [Telemetry: Capturing the Usage](devops/telemetry-capturing-the-usage.md)

#### Platform & Scaling

- [Evolving Platforms and Future Landscapes: From Monoliths to AI-Native IDPs](devops/evolving-platforms-and-future-landscapes.md)
- [From One Machine to Many: The Complete Guide to Learning Docker Compose and Kubernetes](devops/docker-compose-to-kubernetes-guide.md)
- [Kubernetes vClusters: Evolution and Key Changes (2024–2026)](devops/vclusters-evolution-and-changes.md)
- [Scaling From 0 to a Million Users: A Comprehensive Guide](devops/scaling-from-0-to-million.md)
- [Understanding Third-, Second-, and First-Party Providers: A Single-Page Summary](devops/third-party-providers.md)

### Distributed Systems

- [Lightweight Apache Kafka Alternatives](distributed-systems/lightweight-apache-kafka-alternatives.md)
- [Mitigating Man-in-the-Middle (MITM) Attacks in Heterogeneous Distributed Applications (React + Python)](distributed-systems/mitm-in-heterogeneous-distributed-applications.md)
- [The Anatomy of a Distributed Lock and How It Differs from Physical Clocks](distributed-systems/anatomy-of-distributed-lock.md)
- [The Saga Pattern: Managing Distributed Transactions and Eventual Consistency in Microservices](distributed-systems/saga-pattern-distributed-transactions.md)

### Environment

- [Atmospheric Water Generation: Defense Against Air Pollution (2026 Report)](environment/awg-pollution-defense-report-2026.md)
- [The Dynamo Effect: How Celestial Engines Generate Magnetic Shields and Shape Planetary Habitability](environment/dynamo-effect-planetary-magnetic-engines.md)

### Frontend

- [Adding Search to a Markdown-Backed GitHub Pages Site: Open Source & Free Libraries](frontend/github-pages-markdown-search.md)
- [Adding Search to Your Static Site: Open Source & Free Libraries](frontend/static-site-search-open-source.md)
- [Airgapped Production Font Deployment Guide: Auditing, Migrating, and Isolating Google Fonts in React](frontend/airgapped-production-font-deployment.md)
- [Architectural Risk Assessment: Public Font CDNs in Airgapped Environments](frontend/airgapped-font-cdn-anti-pattern.md)
- [Basecoat Alternatives: Framework-Agnostic Component Libraries](frontend/basecoat-alternatives.md)
- [Building Production-Grade Video and Voice Systems with Expo Development Builds](frontend/expo-video-voice-production-builds.md)
- [Cross-Platform Mobile Frameworks: An Open-Source Comparison](frontend/cross-platform-mobile-frameworks-comparison.md)
- [Expo and Verifiable Credential Wallets: Why Dev Builds Replace Expo Go](frontend/expo-dev-builds-for-vc-wallets.md)
- [Meet Ripple: The TypeScript UI Framework for the AI Era](frontend/ripple-framework-summary.md)
- [Microsoft Open Sources XAML Studio: Rapid Prototyping for WinUI](frontend/xaml-studio-open-source-summary.md)
- [Migrating Our DOM to Zig: Summary of Lightpanda's Migration from LibDOM](frontend/migrating-dom-to-zig.md)
- [Open-Source React Native Wallets for Verifiable Credentials](frontend/open-source-react-native-vc-wallets.md)
- [Preventing Man-in-the-Middle (MITM) Attacks in a Decoupled React + Django Architecture](frontend/preventing-mitm-react-django.md)
- [Slint and Node.js: Building Native UIs with JavaScript](frontend/slint-and-nodejs.md)
- [Summary of the htmx Manifesto](frontend/htmx-manifesto-summary.md)
- [TypeScript History, Features, and Timeline](frontend/typescript-history-features-timeline.md)

### Licensing

- [Comparison of The Unlicense and Creative Commons Zero (CC0) License](licensing/unlicense-vs-cc0-comparison.md)

### Philosophy

#### Career & Growth

- [Job Sidequests vs. Hobbies: The Art of XP Management](philosophy/job-sidequests-vs-hobbies.md)
- [Mid-Career Pivot: From Old Hand to New Bee](philosophy/mid-career-pivot.md)
- [Navigating Layoff: A Strategic Guide](philosophy/navigating-layoff-strategic-guide.md)

#### Critical Thinking & Emotions

- [Critical Thinking: Managing Emotions for Objective Results](philosophy/critical-thinking-managing-emotions.md)
- [Critical Thinking: Navigating Emotional Multitudes](philosophy/critical-thinking-emotional-multitudes.md)
- [Postmortem: An Emotional Retrospective](philosophy/postmortem-emotional-retrospective.md)
- [The Slow Navigator: Guardrails Against Stalls, Swerves, and Cognitive Sabotage](philosophy/the-slow-navigator-framework.md) [NEW]

#### Information & Thought

- [Chasing Different Phantoms in Information Development: A Taxonomy](philosophy/chasing-different-phantoms-in-information-development.md)
- [Chasing the Phantom in Information Development](philosophy/chasing-the-phantom-in-information-development.md)
- [Nautical Task Organization for Exploration](philosophy/nautical-task-organization.md)
- [Organizing Thoughts: Different Approaches to Clarity and Structure](philosophy/organizing-thoughts-different-approaches.md)
- [Phantoms in Development and Debugging: A Guide to Elusive Problems in Information Development](philosophy/phantoms-in-development-and-debugging.md)
- [The Domino Effect: From Physical Mechanics to Systems Architecture and Human Behavior](philosophy/the-domino-effect-mechanics-systems-behavior.md)

#### Personal & Wellness

- [Random Acts of Kindness](philosophy/random-acts-of-kindness.md)
- [The Day the Observatory Went Dark: A Fable About Vendor Lock-in](philosophy/vendor-lock-in-fable.md)
- [The Hero's Journey in Tech: A Framework for Understanding Product Transformation](philosophy/heros-journey-tech-quest.md)
- [Wake Up Naturally Without Alarms](philosophy/wake-up-naturally.md)

#### Programming Philosophy

- [Ageless Programming: Timeless Software Design](philosophy/ageless-programming.md)
- [Egoless Programming](philosophy/egoless-programming.md)
- [File Over App: A Manifesto for Digital Longevity](philosophy/file-over-app-manifesto.md)

### Testing

- [Balancing Reuse vs. Functional Script Steps: Arguments and Counter-Arguments](testing/balancing-reuse-vs-functional-steps.md)
- [Implementing Self-Healing Test Scripts with Mocha and Chai](testing/self-healing-test-scripts-mocha-chai.md)

### Tools

- [Alternatives and Progression of NotePad in Windows Environment](tools/notepad-progression-and-alternatives.md)
- [Burp Proxy Alternatives: Open Source and Free Libraries](tools/burp-proxy-alternatives.md)
- [Comparison of Open Source Alternatives to Taskade](tools/taskade-open-source-alternatives.md)
- [From Source to Sandbox: Decoupling the Modern Open-Source Code Editor](tools/decoupling-modern-code-editor.md)
- [Go 1.26: Key Changes and Features](tools/go-1-26-changes.md)
- [Mac OS Shells: A Dive into Open Source Power](tools/mac-os-shells-open-source.md)
- [PodPDF: Free & Open Source Markdown-to-PDF Generator (Bun & Puppeteer)](tools/podpdf-usage-guide.md)
- [The GPM Anchor: Using Google Password Manager as a Cross-Device Sync Bridge](tools/google-password-manager-sync-strategy.md)
- [Top Online Markdown Editors for Uploading to Scribd](tools/markdown-editors-for-scribd-upload.md)
- [Why I Chose WezTerm over Alacritty and Kitty](tools/wezterm-choice.md)
- [Why Neovim Is the Future of Text Editing](tools/neovim-guide.md)

### Travel

- [Glowmads & Wellness Retreats: The New Era of Travel](travel/glowmads-and-wellness-retreats.md)
- [Singapore Tourist & Business Visa Guide for Indian Citizens (2026)](travel/singapore-tourist-business-visa-guide-for-indian-citizens-2026.md)
- [Top IRCTC Prediction Apps in 2026: Your Guide to a Confirmed Seat](travel/irctc-prediction-apps-2026.md)
