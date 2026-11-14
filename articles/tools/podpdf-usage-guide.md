---
title: "PodPDF: Open-Source Markdown to PDF with Bun"
date: 2026-01-18
tags: [bun, pdf, open-source, markdown, tools]
---

# PodPDF: Free & Open Source PDF Generator

PodPDF is a lightweight, open-source utility powered by **Bun** to convert Markdown files into professional PDFs. Unlike paid SaaS solutions, PodPDF runs locally on your machine, ensuring **zero cost**, total privacy, and lightning-fast performance.

This guide provides a checklist of steps to build and use the PodPDF script locally.

## 🚀 Setup Checklist

Get your environment ready for PodPDF.

- [ ] **Install Bun**: Ensure Bun is installed on your system.
- [ ] **Initialize Project**:
    - [ ] Create a folder: `mkdir podpdf && cd podpdf`
    - [ ] Initialize Bun: `bun init -y`
- [ ] **Install Dependencies**:
    - [ ] `bun add puppeteer` (Headless browser for PDF generation)
    - [ ] `bun add markdown-it` (Markdown parser)
    - [ ] `bun add -d @types/markdown-it` (Types for TypeScript)

## �️ Implementation Checklist

Create the `podpdf.ts` script to handle the conversion.

### The Script (`podpdf.ts`)

- [ ] **Import Libraries**: Import `puppeteer` and `markdown-it`.
- [ ] **Read Arguments**: Capture input and output filenames from `process.argv`.
- [ ] **Render HTML**: Convert Markdown to HTML and inject basic CSS styles.
- [ ] **Print PDF**: Use Puppeteer to `printToPDF`.

```typescript
import puppeteer from "puppeteer";
import MarkdownIt from "markdown-it";

const md = new MarkdownIt();
const inputFile = process.argv[2];
const outputFile = process.argv[3] || "output.pdf";

if (!inputFile) {
  console.error("Usage: bun podpdf.ts <input.md> [output.pdf]");
  process.exit(1);
}

try {
  // 1. Read Markdown
  const markdown = await Bun.file(inputFile).text();

  // 2. Convert to HTML with basic styling
  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          body { font-family: 'Helvetica', sans-serif; padding: 40px; line-height: 1.6; }
          h1 { border-bottom: 2px solid #333; padding-bottom: 10px; }
          table { width: 100%; border-collapse: collapse; margin: 20px 0; }
          th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
          th { background-color: #f4f4f4; }
          code { background: #f4f4f4; padding: 2px 5px; border-radius: 4px; }
        </style>
      </head>
      <body>
        ${md.render(markdown)}
      </body>
    </html>
  `;

  // 3. Generate PDF
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: "networkidle0" });
  await page.pdf({ path: outputFile, format: "A4", printBackground: true });

  await browser.close();
  console.log(`✅ PDF created: ${outputFile}`);

} catch (error) {
  console.error("Error generating PDF:", error);
}
```

## � Usage Checklist

Once your script is ready, follow this flow to generate a PDF.

### 1. Prepare Your Content
- [ ] Create a Markdown file (e.g., `invoice.md`).
- [ ] Use standard Markdown syntax (headers, lists, tables).
- [ ] Verify standard assets (local images should be relative paths).

### 2. Run the Converter
- [ ] Execute `bun podpdf.ts invoice.md invoice.pdf`
- [ ] Check the directory for the output file.

## 💡 Quick Example: Simple Invoice

Create a file named `invoice.md` with the following content to test your setup.

```markdown
# Invoice #001

**From:** My Company Inc.
**To:** Jane Doe

| Item | Qty | Price |
| :--- | :-- | :---- |
| Consulting | 10 | $1500 |
| Setup Fee  | 1  | $200  |

**Total: $1700**
```

Run:
```bash
bun podpdf.ts invoice.md invoice.pdf
```

By following this guide, you have a completely **free**, **open-source**, and **customizable** PDF generator using the power of Bun.
