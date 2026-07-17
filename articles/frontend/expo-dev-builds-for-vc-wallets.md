# Expo and Verifiable Credential Wallets: Why Dev Builds Replace Expo Go

**Date:** July 17, 2026

## Introduction

Short answer: **No, you cannot use vanilla Expo Go** for a production-ready verifiable credentials wallet. However, **yes, you absolutely should use the Expo ecosystem** via **Expo Development Builds**.

This distinction matters because Expo Go and the broader Expo ecosystem are not the same thing — and conflating them is one of the most common mistakes teams make when evaluating whether Expo is viable for decentralized identity applications. Expo Go is a pre-built sandbox. Expo Development Builds are custom-compiled native binaries that retain every developer experience advantage of Expo while removing the native module restrictions entirely.

This article explains exactly why Expo Go falls short for this specific use case, and how the modern Expo workflow solves it.

---

## Why Expo Go Is a Hard "No"

Expo Go is a pre-compiled sandbox application downloaded from the App Store or Google Play. It ships with a fixed set of native modules vetted by the Expo team — things like basic camera access, maps, and file system operations. You install it once, point it at your development server, and your JavaScript bundle runs inside that pre-built container.

This model works brilliantly for the vast majority of mobile applications. But a decentralized identity wallet breaks this sandbox in three critical areas.

### 1. Custom Cryptography and Hardware Security

Wallets require low-level access to the **iOS Secure Enclave** and **Android Keystore** (StrongBox TEE) to generate and store private keypairs that users cannot extract. These are not standard React Native modules — they require custom native code that interfaces directly with platform security hardware.

Expo Go does not expose these specialized cryptographic APIs. When your wallet code attempts to call into the Secure Enclave, the call hits a missing native module and the app crashes at runtime.

### 2. Platform Identity APIs

To act as a legitimate wallet on the device — for example, to handle system-level prompts for digital IDs or Passkeys — you must tap into OS-specific features like Android's **Credential Manager API** or Apple's **WebAuthn/Passkey** handlers.

These APIs require native module registration during the app's build phase. Expo Go's pre-compiled binary does not include these registrations, so the OS has no way to route identity requests to your application.

### 3. Open-Source SDK Dependencies

Heavy-duty open-source SSI frameworks (like Procivis One Core or OWF Credo) use native C++ or Rust implementations exposed via the high-performance **React Native JSI (JavaScript Interface)**. JSI allows synchronous calls from JavaScript into native code without the serialization overhead of the old bridge.

Expo Go fundamentally cannot parse these custom native bindings. The JSI modules are compiled into the app binary at build time, and since Expo Go's binary is pre-built by the Expo team, your custom JSI modules simply do not exist in that binary.

---

## The Solution: Expo Development Builds

You do not need to ditch Expo entirely and go back to a standard React Native "bare" project. In 2026, the modern workflow relies on **Continuous Native Generation (CNG)** and **Development Builds**.

### What Is CNG?

Continuous Native Generation means that the `ios/` and `android/` native project directories are **generated on-the-fly** from your `app.json` configuration and Expo config plugins — rather than being manually maintained source files that you commit to version control. Every time you run `npx expo prebuild`, Expo reads your config, applies all registered plugins, and produces fresh native project files.

This is a fundamental shift from the old "eject and maintain" model. You never need to manually edit Xcode project settings or Gradle build files. Config plugins do it programmatically.

### What Is an Expo Development Build?

Instead of using the generic Expo Go app, you run a single command to generate your own custom native binaries (`.ipa` and `.apk`) tailored precisely to your application. This custom binary acts exactly like Expo Go — offering hot reloading, fast JS development loops, and the Expo Dev Menu — but includes all the custom native code your wallet needs.

```
┌────────────────────────────────────────────────────────┐
│                   Your App Repository                  │
│       (App.js, Screens, Wallet Business Logic)         │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    [ Pure JS / Expo Go ]        [ Expo Dev Builds / CNG ]
    • No custom Rust/C++ modules  • Compiles custom native modules
    • Limited secure storage      • Full hardware Keystore access
    • Protocol libraries CRASH    • Standard for 2026 wallet apps
            ✗                               ✓
```

### The Workflow

