# Open-Source React Native Wallets for Verifiable Credentials

**Date:** July 17, 2026

## Introduction

Focusing strictly on **open-source** frameworks completely changes the layout when building a decentralized identity wallet. It shifts your strategy toward community-backed repositories under the **Linux Foundation's OpenWallet Foundation (OWF)** or open-source reference implementations built by compliant digital ID companies.

Rather than evaluating proprietary vendor SDKs, this article outlines the premier open-source frameworks for implementing an interoperable React Native wallet that supports Verifiable Credentials (VCs) and Verifiable Presentations (VPs). Each framework takes a different architectural stance — from full-stack white-label wallet templates to modular npm packages you can wire into an existing app.

---

## 1. Bifold Wallet + Credo TS (OpenWallet Foundation)

This is the absolute gold standard for a fully open-source React Native decentralized identity wallet. It is hosted directly by the Linux Foundation's OpenWallet Foundation.

### Architecture

**Bifold** provides the UI shell, workflows, and screen flows (QR scanning, credential cards, history), while **Credo TS** (formerly Aries Framework JavaScript) handles the deep cryptographic lifting under the hood.

The separation is clean: Bifold is a React Native application that consumes Credo TS as a dependency. Credo manages DIDComm messaging, credential exchange protocols, secure key storage, and ledger interactions. Bifold handles everything the user sees — onboarding flows, credential card rendering, connection management, and proof request handling.

### Standards Covered

- **W3C Verifiable Credentials (VCs):** Full issuance and verification lifecycle.
- **Decentralized Identifiers (DIDs):** Supports `did:key`, `did:indy`, `did:cheqd`, and extensible to other DID methods.
- **DIDComm v1/v2:** The messaging layer for peer-to-peer credential exchange.
- **OpenID4VCI and OpenID4VP:** Actively being added as modern extensions to support the latest OpenID-based credential issuance and presentation flows.

### Why Choose It

- Completely free and community-governed under the OpenWallet Foundation.
- Heavily production-tested by governments. The Government of British Columbia's **BC Wallet** is a direct offshoot of this framework, deployed to real citizens for real credential use cases.
- The largest contributor community in the open-source decentralized identity space, which means faster bug fixes, broader protocol coverage, and a clear governance roadmap.

### Source Repository

`openwallet-foundation/bifold-wallet` on GitHub.

---

## 2. Procivis One Core React Native SDK

While Procivis offers commercial services, their underlying core stack — including the React Native mobile wrappers — is fully **open-source (Apache-2.0 or dual-licensed)**.

### Architecture

The core cryptographic engine is written in highly optimized, secure **Rust**. Procivis exposes this engine to React Native via a high-performance **JSI (JavaScript Interface) bridge** (`@procivis/react-native-one-core`).

This is a fundamentally different architecture from Credo TS. Where Credo runs cryptographic operations in JavaScript (with polyfills), Procivis compiles Rust to native ARM binaries and calls them synchronously from the JS thread via JSI. The result is significantly faster cryptographic operations and direct access to hardware security modules.

### Standards Covered

- **SD-JWT VC (Selective Disclosure JWT Verifiable Credentials):** First-class support for privacy-preserving selective disclosure.
- **ISO mdoc (mDL):** Mobile Driving License format compliant with ISO/IEC 18013-5.
- **OpenID4VCI:** Credential issuance via the OpenID for Verifiable Credential Issuance specification.
- **OpenID4VP:** Credential presentation via the OpenID for Verifiable Presentations specification, including offline transport layers like **Bluetooth Low Energy (BLE)**.

### Why Choose It

- If you need modern privacy features like **Selective Disclosure (SD-JWT)** or are designing specifically for the **EU Digital Identity (EUDI) framework** architecture, this is the fastest open-source path.
- Native-level hardware security (Secure Enclave on iOS / Android Keystore) is accessible from within React Native, because the Rust core interfaces directly with platform key management APIs.
- The JSI bridge eliminates the serialization overhead of the old React Native bridge, making cryptographic operations feel instantaneous to the user.

### Source Repository

`procivis/one-core-react-native-sdk` on GitHub.

---

## 3. Sphereon SSI SDK (React Native Extension)

Sphereon provides a highly modular, open-source (Apache-2.0) suite of TypeScript packages designed explicitly for OpenID4VC ecosystems.

### Architecture

Rather than forcing you into a specific wallet UI template, Sphereon provides discrete **plug-and-play modules**. Each module handles a single concern:

- A module for **OpenID4VCI** (credential issuance flows).
- A module for **OpenID4VP** (credential presentation flows).
- A module for **W3C VC data parsing and validation**.
- A module for **SD-JWT** creation and verification.
- Crypto extension modules for key management and signing.

You compose these modules together inside your own React Native app. There is no imposed navigation structure, no mandatory UI kit, and no opinionated state management layer.

### Standards Covered

