# Vercel AI SDK 6 Overview
Vercel AI SDK 6 is a major update focused on making AI agents more production-ready, reusable, and safe. The release centers on a new **Agent abstraction** and **Human-in-the-Loop** workflows.

Here is a summary of the key features and improvements:

### 1. New Agent Abstraction

The SDK introduces a formal `Agent` class to simplify how you build and reuse AI logic.

* **Encapsulation:** You can now define an agent’s model, instructions, and tools in a single object. This makes it easier to share agents across different parts of your app (UIs, background jobs, or APIs).
* **ToolLoopAgent:** A pre-built implementation that handles the complexity of "agentic loops." It automatically manages calling the model, executing tools, and feeding results back into the conversation until a task is finished (up to a default 20-step limit).

### 2. Human-in-the-Loop (Tool Approval)

To solve the safety concerns of giving LLMs powerful tools (like deleting files or making payments), SDK 6 introduces a native approval workflow:

* **`needsApproval` Flag:** You can mark specific tools as sensitive.
* **UI Integration:** The `useChat` hook can now detect when a tool requires approval and automatically pause execution to prompt the user for a "Yes/No" before the tool runs.

### 3. Model Context Protocol (MCP) Support

The SDK now has stable support for **MCP**, an open standard for connecting AI models to data sources and tools.

* It allows you to instantly connect to a growing ecosystem of community-built tools for GitHub, Slack, local filesystems, and more without writing custom wrappers.

### 4. Technical Enhancements & DX

* **Reasoning Models:** First-class support for reasoning-focused models like **Anthropic Claude 3.7 Sonnet** and **DeepSeek R1**, including the ability to extract and display "reasoning tokens" (chain-of-thought) separately from the final answer.
* **Strict Mode & Schema Examples:** Tools now support "Strict Mode" to ensure LLM outputs match your Zod schemas exactly, and you can provide examples within the schema to guide the model.
* **Reranking:** Built-in support for reranking models (e.g., Cohere) to improve the accuracy of RAG (Retrieval-Augmented Generation) pipelines.
* **DevTools:** A new debugging interface that allows you to visualize agent steps, prompts, and token usage in real-time.

### 5. Migration & Compatibility

Despite being a version 6 (V6) release, the team has minimized breaking changes. Most existing V5 code should remain compatible, as many of the internal updates focus on the underlying language model specification rather than changing the public API.
