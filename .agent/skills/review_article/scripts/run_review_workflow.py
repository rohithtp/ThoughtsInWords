#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stateful multi-turn review_article orchestration module for Antigravity `run_workflow` (Option B4 + A4).

Invoke via `run_workflow`:
  run_workflow(
      Script=(
          "import runpy\\n"
          "mod = runpy.run_path('.agent/skills/review_article/scripts/run_review_workflow.py', init_globals=globals())\\n"
          "await mod['run_pipeline'](globals())\\n"
      ),
      Args={"article_path": "articles/<category>/<slug>.md"},
      Description="Run 5-stage schema-validated multi-persona article review",
  )

Self-test locally without LLM calls (via uv/pip runner):
  bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/review_article/scripts/run_review_workflow.py --self-test
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = Path(__file__).resolve().parent
RECONCILER_SCRIPT = (
    DEFAULT_REPO_ROOT / ".agent" / "skills" / "organize_readme" / "scripts" / "reconcile_indexes.py"
)

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from schemas import (  # noqa: E402
    AFTER_SCORECARD_SCHEMA,
    BEFORE_SCORECARD_SCHEMA,
    INDEX_HANDOFF_SCHEMA,
    REMEDIATION_RESULT_SCHEMA,
    build_python_cmd,
    compute_scorecard,
    ensure_dependencies,
    get_uv_env,
    render_review_report,
    validate_against_schema,
)


def _format_long_date(dt: datetime) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def _format_short_date(dt: datetime) -> str:
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def _get_primitive(name: str, env: dict[str, Any], default: Any = None) -> Any:
    if name in env and env[name] is not None:
        return env[name]
    if default is not None:
        return default
    raise RuntimeError(
        f"Missing required run_workflow primitive '{name}'. "
        "Execute via run_workflow or pass a runtime_env dict."
    )


def _resolve_repo_root(env: dict[str, Any]) -> Path:
    workspaces = env.get("WORKSPACES")
    if workspaces and len(workspaces) > 0:
        return Path(workspaces[0])
    return DEFAULT_REPO_ROOT


def _validate_article_path(raw_path: str, repo_root: Path) -> tuple[Path, str, str, str]:
    rel_path = raw_path.strip().lstrip("./")
    m = re.match(r"^articles/([a-z0-9-]+)/([a-z0-9-]+)\.md$", rel_path)
    if not m:
        raise ValueError(
            f"article_path must match 'articles/<category>/<kebab-case>.md', got: {raw_path!r}"
        )
    abs_path = repo_root / rel_path
    if not abs_path.is_file():
        raise FileNotFoundError(f"Target article does not exist on disk: {abs_path}")
    return abs_path, rel_path, m.group(1), m.group(2)