- Highly compliant with the latest drafts of **OpenID4VCI** and **OpenID4VP**.
- Full **W3C Verifiable Credentials** data model support.
- **SD-JWT** creation, parsing, and selective disclosure verification.

### Why Choose It

- If you already have an existing React Native app and you *do not* want to clone an entire white-label wallet repo (like Bifold), Sphereon allows you to `npm install` just the specific open-source protocol handlers you need.
- Maximum flexibility for teams that want to own the UX entirely while outsourcing the protocol complexity to well-maintained, spec-compliant open-source packages.
- Ideal for teams building wallets that must support multiple credential formats simultaneously (e.g., both W3C JSON-LD VCs and SD-JWT VCs in the same application).

### Source Repository

`Sphereon/ssi-sdk-crypto-extensions` on GitHub.

---

## Technical Gotchas of Open-Source Crypto in React Native

When compiling these open-source frameworks, the JavaScript engine embedded in React Native (**Hermes**) cannot compute complex cryptography natively. You must account for these requirements during your build setup.

### 1. Polyfills Are Mandatory

If using pure TypeScript/JS engines like Credo TS, you will need to map Node.js core libraries (`buffer`, `crypto`, `stream`) to React Native equivalents. The typical polyfill stack includes:

- `react-native-get-random-values` — Provides `crypto.getRandomValues()` for secure random number generation.
- `react-native-quick-crypto` — A JSI-based replacement for Node's `crypto` module, significantly faster than pure-JS alternatives.
- `buffer` — The npm `buffer` package, since React Native's Hermes engine does not include Node's `Buffer` global.
- `readable-stream` — A userland implementation of Node.js streams.
- Nodeify shims (e.g., `rn-nodeify` or `react-native-polyfill-globals`) to wire these replacements into the module resolution system.

The order in which these polyfills are imported matters. `react-native-get-random-values` must be imported before any library that calls `crypto.getRandomValues()`, or you will hit a runtime crash on app launch.

### 2. TurboModules / JSI Optimization

The faster open-source frameworks (like Procivis or native OWF extensions) rely on native C++/Rust layers compiled into the app binary. This has build-system implications:

- **You cannot use basic Expo Go.** Expo Go ships a pre-built binary with a fixed set of native modules. Any framework that includes custom native code requires you to create a **custom Expo dev client** (via `expo prebuild`) or eject entirely to bare React Native.
- **Android NDK configuration:** Rust-based cores (Procivis) require the Android NDK to be installed and properly configured in your `local.properties` and Gradle build files. Ensure the NDK version matches what the SDK expects.
- **iOS Xcode build phases:** Native dependencies must be linked correctly in Xcode. CocoaPods is the most common integration path, but some newer SDKs are migrating to Swift Package Manager (SPM).

### 3. Secure Key Storage

All three frameworks need access to platform-level secure storage for cryptographic key material:

- **iOS:** Secure Enclave via the Keychain Services API.
- **Android:** Android Keystore system backed by hardware (StrongBox or TEE).

If your React Native project does not already include a native module for secure key storage (e.g., `react-native-keychain` or a framework-specific binding), you will need to add one. The Procivis SDK handles this internally via its Rust core; Credo TS and Sphereon rely on you providing a key management integration.

---

## Framework Comparison

| Criteria | **Bifold + Credo TS** | **Procivis One Core** | **Sphereon SSI SDK** |
| :--- | :--- | :--- | :--- |
| **Type** | Full wallet application template | SDK with React Native bindings | Modular npm packages |
| **Core Language** | TypeScript | Rust (via JSI bridge) | TypeScript |
| **UI Included** | Yes (complete wallet UI) | No (SDK only) | No (modules only) |
| **SD-JWT Support** | In progress | First-class | First-class |
| **ISO mdoc / mDL** | Limited | First-class | Limited |
| **EUDI Compliance** | Partial | Strong | Partial |
| **Hardware Security** | Via external module | Built-in (Rust ↔ Secure Enclave) | Via external module |
| **Crypto Performance** | JS-bound (with polyfills) | Native (Rust, compiled ARM) | JS-bound (with polyfills) |
| **Best For** | Pre-built wallet apps, government use cases | EU-compliant, high-security wallets | Adding VC/VP to existing apps |

---

## Summary Verdict

- For a **complete, pre-built template application** with a UI ready out of the box, use **OWF Bifold**. It is the most battle-tested open-source wallet in the ecosystem, backed by the Linux Foundation, and proven in government-scale deployments.

- For an **enterprise or EU-compliant system** that needs bleeding-edge protocols like **SD-JWT** and **ISO mdoc**, with blazing-fast performance from a Rust cryptographic core, use the **Procivis One React Native SDK**.

- For **maximum modularity** where you want to surgically add VC/VP capabilities to an existing React Native application without adopting an entire wallet framework, use the **Sphereon SSI SDK**.

All three are genuinely open-source, actively maintained, and designed for interoperability with the emerging standards that will define digital identity for the next decade.
