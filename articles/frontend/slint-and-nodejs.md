# Slint and Node.js: Building Native UIs with JavaScript

**Date:** July 13, 2026

## Introduction

The Node.js ecosystem has long excelled at building server-side applications and, through frameworks like Electron, desktop GUIs. But Electron's browser-based rendering comes with a well-known cost: high memory usage, large bundle sizes, and a user experience that never quite feels native. Slint offers a fundamentally different approach. It is a declarative UI toolkit that renders natively — no DOM, no Chromium — while letting you write all of your business logic in JavaScript or TypeScript via first-class Node.js bindings.

This article explores the architecture of Slint, its markup language, its reactive property system, and how it integrates with Node.js to produce lightweight, high-performance desktop and embedded applications.

## What Is Slint?

Slint is an open-source, cross-platform GUI toolkit created by SixtyFPS GmbH (now Slint). It supports Rust, C++, Python, and JavaScript/Node.js as backend languages. Unlike web-based solutions, Slint compiles its UI descriptions ahead of time into optimized native code, which means:

- **No browser engine overhead.** There is no embedded Chromium or WebView. Slint renders directly to its own window using platform-native graphics APIs.
- **Small footprint.** A typical Slint application binary is measured in megabytes, not hundreds of megabytes.
- **True native look and feel.** Slint ships widget styles that match the host platform, and the rendering pipeline is deterministic and GPU-accelerated.

Slint's design philosophy is rooted in the **separation of concerns**: the UI is defined in a domain-specific `.slint` markup language, while the application logic lives entirely in the host language (in our case, JavaScript running on Node.js).

## The `.slint` Markup Language

At the heart of every Slint application is one or more `.slint` files. The language is declarative and purpose-built for describing user interfaces. It borrows ideas from QML, CSS, and modern reactive frameworks, but compiles rather than interprets.

### Core Concepts

- **Components** are the building blocks. Every UI element — a window, a button, a custom widget — is a component.
- **Elements** are the primitives: `Rectangle`, `Text`, `Image`, `TouchArea`, `Flickable`, and so on.
- **Properties** define state. They can be bound to expressions that automatically re-evaluate when dependencies change.
- **Callbacks** handle interactions and bridge the gap between the UI and backend logic.

### A Simple Example

```slint
export component Counter inherits Window {
    title: "Slint Counter";
    width: 320px;
    height: 240px;

    in-out property <int> count: 0;
    callback increment();

    VerticalLayout {
        alignment: center;
        spacing: 12px;

        Text {
            text: "Count: " + root.count;
            font-size: 24px;
            horizontal-alignment: center;
        }

        Button {
            text: "Increment";
            clicked => { root.increment(); }
        }
    }
}
```

This defines a `Counter` component with a reactive `count` property and an `increment` callback. The `Text` element automatically updates whenever `count` changes — no manual DOM diffing, no virtual DOM, no re-renders. The binding expression is tracked at compile time.

## Reactive Properties in Depth

Slint's property system is one of its most distinctive features. Every property assignment is actually a **binding expression**:

```slint
Rectangle {
    width: parent.width * 0.8;
    height: self.width / 2;
    background: self.width > 200px ? #3498db : #e74c3c;
}
```

The runtime tracks which properties each expression depends on. When a dependency changes, the property is marked dirty and lazily re-evaluated. This is similar in spirit to reactive signals (as in SolidJS or Preact Signals) but is resolved at the compiler level rather than at runtime, which makes it extremely efficient.

### Property Qualifiers

Slint distinguishes how properties can be accessed:

| Qualifier | Direction | Use Case |
|-----------|-----------|----------|
| `in` | Set from outside, read inside | Configuration props from the host |
| `out` | Set inside, read from outside | Exposing computed state to the host |
| `in-out` | Read/write from both sides | Two-way data binding |
| (none) | Private to the component | Internal state |

This explicit contract between UI and logic prevents accidental coupling and makes the interface between `.slint` and JavaScript self-documenting.

## Callbacks: The Bridge to Node.js

Callbacks are how the UI communicates intent to your JavaScript code. In the `.slint` file you declare a callback; in JavaScript you attach a handler.

**In `.slint`:**

```slint
export component LoginForm inherits Window {
    in property <string> error-message: "";
    callback submit(string, string);

    // ... UI elements that call root.submit(username, password)
}
```