1. **Initialize your project** with `npx create-expo-app@latest`.
2. **Install your SSI libraries** — Credo TS, Procivis SDK, Sphereon modules, or any other open-source identity package.
3. **Run `npx expo prebuild`** to generate the native `ios/` and `android/` directories with all custom native modules linked.
4. **Build your dev client** with `npx expo run:ios` or `npx expo run:android`. This compiles a custom binary that includes your JSI modules, hardware security bindings, and platform identity API registrations.
5. **Develop normally.** Your custom dev client connects to the Expo Dev Server, supports Fast Refresh, and behaves identically to Expo Go — except it can run your wallet code without crashing.

You only need to rebuild the native binary when you add or remove a native dependency. Pure JavaScript and TypeScript changes are reflected instantly via Fast Refresh, just like Expo Go.

---

## The 2026 Expo Ecosystem Advantage

By choosing an Expo Managed workflow (using Dev Builds instead of plain Go), you gain instant access to excellent open-source config plugins written specifically for digital wallets.

### expo-secure-store

Expo's built-in `expo-secure-store` module handles hardware-backed encryption out of the box for basic tokens and secrets. It uses the iOS Keychain and Android EncryptedSharedPreferences under the hood.

For a wallet, `expo-secure-store` is sufficient for storing session tokens, user preferences, and non-critical secrets. For actual cryptographic key material (DID private keys, signing keys), you will need the deeper hardware security integration provided by your SSI framework or a dedicated Keychain/Keystore module.

### @animo-id/expo-digital-credentials-api

This is a specialized open-source Expo module created by the Animo community specifically to link React Native applications directly into Android's native **Digital Credentials API**. It handles:

- Registration of your app as a credential holder with the Android Credential Manager.
- Receiving and responding to credential presentation requests (SD-JWT VCs, mdocs).
- Integrating with the system-level identity UI that Android presents to users when a verifier requests credentials.

This module is distributed as an Expo config plugin, meaning you add it to your `app.json` and run `npx expo prebuild` — no manual Gradle editing required.

### expo-local-authentication

For biometric gating (requiring Face ID or fingerprint before revealing credentials), `expo-local-authentication` provides a clean cross-platform API. It wraps iOS Local Authentication (Face ID / Touch ID) and Android BiometricPrompt.

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Starting with Expo Go and Migrating Later

Some teams start prototyping with Expo Go and plan to "switch to Dev Builds later." This creates a false sense of progress — your prototype will work until the moment you try to import a real identity SDK, at which point it crashes. Start with Dev Builds from day one.

### Pitfall 2: Forgetting to Prebuild After Adding Native Deps

When you `npm install` a package that includes native code, your JavaScript bundle will resolve the import, but the native module will be missing from the binary. You must run `npx expo prebuild --clean` and rebuild your dev client. The `--clean` flag ensures the native directories are regenerated from scratch, avoiding stale configuration.

### Pitfall 3: Committing the ios/ and android/ Directories

With CNG, the `ios/` and `android/` directories are generated artifacts — like `node_modules/`. Add them to `.gitignore`. Committing them defeats the purpose of CNG and leads to merge conflicts when config plugins update native files.

### Pitfall 4: Using EAS Build Without Understanding CNG

Expo Application Services (EAS) Build runs `npx expo prebuild` in the cloud before compiling your app. If your config plugins or native dependencies have undeclared system requirements (e.g., a specific NDK version for Rust compilation), the cloud build may fail in ways that are difficult to debug remotely. Always verify that `npx expo prebuild && npx expo run:ios` works locally before pushing to EAS Build.

---

## Summary

| Approach | Wallet Viable? | Developer Experience | Native Module Support |
| :--- | :--- | :--- | :--- |
| **Expo Go** | No | Excellent (no build step) | Pre-built modules only |
| **Expo Dev Builds (CNG)** | Yes | Excellent (rebuild only on native changes) | Full custom native support |
| **Bare React Native** | Yes | Good (manual native config) | Full custom native support |

### Verdict

Skip the standard **Expo Go** app to avoid immediate runtime crashes when importing identity packages. Initialize your project using `create-expo-app`, install the open-source SSI libraries you need, and immediately spin up an **Expo Development Build**.

You get all the developer experience benefits of Expo — Fast Refresh, config plugins, EAS Build, OTA updates for JS changes — with none of the native module restrictions that make Expo Go incompatible with cryptographic wallet requirements.
