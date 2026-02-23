# OpenFeature API Specification: A Vendor-Agnostic Standard for Feature Flags

**Source:** [openfeature.dev](https://openfeature.dev/specification/)
**Date:** February 23, 2026

---

## Summary

OpenFeature is an open, vendor-agnostic specification for feature flag evaluation.

Maintained under the **Cloud Native Computing Foundation (CNCF)**, it provides a unified SDK and API surface that decouples application code from any specific feature flag vendor — eliminating vendor lock-in at the flag evaluation layer.

At its simplest, a feature flag is an `if/else` statement controlled at runtime without deploying new code. OpenFeature defines the **contract** that makes this portable across any flag management backend.

---

## What are Feature Flags?

Feature flags (also called feature toggles) are runtime control switches that alter application behavior without code changes or redeployments.

Common use cases:

- **Canary releases** — Roll out a feature to a small subset of users first
- **A/B testing** — Compare user experience across different flag variants
- **Kill switches** — Disable a failing feature instantly during an incident
- **Progressive delivery** — Gradually increase a feature's rollout percentage
- **Geo-gating / compliance** — Restrict features by geography, IP, or user type
- **Dark launching** — Ship code to production but keep it hidden from users

Feature flags require runtime evaluation, contextual awareness, and a dynamic configuration source — all of which demand a proper system, not ad-hoc conditionals.

---

## What is the OpenFeature Specification?

OpenFeature is **not** a feature flag provider. It is a **specification** — a defined contract for how SDKs, providers, and application code interact.

It lets teams swap flag management backends (e.g., LaunchDarkly, Flagsmith, Unleash, or a custom in-house system) without touching application code.

The specification lives at [openfeature.dev/specification](https://openfeature.dev/specification/) and is versioned with clear document-status levels.

---

## Key Components

### 1. Evaluation API

The primary interface application developers interact with. It exposes type-safe methods to resolve flag values at runtime:

- `getBooleanValue(flagKey, defaultValue, context)` — resolves a boolean flag
- `getStringValue(...)`, `getIntegerValue(...)`, `getObjectValue(...)` — typed variants

"Details" methods (e.g., `getBooleanDetails`) return richer resolution metadata — reason, variant, and error codes — enabling observability into *why* a flag resolved a certain way.

### 2. Evaluation Context

A container of arbitrary key-value data passed into flag evaluation. Allows flags to be resolved dynamically based on runtime state.

Three levels of context:

- **Global context** — set once at SDK initialization (e.g., app name, host, environment)
- **Transaction context** — propagated implicitly through middleware (e.g., user session)
- **Invocation context** — passed explicitly at the point of flag evaluation

Contexts merge in a defined order; more-specific contexts take precedence over less-specific ones.

### 3. Providers

The **translation layer** between the OpenFeature Evaluation API and the underlying flag management system. A provider implements a standard interface, mapping generic API calls to the specific API of a backend.

- Abstracts away backend-specific authentication, serialization, and evaluation logic
- Switching flag backends means replacing the provider — not changing application code
- Multiple providers can be registered: a global default and domain-specific overrides

### 4. Hooks

Lifecycle intercepts that run at defined points during flag evaluation: `before`, `after`, `finally`, and `error`.

Hooks can be registered globally, per-provider, or per individual flag call.

Use cases:

- **Logging and telemetry** — emit metrics on every flag evaluation
- **Validation** — assert returned values are within expected bounds
- **Context enrichment** — add data to the evaluation context before evaluation
- **Tracing** — propagate trace context into flag evaluation spans

### 5. Events

Enable reactive patterns tied to provider state changes.

Standard event types defined by the specification:

- `PROVIDER_READY` — provider initialized successfully
- `PROVIDER_ERROR` — provider encountered an unrecoverable error
- `PROVIDER_STALE` — provider's configuration may be out of date
- `PROVIDER_CONFIGURATION_CHANGED` — flag configuration changed at the source

Applications subscribe to events to refresh caches, alert on errors, or trigger reconfigurations without polling.

### 6. Tracking

The Tracking API (a newer addition) lets application authors associate user actions or conversion events with flag evaluations.

This bridges feature flagging with **experimentation**: when a user converts after seeing a specific flag variant, that signal can be attributed back to the flag and variant that influenced it.

---

## Specification Conformance

The specification uses RFC 2119 keywords (`MUST`, `MUST NOT`, `SHOULD`, `MAY`) in normative sections to define binding requirements.

An SDK or provider is **compliant** if it satisfies all `MUST` / `SHALL` requirements.

Document statuses:

- **Experimental** — in active development, subject to breaking changes
- **Hardening** — feature-complete, seeking real-world validation
- **Stable** — finalized, with backward-compatibility guarantees

---

## Why OpenFeature Matters

Without a standard, every team that adopts a feature flag backend becomes coupled to that vendor's SDK throughout their codebase. Migrating backends means touching every flag evaluation call.

With OpenFeature:

- Flag backends become **pluggable infrastructure** — swappable without application changes
- SDKs across languages (JavaScript, Go, Java, Python, .NET, PHP, etc.) expose the same conceptual surface
- Observability, hooks, and events are standardized — not vendor-specific afterthoughts
- CNCF backing ensures community governance and long-term stability

> OpenFeature is to feature flags what OpenTelemetry is to observability — a shared abstraction that commoditizes the integration layer.

---

## Conclusion

The OpenFeature API specification addresses a fragmentation problem that has slowed feature flag adoption for years.

By defining a clear contract for evaluation, context propagation, providers, hooks, and events, it lets organizations adopt feature flagging as a first-class capability — without vendor lock-in.

For teams already using feature flags through a proprietary SDK, migrating to the OpenFeature model buys flexibility, standardized observability, and long-term resilience.

---

## References

- [OpenFeature Official Site](https://openfeature.dev/)
- [OpenFeature Specification](https://openfeature.dev/specification/)
- [OpenFeature Introduction](https://openfeature.dev/docs/reference/intro)
- [Evaluation API Docs](https://openfeature.dev/specification/sections/flag-evaluation)
- [Providers Docs](https://openfeature.dev/specification/sections/providers)
- [Hooks Docs](https://openfeature.dev/specification/sections/hooks)
- [Events Docs](https://openfeature.dev/specification/sections/events)
- [Tracking Docs](https://openfeature.dev/specification/sections/tracking)
- [OpenFeature GitHub](https://github.com/open-feature)
