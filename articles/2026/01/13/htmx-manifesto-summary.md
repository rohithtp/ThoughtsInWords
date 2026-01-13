# htmx - intro
JavaScript should be used for enhancement, not as the foundation for every simple webpage. HTMX allows developers to build modern, "feeling" apps while staying within the simplicity of the original web model.

# The Case for HTMX: A Manifesto Against Modern Web Bloat

This document summarizes the core arguments and technical philosophy presented by **pleasejusttryhtmx.com**, a critique of modern frontend development that advocates for a return to hypermedia-driven applications.

---

## **I. The Problem: Modern JavaScript Fatigue**

The manifesto argues that the industry has drifted into a state of unnecessary complexity. By defaulting to "SPA-first" frameworks (React, Vue, Angular), developers inherit significant overhead:

* **Massive Dependency Graphs:** Thousands of packages in `node_modules`.
* **Build Chain Fragility:** Hours spent configuring Webpack, Vite, or Babel.
* **State Synchronization Issues:** The constant struggle to keep client-side JSON data in sync with the server database.
* **Mental Overhead:** Managing complex lifecycles and hooks just to perform simple UI updates.

## **II. The Solution: HTMX & Hypermedia**

HTMX proposes that we stop treating the browser as a mere JavaScript runtime and start using it as a true **Hypermedia User Agent**.

### **Key Technical Principles**

1. **Server-Side HTML:** Instead of the server sending JSON and the client rendering it, the server sends **HTML fragments** that are swapped directly into the DOM.
2. **Locality of Behavior (LoB):** Behavior is declared directly on the element.
* *Example:* `<button hx-get="/info" hx-target="#details">Click Me</button>`


3. **The "Hypermedia" Loop:** * **Request:** Any element can trigger an AJAX request (not just `<a>` and `<form>`).
* **Response:** The server responds with plain HTML.
* **Update:** HTMX swaps that HTML into a specific target on the page.



## **III. The Impact (By the Numbers)**

The site highlights that switching from a React-heavy stack to HTMX often results in dramatic efficiency gains:

* **Code Volume:** Up to **67% reduction** in total codebase size.
* **Dependency Count:** Up to **96% fewer** third-party libraries.
* **Performance:** Faster First Contentful Paint (FCP) and no "hydration" lag.

## **IV. Practical Use Cases**

| Use HTMX For... | Stick to React/JS For... |
| --- | --- |
| **Standard CRUD Apps** (Dashboards, Blogs, SaaS) | **High-Fidelity Interaction** (Figma, Canva) |
| **Dynamic Forms** (Validation, dependent inputs) | **Offline-First Apps** (Progressive Web Apps) |
| **Simple Real-time** (Notifications, status bars) | **Heavy Client Computation** (Video editors) |

---

### **Final Verdict**

The manifesto isn't saying JavaScript is "bad"; it’s saying JavaScript should be used for **enhancement**, not as the foundation for every simple webpage. HTMX allows developers to build modern, "feeling" apps while staying within the simplicity of the original web model.
