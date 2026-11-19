#!/usr/bin/env python3
"""Stateful multi-turn review_article orchestration script for Antigravity `run_workflow` (Option B4 + A4).

Invoke via `run_workflow`:
  run_workflow(
      ScriptPath="/abs/path/to/.agent/skills/review_article/scripts/run_review_workflow.py",
      Args={"article_path": "articles/<category>/<slug>.md"},
      Description="Run 5-stage schema-validated multi-persona article review",
  )
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Resolve workspace root cleanly inside `run_workflow`
_workspaces = globals().get("WORKSPACES", ())
REPO_ROOT = Path(_workspaces[0]) if _workspaces else Path.cwd()
SCRIPTS_DIR = REPO_ROOT / ".agent" / "skills" / "review_article" / "scripts"
RECONCILER_SCRIPT = REPO_ROOT / ".agent" / "skills" / "organize_readme" / "scripts" / "reconcile_indexes.py"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from schemas import (  # noqa: E402
    AFTER_SCORECARD_SCHEMA,
    BEFORE_SCORECARD_SCHEMA,
    INDEX_HANDOFF_SCHEMA,
    REMEDIATION_RESULT_SCHEMA,
    compute_scorecard,
    render_review_report,
    validate_against_schema,
)


def _format_long_date(dt: datetime) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def _format_short_date(dt: datetime) -> str:
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def _validate_article_path(raw_path: str) -> tuple[Path, str, str, str]:
    rel_path = raw_path.strip().lstrip("./")
    m = re.match(r"^articles/([a-z0-9-]+)/([a-z0-9-]+)\.md$", rel_path)
    if not m:
        raise ValueError(
            f"article_path must match 'articles/<category>/<kebab-case>.md', got: {raw_path!r}"
        )
    abs_path = REPO_ROOT / rel_path
    if not abs_path.is_file():
        raise FileNotFoundError(f"Target article does not exist on disk: {abs_path}")
    return abs_path, rel_path, m.group(1), m.group(2)


async def run_pipeline() -> dict[str, Any]:
    wf_args: dict[str, Any] = globals().get("args", {}) or {}
    raw_article_path = wf_args.get("article_path", "")
    if not raw_article_path:
        raise ValueError("Missing required workflow arg 'article_path' (e.g. 'articles/devops/example.md').")

    abs_article_path, article_rel_path, category, slug = _validate_article_path(raw_article_path)
    report_rel_path = f"reviews/{category}/{slug}-review.md"
    abs_report_path = REPO_ROOT / report_rel_path
    today_dt = datetime.now()
    today_long = _format_long_date(today_dt)

    # Read minimal header metadata from target article for context logging
    article_head = abs_article_path.read_text(encoding="utf-8")[:1500]
    title_m = re.search(r"^#\s+(.+?)\s*$", article_head, flags=re.MULTILINE)
    initial_title = title_m.group(1).strip() if title_m else slug

    log(f"Starting Option B4 review pipeline for {article_rel_path} ('{initial_title}')")

    # ------------------------------------------------------------------
    # Stage 1: Persistent Read-Only Reviewer Definitions & Parallel Audit
    # ------------------------------------------------------------------
    phase("Stage 1: Parallel Multi-Persona Before Audit")

    read_only_guard = (
        "CRITICAL READ-ONLY CONSTRAINT: You are an independent read-only auditor. "
        "Do NOT call write_file, edit_file, or any mutating run_command. "
        "Read the target article and the rubric/repository files referenced below, "
        "then submit your structured JSON output strictly via the `finish` tool."
    )

    reader_standing = (
        f"You are the Reader Mode Reviewer for ThoughtsInWords (Parameters 1–4).\n"
        f"{read_only_guard}\n\n"
        "Prerequisites to read before scoring:\n"
        f"1. Target article: `{article_rel_path}`\n"
        "2. Rubric Parameters 1–4: `.agent/skills/review_article/references/rubric-and-repo-alignment.md`\n\n"
        "Owned Parameters (0.0–10.0, use 0.5 or 1.0 increments):\n"
        "- param_id 1: Executive Clarity & Hook (`## Summary` & `## Key Points`)\n"
        "- param_id 2: Narrative Flow & Cognitive Load\n"
        "- param_id 3: Visual Aids & Scannability\n"
        "- param_id 4: Accessibility & Actionable Takeaway\n"
        "Use recommendation IDs formatted strictly as `R-01`, `R-02`, etc."
    )

    sme_standing = (
        f"You are the Subject Matter Expert (SME) Reviewer for ThoughtsInWords (Parameters 5–8).\n"
        f"{read_only_guard}\n\n"
        "Prerequisites to read before scoring:\n"
        f"1. Target article: `{article_rel_path}`\n"
        "2. Governance rules (especially Invariant 1 Pure Open-Source Systems Mandate): `.agent/rules/AGENTS.md`\n"
        "3. Rubric Parameters 5–8: `.agent/skills/review_article/references/rubric-and-repo-alignment.md`\n\n"
        "Owned Parameters (0.0–10.0, use 0.5 or 1.0 increments):\n"
        "- param_id 5: Technical & Domain Accuracy\n"
        "- param_id 6: Depth of Insight & Edge Cases\n"
        "- param_id 7: Citations, Specifications & Evidence\n"
        "- param_id 8: Domain Completeness & Currency\n"
        "Audit every tool, platform, or framework claim for OSI-approved pure open-source compliance (Invariant 1). "
        "Set `invariant1_violation: true` on any recommendation fixing proprietary/open-core/SaaS inclusion or missing licensing notes. "
        "Use recommendation IDs formatted strictly as `S-01`, `S-02`, etc."
    )

    arch_standing = (
        f"You are the Technical Architect & Repo Concept Steward for ThoughtsInWords (Parameters 9–12).\n"
        f"{read_only_guard}\n\n"
        "Prerequisites to read before scoring:\n"
        f"1. Target article: `{article_rel_path}`\n"
        "2. Governance rules (Invariants 1–3): `.agent/rules/AGENTS.md`\n"
        "3. Rubric Parameters 9–12 & Philosophy Checklist: `.agent/skills/review_article/references/rubric-and-repo-alignment.md`\n"
        "4. Repository philosophy & digital garden index: `README.md` and `articles/README.md`\n\n"
        "Owned Parameters (0.0–10.0, use 0.5 or 1.0 increments):\n"
        "- param_id 9: Architectural Soundness & Trade-Off Rigor (pure open-source NFRs, blast radius, when NOT to use)\n"
        "- param_id 10: ThoughtsInWords Philosophy Alignment (guard explicitly against the 'Engineer's Philosophy' pitfall of oversimplifying systemic/human problems)\n"
        "- param_id 11: Digital Garden Interconnectivity (check `articles/README.md` for 2–4 valid relative `.md` cross-links)\n"
        "- param_id 12: Repository Lifecycle & Standards Compliance (`kebab-case.md`, immutable `**Date:**`, `**Last Updated:**`, `**Review:**`, `Scope & Licensing Note`, bottom section order)\n"
        "Populate `pure_oss_audit` and `philosophy_alignment_notes`. Use recommendation IDs formatted strictly as `A-01`, `A-02`, etc."
    )

    r_reader = agent(reader_standing, role="Reader Mode Reviewer (Params 1-4)")
    r_sme = agent(sme_standing, role="Subject Expert Reviewer (Params 5-8)")
    r_arch = agent(arch_standing, role="Technical Architect Reviewer (Params 9-12)")

    before_tasks = [
        (
            r_reader,
            f"Perform the Stage 1 (Before) audit of `{article_rel_path}` for persona `'Reader Mode'` (param_ids 1, 2, 3, 4). "
            "Read the target article and rubric now, then finish with your BEFORE_SCORECARD_SCHEMA payload.",
        ),
        (
            r_sme,
            f"Perform the Stage 1 (Before) audit of `{article_rel_path}` for persona `'Subject Expert'` (param_ids 5, 6, 7, 8). "
            "Read the target article, `.agent/rules/AGENTS.md`, and rubric now, then finish with your BEFORE_SCORECARD_SCHEMA payload.",
        ),
        (
            r_arch,
            f"Perform the Stage 1 (Before) audit of `{article_rel_path}` for persona `'Technical Architect'` (param_ids 9, 10, 11, 12). "
            "Read the target article, `.agent/rules/AGENTS.md`, `README.md`, `articles/README.md`, and rubric now, then finish with your BEFORE_SCORECARD_SCHEMA payload.",
        ),
    ]

    before_payloads = await parallel(
        before_tasks,
        lambda item: item[0](item[1], schema=BEFORE_SCORECARD_SCHEMA),
    )
    del before_tasks

    # ------------------------------------------------------------------
    # Stage 2 & 3: Synthesize Recommendations & Remediate Target Article
    # ------------------------------------------------------------------
    phase("Stage 2 & 3: Synthesize & Remediate Target Article")

    priority_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    merged_recs: list[dict[str, Any]] = []
    for p in before_payloads:
        for rec in p["recommendations"]:
            merged_recs.append({"persona": p["persona"], **rec})
    merged_recs.sort(key=lambda r: (priority_rank.get(r["priority"], 9), r["id"]))

    log(f"Synthesized {len(merged_recs)} prioritized recommendations across 3 reviewer personas.")

    remediator_prompt = (
        f"You are the scoped Article Remediator for ThoughtsInWords.\n"
        f"Target Article: `{article_rel_path}`\n"
        f"Today's Date: `{today_long}`\n"
        f"Target Review Report Link: `../../{report_rel_path}`\n\n"
        "STRICT WRITE SCOPE (Option A4 Single-Writer Partitioning):\n"
        f"- You MUST edit ONLY `{article_rel_path}`.\n"
        "- Do NOT edit `README.md`, `articles/README.md`, `articles/CHANGELOG.md`, `reviews/README.md`, or the review report file. Those are handled by Python and `reconcile_indexes.py` in Stages 4–5.\n\n"
        "Mandatory Governance Rules (`.agent/rules/AGENTS.md`):\n"
        "1. Invariant 1 (Pure Open-Source Mandate): Replace or omit any proprietary, SaaS, commercial-only, or open-core ('Community Edition') tools in prose, tables, and Mermaid diagrams with pure OSI-approved open-source equivalents. Add the exact `Scope & Licensing Note` callout if covering tooling/systems and missing.\n"
        "2. Invariant 3 (Immutable Header & Bottom Ordering):\n"
        "   - NEVER alter or remove the original `**Date:** Month Day, Year`.\n"
        f"   - Add or update `**Last Updated:** {today_long}` directly beneath `**Date:**`.\n"
        f"   - Add or update `**Review:** [Expert & Architecture Review Report](../../{report_rel_path})` directly beneath `**Last Updated:**`.\n"
        "   - Preserve ALL existing valid citations, `## References`, and inline links.\n"
        "   - Order bottom sections strictly as: `## Related Articles` (2–4 valid relative `.md` links verified against `articles/README.md`) -> `## References` (if present) -> `## Changelog` (at very bottom, prepending `- **Mon DD, YYYY:** Completed multi-persona review (Reader, SME, Technical Architect); applied improvements ([Review Report](../../"
        f"{report_rel_path})).`).\n\n"
        "Prioritized Stage 1 Recommendations to Apply:\n"
        f"```json\n{json.dumps(merged_recs, indent=2)}\n```\n\n"
        "Ensure all technical additions maintain clean Reader Mode pacing (tables, Mermaid diagrams, concise bullets). "
        "Return your result strictly via `finish` matching REMEDIATION_RESULT_SCHEMA."
    )

    remediation = await agent(
        remediator_prompt,
        schema=REMEDIATION_RESULT_SCHEMA,
        role="Article Remediator (Scoped)",
        workspace="inherit",
    )

    # ------------------------------------------------------------------
    # Stage 4: Stateful Multi-Turn After Re-Verification & Report Render
    # ------------------------------------------------------------------
    phase("Stage 4: Stateful Multi-Turn After Re-Verification & Report Rendering")

    def _make_after_prompt(persona: str, param_range: str, before_data: dict[str, Any]) -> str:
        rec_ids = [r["id"] for r in before_data["recommendations"]]
        return (
            f"The target article `{article_rel_path}` has now been revised in Stage 3.\n"
            f"Applied recommendation IDs reported by remediator: {remediation['applied_recommendation_ids']}\n"
            f"Your Stage 1 recommendation IDs to verify: {rec_ids}\n\n"
            f"Instructions for persona '{persona}' (Parameters {param_range}):\n"
            f"1. Re-read `{article_rel_path}` completely (stay strictly read-only).\n"
            "2. Verify every Stage 1 recommendation you raised and mark its status accurately as `'Applied'` or `'Deferred'`.\n"
            "3. Re-score ONLY your 4 parameters (0.0–10.0, 0.5/1.0 increments) strictly against the actual text on disk. "
            "Do NOT inflate scores if recommendations remain `'Deferred'` or unresolved.\n"
            "4. Submit your AFTER_SCORECARD_SCHEMA payload via `finish`."
        )

    after_tasks = [
        (r_reader, _make_after_prompt("Reader Mode", "1–4", before_payloads[0])),
        (r_sme, _make_after_prompt("Subject Expert", "5–8", before_payloads[1])),
        (r_arch, _make_after_prompt("Technical Architect", "9–12", before_payloads[2])),
    ]

    after_payloads = await parallel(
        after_tasks,
        lambda item: item[0](item[1], schema=AFTER_SCORECARD_SCHEMA),
    )
    del after_tasks, r_reader, r_sme, r_arch

    scorecard = compute_scorecard(before_payloads, after_payloads)
    if scorecard["anti_inflation_clamps"]:
        log(f"Anti-inflation clamps applied: {json.dumps(scorecard['anti_inflation_clamps'])}")

    review_date_long = remediation.get("last_updated") or today_long
    report_md = render_review_report(
        article_title=remediation["article_title"],
        category=category,
        slug=slug,
        review_date=review_date_long,
        remediation=remediation,
        scorecard=scorecard,
    )

    abs_report_path.parent.mkdir(parents=True, exist_ok=True)
    abs_report_path.write_text(report_md, encoding="utf-8")
    log(f"Wrote deterministic Check 7 report to {report_rel_path}")

    # ------------------------------------------------------------------
    # Stage 5: Single-Writer Index Reconciliation & Verification Gate
    # ------------------------------------------------------------------
    phase("Stage 5: Single-Writer Index Reconciliation & Verification Gate")

    try:
        parsed_review_dt = datetime.strptime(review_date_long.strip(), "%B %d, %Y")
    except ValueError:
        parsed_review_dt = today_dt

    handoff_payload = {
        "action": "Reviewed & Updated",
        "article_path": article_rel_path,
        "title": remediation["article_title"],
        "date": remediation["date"],
        "last_updated": review_date_long,
        "changelog_summary": remediation["changelog_summary"],
        "review_move": {
            "report_path": report_rel_path,
            "before_score": scorecard["overall"]["before"],
            "after_score": scorecard["overall"]["after"],
            "delta": scorecard["overall"]["delta"],
            "review_date": _format_short_date(parsed_review_dt),
        },
    }
    validate_against_schema(handoff_payload, INDEX_HANDOFF_SCHEMA, "handoff")

    proc = subprocess.run(
        [sys.executable, str(RECONCILER_SCRIPT), "--handoff", json.dumps(handoff_payload)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    log(proc.stdout.strip())
    if proc.stderr.strip():
        log(f"reconcile_indexes stderr: {proc.stderr.strip()}")

    summary = {
        "article_path": article_rel_path,
        "report_path": report_rel_path,
        "overall_before": scorecard["overall"]["before"],
        "overall_after": scorecard["overall"]["after"],
        "overall_delta": scorecard["overall"]["delta"],
        "persona_summaries": scorecard["persona_summaries"],
        "anti_inflation_clamps": scorecard["anti_inflation_clamps"],
    }
    print(json.dumps(summary, indent=2))
    return summary


await run_pipeline()