async def run_pipeline(runtime_env: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute the 5-stage stateful review pipeline inside a `run_workflow` or mock runtime."""
    ensure_dependencies()
    env: dict[str, Any] = runtime_env if runtime_env is not None else globals()
    repo_root = _resolve_repo_root(env)

    log_fn: Callable[..., Any] = _get_primitive("log", env, default=print)
    phase_fn: Callable[[str], Any] = _get_primitive("phase", env, default=lambda _name: None)
    agent_fn: Callable[..., Any] = _get_primitive("agent", env)
    parallel_fn: Callable[..., Any] = _get_primitive("parallel", env)
    wf_args: dict[str, Any] = _get_primitive("args", env, default={}) or {}

    raw_article_path = wf_args.get("article_path", "")
    if not raw_article_path:
        raise ValueError(
            "Missing required workflow arg 'article_path' (e.g. 'articles/devops/example.md')."
        )
    dry_run = bool(wf_args.get("dry_run", False))

    abs_article_path, article_rel_path, category, slug = _validate_article_path(
        raw_article_path, repo_root
    )
    report_rel_path = f"reviews/{category}/{slug}-review.md"
    abs_report_path = repo_root / report_rel_path
    today_dt = datetime.now()
    today_long = _format_long_date(today_dt)

    # Read minimal header metadata from target article for context logging
    article_head = abs_article_path.read_text(encoding="utf-8")[:1500]
    title_m = re.search(r"^#\s+(.+?)\s*$", article_head, flags=re.MULTILINE)
    initial_title = title_m.group(1).strip() if title_m else slug

    log_fn(f"Starting Option B4 review pipeline for {article_rel_path} ('{initial_title}')")

    # ------------------------------------------------------------------
    # Stage 1: Persistent Read-Only Reviewer Definitions & Parallel Audit
    # ------------------------------------------------------------------
    phase_fn("Stage 1: Parallel Multi-Persona Before Audit")

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

    r_reader = agent_fn(reader_standing, role="Reader Mode Reviewer (Params 1-4)")
    r_sme = agent_fn(sme_standing, role="Subject Expert Reviewer (Params 5-8)")
    r_arch = agent_fn(arch_standing, role="Technical Architect Reviewer (Params 9-12)")

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

    before_payloads = await parallel_fn(
        before_tasks,
        lambda item: item[0](item[1], schema=BEFORE_SCORECARD_SCHEMA),
    )
    del before_tasks

    # ------------------------------------------------------------------
    # Stage 2 & 3: Synthesize Recommendations & Remediate Target Article
    # ------------------------------------------------------------------
    phase_fn("Stage 2 & 3: Synthesize & Remediate Target Article")

    priority_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    merged_recs: list[dict[str, Any]] = []
    for p in before_payloads:
        for rec in p["recommendations"]:
            merged_recs.append({"persona": p["persona"], **rec})
    merged_recs.sort(key=lambda r: (priority_rank.get(r["priority"], 9), r["id"]))

    log_fn(f"Synthesized {len(merged_recs)} prioritized recommendations across 3 reviewer personas.")

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

    remediation = await agent_fn(
        remediator_prompt,
        schema=REMEDIATION_RESULT_SCHEMA,
        role="Article Remediator (Scoped)",
        workspace="inherit",
    )

    # ------------------------------------------------------------------
    # Stage 4: Stateful Multi-Turn After Re-Verification & Report Render
    # ------------------------------------------------------------------
    phase_fn("Stage 4: Stateful Multi-Turn After Re-Verification & Report Rendering")

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

    after_payloads = await parallel_fn(
        after_tasks,
        lambda item: item[0](item[1], schema=AFTER_SCORECARD_SCHEMA),
    )
    del after_tasks, r_reader, r_sme, r_arch

    scorecard = compute_scorecard(before_payloads, after_payloads)
    if scorecard["anti_inflation_clamps"]:
        log_fn(f"Anti-inflation clamps applied: {json.dumps(scorecard['anti_inflation_clamps'])}")

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
    log_fn(f"Wrote deterministic Check 7 report to {report_rel_path}")

    # ------------------------------------------------------------------
    # Stage 5: Single-Writer Index Reconciliation & Verification Gate
    # ------------------------------------------------------------------
    phase_fn("Stage 5: Single-Writer Index Reconciliation & Verification Gate")

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

    if dry_run:
        cmd = build_python_cmd(str(RECONCILER_SCRIPT), "--dry-run")
        proc = subprocess.run(
            cmd,
            cwd=str(DEFAULT_REPO_ROOT),
            env=get_uv_env(),
            capture_output=True,
            text=True,
            check=True,
        )
    else:
        cmd = build_python_cmd(str(RECONCILER_SCRIPT), "--handoff", json.dumps(handoff_payload))
        proc = subprocess.run(
            cmd,
            cwd=str(repo_root),
            env=get_uv_env(),
            capture_output=True,
            text=True,
            check=True,
        )

    log_fn(proc.stdout.strip())
    if proc.stderr.strip():
        log_fn(f"reconcile_indexes stderr: {proc.stderr.strip()}")

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


def _run_self_test() -> None:
    """Exercise all 5 stages of run_pipeline() end-to-end with deterministic mock agents."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        article_path = tmp_root / "articles" / "devops" / "sample-article.md"
        article_path.parent.mkdir(parents=True, exist_ok=True)
        article_path.write_text(
            "# Sample Architecture Article\n\n**Date:** November 18, 2026\n\nDraft body.\n",
            encoding="utf-8",
        )

        phases_seen: list[str] = []
        logs_seen: list[str] = []
        handle_turns: dict[str, int] = {}

        class _MockHandle:
            def __init__(self, role: str) -> None:
                self.role = role
                handle_turns[role] = 0

            async def __call__(self, _prompt: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
                handle_turns[self.role] += 1
                turn = handle_turns[self.role]
                if self.role.startswith("Reader Mode"):
                    if turn == 1:
                        return {
                            "persona": "Reader Mode",
                            "scores": [
                                {"param_id": 1, "name": "Clarity", "score": 7.0, "rationale": "Hook ok"},
                                {"param_id": 2, "name": "Flow", "score": 7.5, "rationale": "Good flow"},
                                {"param_id": 3, "name": "Visuals", "score": 6.5, "rationale": "Missing diagram"},
                                {"param_id": 4, "name": "Takeaway", "score": 7.0, "rationale": "Good checklist"},
                            ],
                            "strengths": ["Clear summary"],
                            "gaps": ["Missing Mermaid diagram"],
                            "recommendations": [
                                {
                                    "id": "R-01",
                                    "param_id": 3,
                                    "priority": "High",
                                    "target_section": "## Architecture",
                                    "change": "Add Mermaid diagram",
                                    "invariant1_violation": False,
                                }
                            ],
                        }
                    return {
                        "persona": "Reader Mode",
                        "scores": [
                            {"param_id": 1, "score": 7.0, "key_improvement_applied": "Retained clear hook"},
                            {"param_id": 2, "score": 7.5, "key_improvement_applied": "Preserved pacing"},
                            {"param_id": 3, "score": 8.5, "key_improvement_applied": "Added Mermaid diagram"},
                            {"param_id": 4, "score": 7.0, "key_improvement_applied": "Checklist intact"},
                        ],
                        "verified_improvements": ["Added Mermaid architecture diagram."],
                        "recommendation_outcomes": [
                            {"id": "R-01", "status": "Applied", "article_section_updated": "## Architecture"}
                        ],
                    }

                if self.role.startswith("Subject Expert"):
                    if turn == 1:
                        return {
                            "persona": "Subject Expert",
                            "scores": [
                                {"param_id": 5, "name": "Accuracy", "score": 8.0, "rationale": "Accurate"},
                                {"param_id": 6, "name": "Edge Cases", "score": 6.0, "rationale": "Missing timeout"},
                                {"param_id": 7, "name": "Citations", "score": 7.5, "rationale": "RFC cited"},
                                {"param_id": 8, "name": "Currency", "score": 8.0, "rationale": "Current"},
                            ],
                            "strengths": ["Primary specs cited"],
                            "gaps": ["No backpressure failure mode"],
                            "recommendations": [
                                {
                                    "id": "S-01",
                                    "param_id": 6,
                                    "priority": "Critical",
                                    "target_section": "## Failure Modes",
                                    "change": "Document bounded queue backpressure",
                                    "invariant1_violation": False,
                                }
                            ],
                        }
                    return {
                        "persona": "Subject Expert",
                        "scores": [
                            {"param_id": 5, "score": 8.0, "key_improvement_applied": "Sound claims"},
                            {"param_id": 6, "score": 8.5, "key_improvement_applied": "Added backpressure mode"},
                            {"param_id": 7, "score": 7.5, "key_improvement_applied": "Kept RFC citations"},
                            {"param_id": 8, "score": 8.0, "key_improvement_applied": "Current"},
                        ],
                        "verified_improvements": ["Added bounded queue backpressure section."],
                        "recommendation_outcomes": [
                            {"id": "S-01", "status": "Applied", "article_section_updated": "## Failure Modes"}
                        ],
                    }

                # Technical Architect
                if turn == 1:
                    return {
                        "persona": "Technical Architect",
                        "scores": [
                            {"param_id": 9, "name": "Trade-Offs", "score": 7.0, "rationale": "Missing bounds"},
                            {"param_id": 10, "name": "Philosophy", "score": 8.0, "rationale": "Balanced"},
                            {"param_id": 11, "name": "Interconnectivity", "score": 7.0, "rationale": "Few links"},
                            {"param_id": 12, "name": "Lifecycle", "score": 7.0, "rationale": "Missing note"},
                        ],
                        "strengths": ["Realistic migration framing"],
                        "gaps": ["Missing Scope & Licensing Note"],
                        "pure_oss_audit": "Verified pure Apache-2.0 stack and Scope & Licensing Note.",
                        "philosophy_alignment_notes": {
                            "logic_and_emotion": "Grounded operator metrics.",
                            "engineers_philosophy_check": "Recognizes socio-technical adoption cost.",
                            "interconnectivity_and_metadata": "Added cross-links and Review header.",
                        },
                        "recommendations": [
                            {
                                "id": "A-01",
                                "param_id": 12,
                                "priority": "High",
                                "target_section": "Header",
                                "change": "Add Scope & Licensing Note",
                                "invariant1_violation": True,
                            }
                        ],
                    }
                return {
                    "persona": "Technical Architect",
                    "scores": [
                        {"param_id": 9, "score": 8.5, "key_improvement_applied": "Added trade-off bounds"},
                        {"param_id": 10, "score": 8.0, "key_improvement_applied": "Balanced philosophy"},
                        {"param_id": 11, "score": 8.0, "key_improvement_applied": "Expanded cross-links"},
                        {"param_id": 12, "score": 9.0, "key_improvement_applied": "Added Scope & Licensing Note"},
                    ],
                    "verified_improvements": ["Added Scope & Licensing Note and Review metadata."],
                    "recommendation_outcomes": [
                        {"id": "A-01", "status": "Applied", "article_section_updated": "Header"}
                    ],
                }

        def _mock_agent(prompt: str | None = None, schema: dict[str, Any] | None = None, role: str = "", **_kw: Any) -> Any:
            if schema is None:
                return _MockHandle(role)

            async def _remediate() -> dict[str, Any]:
                assert schema == REMEDIATION_RESULT_SCHEMA
                return {
                    "article_path": "articles/devops/sample-article.md",
                    "article_title": "Sample Architecture Article",
                    "date": "November 18, 2026",
                    "last_updated": "November 19, 2026",
                    "verdict_label": "Production-Ready",
                    "verdict_summary": "Applied diagram, failure modes, and pure-OSS compliance.",
                    "alignment_status": "Partially Aligned → Aligned",
                    "changelog_summary": "Applied multi-persona review recommendations",
                    "applied_recommendation_ids": ["R-01", "S-01", "A-01"],
                }

            return _remediate()

        async def _mock_parallel(items: list[Any], fn: Callable[[Any], Any]) -> list[Any]:
            return await asyncio.gather(*(fn(item) for item in items))

        mock_env: dict[str, Any] = {
            "WORKSPACES": (str(tmp_root),),
            "args": {"article_path": "articles/devops/sample-article.md", "dry_run": True},
            "log": logs_seen.append,
            "phase": phases_seen.append,
            "agent": _mock_agent,
            "parallel": _mock_parallel,
        }

        summary = asyncio.run(run_pipeline(mock_env))

        assert len(phases_seen) == 4
        assert all(turns == 2 for turns in handle_turns.values()), f"Expected 2 turns per reviewer: {handle_turns}"
        assert summary["overall_before"] == 7.2
        assert summary["overall_after"] == 8.0
        assert summary["overall_delta"] == "+0.8"

        generated_report = tmp_root / "reviews" / "devops" / "sample-article-review.md"
        assert generated_report.is_file(), "Stage 4 failed to write review report"
        report_text = generated_report.read_text(encoding="utf-8")
        for heading in (
            "## 2. Before vs. After Scorecard (0–10)",
            "## 3. Reader Mode Review",
            "## 4. Subject Matter Expert (SME) Review",
            "## 5. Technical Architect & Repo Concept Review",
        ):
            assert heading in report_text, f"Missing Check 7 heading: {heading}"

        print("✅ run_review_workflow.py self-test passed (all 5 stages, multi-turn handles, schemas & Check 7 report verified).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review workflow runner and offline self-test.")
    parser.add_argument("--self-test", action="store_true", help="Run 5-stage mock pipeline self-test.")
    cli_args = parser.parse_args()
    if cli_args.self_test:
        _run_self_test()
    else:
        parser.print_help()
