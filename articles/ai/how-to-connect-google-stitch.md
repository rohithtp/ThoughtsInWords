# How to Connect Google Stitch to Your Workflow: A Step-by-Step Guide

**Date:** July 24, 2026

Google Stitch has emerged as a powerful AI-driven UI/UX design tool, enabling developers and designers to generate responsive, high-fidelity layouts from simple text prompts. While Stitch is impressive on its own, its true power is unlocked when connected to your broader development workflow—whether that means exporting to Figma or integrating directly with an agentic IDE like Antigravity via the Model Context Protocol (MCP).

Here is a step-by-step guide on how to connect and integrate Google Stitch into your daily development process.

## Prerequisites

Before starting, ensure you have:
- A valid Google Account.
- (Optional) A Figma account, if you intend to export designs for further manual refinement.
- (Optional) The **Antigravity IDE** installed, if you are setting up an autonomous code-generation pipeline via MCP.

---

## Step 1: Access and Authenticate

The first step is to gain access to the Stitch environment.

1. Navigate to the official portal at **[stitch.withgoogle.com](https://stitch.withgoogle.com/)**.
2. Click on **Sign In** and authenticate using your Google Account credentials.
3. If you are accessing the tool for the first time, you may need to accept the terms of service for Google Labs experimental tools. 
4. Once authenticated, you will be directed to the main Stitch workspace where you can start a new project.

## Step 2: Generate Your Base Design

Before connecting Stitch to an external tool, you need a design context.

1. In the prompt bar, describe the UI you want to create (e.g., *"A modern, dark-mode dashboard for a SaaS analytics platform featuring a sidebar, a line chart, and user activity cards"*).
2. You can also upload reference wireframes or sketches to guide the AI.
3. Allow Stitch (powered by Gemini) to generate the initial UI components. 
4. Use conversational prompts to iterate on the "vibe," adjusting the color palette, typography, and layout until you are satisfied.

---

## Step 3: Choose Your Connection Strategy

Depending on your team's workflow, you can connect Stitch to your downstream tools in two primary ways:

### Option A: Connecting to Figma (Designer-Led Workflow)

If your team requires granular control over vector graphics and design tokens:
1. In the Stitch workspace, locate the **Export** or **Share** button in the top right corner.
2. Select **Export to Figma**.
3. You will be prompted to authenticate your Figma account. Grant Stitch the necessary permissions.
4. Stitch will generate a new Figma file in your drafts, containing fully structured frames, auto-layouts, and design tokens ready for developer handoff.

### Option B: Connecting to Antigravity IDE via MCP (Agent-Led Workflow)

For developers looking to jump straight from design to production-ready code:
1. Open your **Antigravity IDE**.
2. Navigate to your MCP Configuration settings (usually found in `~/.config/antigravity/mcp.json` or via the IDE's extension manager).
3. Add the **Stitch MCP Server** to your configuration. You will need an API key or an OAuth token generated from your Google Cloud Console / AI Studio associated with your Stitch account.
4. Start the MCP server within Antigravity. 
5. In your IDE's agent chat, you can now prompt the coding agent: *"Connect to my latest Google Stitch project and generate the React components for the dashboard."*
6. The IDE will pull the design context directly from Stitch and begin writing the code in your workspace.

---

## Step 4: Iterate and Sync

Whether you are using Figma or Antigravity, connection is not a one-time event. 
- **Continuous Syncing:** If you make changes in Stitch, you can re-trigger the export or ask your Antigravity agent to pull the latest design diffs.
- **Feedback Loops:** Because Stitch understands conversational instructions, you can easily paste a screenshot of your coded UI back into Stitch and ask it how to fix any visual discrepancies between the code and the design.

## Conclusion

Connecting Google Stitch effectively bridges the gap between rapid ideation and concrete implementation. By integrating it into Figma or leveraging MCP for direct IDE access, you can significantly reduce the friction of the design-to-code lifecycle, keeping your focus on building great products rather than translating mockups.