**In Node.js:**

```javascript
import * as slint from "slint-ui/index.js";

const ui = slint.loadFile("login-form.slint");
const form = new ui.LoginForm();

form.submit = (username, password) => {
    console.log(`Login attempt: ${username}`);

    // Perform async validation, then update the UI
    authenticate(username, password)
        .then(() => { /* navigate away */ })
        .catch(err => {
            form.error_message = err.message;
        });
};

form.run();
```

Note how setting `form.error_message` from JavaScript immediately updates the bound `Text` element in the UI. The property system works bidirectionally across the language boundary.

## Event Loop Integration

A critical engineering detail in Slint's Node.js support is how it bridges two event loops: Slint's internal rendering loop and Node.js's `libuv` event loop. As of mid-2026, Slint integrates these natively rather than using a polling fallback:

1. **Single-threaded coordination.** Both loops run on the main thread. Slint hooks into `libuv`'s idle and prepare handles so that UI rendering happens during Node.js's idle phases.
2. **No busy-waiting.** Earlier versions used a polling interval to check for UI events, which wasted CPU cycles. The current integration uses proper file-descriptor-based notification, meaning the process sleeps when there is nothing to do.
3. **Async-friendly.** Because Slint cooperates with `libuv`, you can use `async/await`, `setTimeout`, `fetch`, and any other Node.js async API alongside the UI without freezing the interface.

This makes Slint + Node.js viable for applications that need to perform I/O-heavy work (database queries, HTTP requests, file system operations) while maintaining a responsive GUI.

## Getting Started

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn
- The Slint VS Code extension (optional but highly recommended for live preview and LSP support)

### Quickstart with the Template

The fastest way to start is with the official template:

```bash
# Clone the template
git clone https://github.com/slint-ui/slint-nodejs-template.git my-app
cd my-app

# Install dependencies (pre-compiled binaries are fetched automatically)
npm install

# Run the application
npm start
```

The template gives you a working project structure:

```
my-app/
├── ui/
│   └── app-window.slint    # UI definition
├── src/
│   └── main.js             # Node.js entry point
├── package.json
└── README.md
```

### From Scratch

If you prefer to set things up manually:

```bash
mkdir my-slint-app && cd my-slint-app
npm init -y
npm install slint-ui
```

Create `ui/main.slint`:

```slint
export component App inherits Window {
    title: "My Slint App";
    width: 400px;
    height: 300px;

    in-out property <string> greeting: "Hello from Slint!";

    Text {
        text: root.greeting;
        font-size: 20px;
        color: #2c3e50;
    }
}
```

Create `src/main.js`:

```javascript
import * as slint from "slint-ui/index.js";

const ui = slint.loadFile("ui/main.slint");
const app = new ui.App();

// Update the greeting after 2 seconds (async-friendly!)
setTimeout(() => {
    app.greeting = "Updated from Node.js!";
}, 2000);

app.run();
```

Run it:

```bash
node src/main.js
```

## When to Choose Slint over Electron

| Consideration | Slint + Node.js | Electron |
|---------------|----------------|----------|
| **Memory footprint** | ~20–50 MB | ~150–500 MB |
| **Bundle size** | ~5–15 MB | ~150+ MB |
| **Startup time** | Sub-second | 2–5 seconds |
| **Web tech reuse** | No (new markup language) | Yes (HTML/CSS/JS) |
| **Ecosystem maturity** | Growing; newer | Very mature |
| **Embedded targets** | First-class support | Not practical |
| **Native rendering** | Yes (GPU-accelerated) | No (Chromium) |

Slint is a strong choice when you need a lightweight, performant, native-feeling application — especially on resource-constrained hardware like Raspberry Pi or industrial panels. If your team already has a large investment in web components and CSS, Electron's familiarity may still win.

## Conclusion

Slint brings something genuinely different to the Node.js desktop application story. By separating UI markup from business logic, compiling declarations into optimized native code, and integrating cleanly with Node.js's event loop, it sidesteps the weight of Electron while preserving the developer experience that JavaScript engineers expect.

As v1.17 (June 2026) continues to stabilize the Node.js bindings and the `.slint` language matures, Slint is positioned as a compelling option for teams that want native performance without leaving the JavaScript ecosystem behind.
