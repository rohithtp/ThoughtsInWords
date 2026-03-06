# Telemetry: Capturing the Usage

**Date:** March 6, 2026

## Summary

Telemetry is the automated collection, transmission, and analysis of data about how a system or product is actually used in the real world. It bridges the gap between what we *think* users do and what they *actually* do. For software teams, telemetry is the difference between building blindly and building with purpose.

Good telemetry answers the fundamental question: *Is this feature being used — and is it working?*

## What Is Telemetry?

Telemetry refers to the measurement and transmission of data from remote or distributed sources to a central system for monitoring and analysis. In software, this covers:

- **Events** — discrete actions taken by users (e.g., clicking a button, opening a page)
- **Metrics** — numerical measurements over time (e.g., API response time, error rate)
- **Traces** — the path of a request as it flows through a distributed system
- **Logs** — timestamped records of system behavior and state

Together, these four signals form the foundation of **observability** — the ability to understand a system's internal state from its external outputs.

## Why It Matters

Without telemetry, teams are guessing. With it, they can:

- **Validate assumptions** — did the change you shipped actually improve the experience?
- **Detect problems early** — catch regressions before users file support tickets
- **Prioritize roadmap work** — invest in features that are actually used, deprecate those that aren't
- **Understand failure modes** — see exactly where and why things go wrong in production
- **Measure adoption** — track how new features spread across a user base over time

Telemetry is not just a DevOps concern. It is deeply tied to product design, engineering culture, and business decision-making.

## Usage Telemetry vs. System Telemetry

There are two primary flavors of telemetry worth distinguishing.

### System Telemetry

Focuses on the health and performance of the infrastructure. Examples include:

- CPU and memory utilization
- Error rates and HTTP status codes
- Service latency and throughput
- Disk I/O and network traffic

This is the domain of **Site Reliability Engineering (SRE)** and monitoring tools like Prometheus, Grafana, or Datadog.

### Usage Telemetry

Focuses on *human behavior* within the product. Examples include:

- Which features are accessed and how often
- User flows and drop-off points
- Session duration and engagement patterns
- Feature flag exposure and conversion

This is the domain of **product analytics** tools like Mixpanel, Amplitude, or custom event pipelines.

The best teams instrument both layers and use them together.

## Key Design Principles

### Instrument with Intent

Don't track everything — track the right things. Before adding instrumentation, ask:

- What decision will this data inform?
- Who will act on this signal?
- How often will this data be reviewed?

Tracking noise without intent creates dashboards nobody looks at.

### Name Events Clearly

Event naming conventions matter enormously as telemetry scales. A consistent taxonomy — like `object_action` (e.g., `document_published`, `user_signed_in`, `feature_toggled`) — makes querying and analysis far simpler than ad-hoc names scattered across codebases.

### Capture Enough Context

An event without context is nearly useless. Enrich events with:

- **Session identifiers** — tie events to a user journey
- **Environment** — production vs. staging vs. development
- **Version** — which release was the user on?
- **Entity identifiers** — which document, workspace, or tenant?

### Respect Privacy

Telemetry can quickly cross into surveillance. Best practices include:

- Collect only what is strictly necessary
- Anonymize or pseudonymize personally identifiable information (PII)
- Be transparent — document what is collected and why
- Comply with regulations such as GDPR and CPRA
- Provide opt-out mechanisms where applicable

## Instrumentation Patterns

### Client-Side Instrumentation

Events are emitted directly from the browser or native app. This offers rich behavioral data but is subject to ad blocker interference and can leak sensitive data if not carefully controlled.

### Server-Side Instrumentation

Events are captured at the API boundary or within backend services. More reliable and harder to block, but may miss pure client interactions (e.g., hover behavior, scroll depth).

### Hybrid Approaches

Many mature products combine both: client-side for UX signals, server-side for authoritative action confirmation (e.g., confirming a purchase has truly completed).

## Telemetry and Feature Flags

Telemetry and feature flags are natural partners. When a flag rolls out a feature to a subset of users, telemetry answers whether the experience changed for those users — in terms of engagement, errors, and performance.

This pairing enables **controlled experimentation**: instead of shipping and hoping, teams ship to a defined cohort, measure the delta, and decide whether to expand or revert.

## From Data to Decision

Raw telemetry is not insight. The pipeline from collection to decision typically involves:

1. **Collection** — SDKs, agents, or server-side hooks emit events
2. **Ingestion** — a stream processing system (e.g., Kafka, Kinesis) receives events at scale
3. **Storage** — events land in a data warehouse or time-series database
4. **Query & Analysis** — teams use SQL, dashboards, or notebooks to explore the data
5. **Action** — product or engineering decisions are made based on the findings

Each stage is a potential point of failure or delay. Investing in the pipeline is as important as investing in the instrumentation itself.

## Signals Worth Watching

Some telemetry signals are especially high-signal across many types of products:

- **Feature adoption rate** — percentage of eligible users/sessions that trigger a feature at least once
- **Error rate by feature** — errors concentrated in specific flows reveal fragile surfaces
- **Performance by path** — latency that degrades on specific user journeys exposes optimization targets
- **Funnel completion rate** — how many users who start a key flow actually finish it?
- **Return frequency** — how often do users come back to a specific capability?

## Common Pitfalls

- **Sampling without stratification** — sampling 10% of events can hide rare but critical failure modes
- **Missing baseline** — telemetry before a change is as important as telemetry after it
- **Dashboard sprawl** — too many dashboards means no single source of truth
- **Ignoring the long tail** — outlier behaviors often reveal the most important edge cases
- **Alert fatigue** — too many alerts trained on noisy signals causes on-call teams to tune out

## Conclusion

Telemetry is not about surveillance — it is about clarity. It transforms assumptions into evidence and opinions into data. The teams that build effective telemetry pipelines are not just better at debugging production issues; they are better at making product decisions, prioritizing engineering effort, and understanding what value they are actually delivering.

The goal is not to collect more data. The goal is to ask better questions — and build the instrumentation that answers them.
