#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""JSON Schemas, dependency/runner helpers, deterministic scorecard computation,
and Check 7 report rendering for the ThoughtsInWords multi-persona review_article
pipeline (Option B4 + Option A4 + uv/pip support).
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from typing import Any


def get_uv_env() -> dict[str, str]:
    """Return environment variables configured for sandbox-safe uv/pip execution."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("UV_CACHE_DIR", "/tmp/uv-cache")
    env.setdefault("UV_PYTHON_INSTALL_DIR", "/tmp/uv-python")
    env.setdefault("UV_TOOL_DIR", "/tmp/uv-tools")
    env.setdefault("UV_PYTHON_PREFERENCE", "only-system")
    return env


def ensure_dependencies(packages: list[str] | tuple[str, ...] = ()) -> None:
    """Resolve any missing Python packages via uv pip first, falling back to pip."""
    if not packages:
        return

    missing: list[str] = []
    for raw_pkg in packages:
        mod_name = re.split(r"[<>=!~;\[]", raw_pkg, maxsplit=1)[0].strip().replace("-", "_")
        if mod_name and importlib.util.find_spec(mod_name) is None:
            missing.append(raw_pkg)

    if not missing:
        return

    env = get_uv_env()
    uv_bin = shutil.which("uv")
    if uv_bin:
        uv_proc = subprocess.run(
            [uv_bin, "pip", "install", "--quiet", "--python", sys.executable, *missing],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if uv_proc.returncode == 0:
            return

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", *missing],
        env=env,
        check=True,
    )


def build_python_cmd(*script_and_args: str) -> list[str]:
    """Build a child Python command preferring `uv run --no-project` with direct fallback."""
    uv_bin = shutil.which("uv")
    if uv_bin:
        return [uv_bin, "run", "--no-project", sys.executable, "-B", *script_and_args]
    return [sys.executable, "-B", *script_and_args]

PERSONA_ORDER = ["Reader Mode", "Subject Expert", "Technical Architect"]

PERSONA_PARAM_IDS: dict[str, tuple[int, int, int, int]] = {
    "Reader Mode": (1, 2, 3, 4),
    "Subject Expert": (5, 6, 7, 8),
    "Technical Architect": (9, 10, 11, 12),
}

PARAMETER_NAMES: dict[int, str] = {
    1: "Executive Clarity & Hook (`## Summary` & `## Key Points`)",
    2: "Narrative Flow & Cognitive Load",
    3: "Visual Aids & Scannability",
    4: "Accessibility & Actionable Takeaway",
    5: "Technical & Domain Accuracy",
    6: "Depth of Insight & Edge Cases",
    7: "Citations, Specifications & Evidence",
    8: "Domain Completeness & Currency",
    9: "Architectural Soundness & Trade-Off Rigor",
    10: "ThoughtsInWords Philosophy Alignment",
    11: "Digital Garden Interconnectivity",
    12: "Repository Lifecycle & Standards Compliance",
}

BEFORE_SCORECARD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["persona", "scores", "strengths", "gaps", "recommendations"],
    "properties": {
        "persona": {
            "type": "string",
            "enum": ["Reader Mode", "Subject Expert", "Technical Architect"],
        },
        "scores": {
            "type": "array",
            "minItems": 4,
            "maxItems": 4,
            "items": {
                "type": "object",
                "required": ["param_id", "name", "score", "rationale"],
                "properties": {
                    "param_id": {"type": "integer", "minimum": 1, "maximum": 12},
                    "name": {"type": "string"},
                    "score": {"type": "number", "minimum": 0.0, "maximum": 10.0},
                    "rationale": {"type": "string"},
                },
            },
        },
        "strengths": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
        },
        "gaps": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
        },
        "pure_oss_audit": {"type": "string"},
        "philosophy_alignment_notes": {
            "type": "object",
            "properties": {
                "logic_and_emotion": {"type": "string"},
                "engineers_philosophy_check": {"type": "string"},
                "interconnectivity_and_metadata": {"type": "string"},
            },
        },
        "recommendations": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": [
                    "id",
                    "param_id",
                    "priority",
                    "target_section",
                    "change",
                    "invariant1_violation",
                ],
                "properties": {
                    "id": {"type": "string", "pattern": "^(R|S|A)-[0-9]{2}$"},
                    "param_id": {"type": "integer", "minimum": 1, "maximum": 12},
                    "priority": {
                        "type": "string",
                        "enum": ["Critical", "High", "Medium", "Low"],
                    },
                    "target_section": {"type": "string"},
                    "change": {"type": "string"},
                    "invariant1_violation": {"type": "boolean"},
                },
            },
        },
    },
}

REMEDIATION_RESULT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "article_path",
        "article_title",
        "date",
        "last_updated",
        "verdict_label",
        "verdict_summary",
        "alignment_status",
        "changelog_summary",
        "applied_recommendation_ids",
    ],
    "properties": {
        "article_path": {
            "type": "string",
            "pattern": "^articles/[a-z0-9-]+/[a-z0-9-]+\\.md$",
        },
        "article_title": {"type": "string"},
        "date": {"type": "string"},
        "last_updated": {"type": "string"},
        "verdict_label": {"type": "string"},
        "verdict_summary": {"type": "string"},
        "alignment_status": {"type": "string"},
        "changelog_summary": {"type": "string"},
        "applied_recommendation_ids": {
            "type": "array",
            "items": {"type": "string", "pattern": "^(R|S|A)-[0-9]{2}$"},
        },
    },
}

AFTER_SCORECARD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "persona",
        "scores",
        "verified_improvements",
        "recommendation_outcomes",
    ],
    "properties": {
        "persona": {
            "type": "string",
            "enum": ["Reader Mode", "Subject Expert", "Technical Architect"],
        },
        "scores": {
            "type": "array",
            "minItems": 4,
            "maxItems": 4,
            "items": {
                "type": "object",
                "required": ["param_id", "score", "key_improvement_applied"],
                "properties": {
                    "param_id": {"type": "integer", "minimum": 1, "maximum": 12},
                    "score": {"type": "number", "minimum": 0.0, "maximum": 10.0},
                    "key_improvement_applied": {"type": "string"},
                },
            },
        },
        "verified_improvements": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
        },
        "recommendation_outcomes": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "status", "article_section_updated"],
                "properties": {
                    "id": {"type": "string", "pattern": "^(R|S|A)-[0-9]{2}$"},
                    "status": {"type": "string", "enum": ["Applied", "Deferred"]},
                    "article_section_updated": {"type": "string"},
                },
            },
        },
    },
}

INDEX_HANDOFF_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["action", "article_path", "title", "date", "changelog_summary"],
    "properties": {
        "action": {
            "type": "string",
            "enum": ["Added", "Updated", "Simplified", "Reviewed & Updated"],
        },
        "article_path": {
            "type": "string",
            "pattern": "^articles/[a-z0-9-]+/[a-z0-9-]+\\.md$",
        },
        "title": {"type": "string"},
        "date": {"type": "string"},
        "last_updated": {"type": "string"},
        "changelog_summary": {"type": "string"},
        "review_move": {
            "type": "object",
            "required": [
                "report_path",
                "before_score",
                "after_score",
                "delta",
                "review_date",
            ],
            "properties": {
                "report_path": {
                    "type": "string",
                    "pattern": "^reviews/[a-z0-9-]+/[a-z0-9-]+-review\\.md$",
                },
                "before_score": {"type": "number", "minimum": 0.0, "maximum": 10.0},
                "after_score": {"type": "number", "minimum": 0.0, "maximum": 10.0},
                "delta": {"type": "string"},
                "review_date": {"type": "string"},
            },
        },
        "reciprocal_articles_touched": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


class SchemaValidationError(ValueError):
    """Raised when a payload violates its JSON Schema contract."""


def validate_against_schema(
    value: Any,
    schema: dict[str, Any],
    path: str = "$",
) -> None:
    """Validate a Python object against a Draft-07 JSON Schema subset."""
    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            raise SchemaValidationError(f"{path}: expected object, got {type(value).__name__}")
        for req in schema.get("required", []):
            if req not in value:
                raise SchemaValidationError(f"{path}: missing required key '{req}'")
        props = schema.get("properties", {})
        for key, prop_schema in props.items():
            if key in value:
                validate_against_schema(value[key], prop_schema, f"{path}.{key}")
    elif expected_type == "array":
        if not isinstance(value, list):
            raise SchemaValidationError(f"{path}: expected array, got {type(value).__name__}")
        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if min_items is not None and len(value) < min_items:
            raise SchemaValidationError(f"{path}: expected at least {min_items} items, got {len(value)}")
        if max_items is not None and len(value) > max_items:
            raise SchemaValidationError(f"{path}: expected at most {max_items} items, got {len(value)}")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value):
                validate_against_schema(item, item_schema, f"{path}[{idx}]")
    elif expected_type == "string":
        if not isinstance(value, str):
            raise SchemaValidationError(f"{path}: expected string, got {type(value).__name__}")
        if "enum" in schema and value not in schema["enum"]:
            raise SchemaValidationError(f"{path}: value {value!r} not in {schema['enum']}")
        pattern = schema.get("pattern")
        if pattern and not re.match(pattern, value):
            raise SchemaValidationError(f"{path}: value {value!r} does not match pattern {pattern!r}")
    elif expected_type == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            raise SchemaValidationError(f"{path}: expected integer, got {type(value).__name__}")
        if "minimum" in schema and value < schema["minimum"]:
            raise SchemaValidationError(f"{path}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            raise SchemaValidationError(f"{path}: {value} > maximum {schema['maximum']}")
    elif expected_type == "number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise SchemaValidationError(f"{path}: expected number, got {type(value).__name__}")
        if "minimum" in schema and value < schema["minimum"]:
            raise SchemaValidationError(f"{path}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            raise SchemaValidationError(f"{path}: {value} > maximum {schema['maximum']}")
    elif expected_type == "boolean":
        if not isinstance(value, bool):
            raise SchemaValidationError(f"{path}: expected boolean, got {type(value).__name__}")


def format_delta(before: float, after: float) -> str:
    """Format a signed 1-decimal delta cleanly without -0.0 artifacts."""
    diff = round(after - before, 1)
    if abs(diff) < 1e-9:
        return "0.0"
    return f"{diff:+.1f}"


def _index_persona_payloads(
    payloads: list[dict[str, Any]],
    schema: dict[str, Any],
    label: str,
) -> dict[str, dict[str, Any]]:
    by_persona: dict[str, dict[str, Any]] = {}
    for payload in payloads:
        validate_against_schema(payload, schema, label)
        persona = payload["persona"]
        if persona in by_persona:
            raise SchemaValidationError(f"{label}: duplicate persona {persona!r}")
        expected_ids = set(PERSONA_PARAM_IDS[persona])
        actual_ids = {item["param_id"] for item in payload["scores"]}
        if actual_ids != expected_ids:
            raise SchemaValidationError(
                f"{label}.{persona}: expected param_ids {sorted(expected_ids)}, got {sorted(actual_ids)}"
            )
        by_persona[persona] = payload
    missing = [p for p in PERSONA_ORDER if p not in by_persona]
    if missing:
        raise SchemaValidationError(f"{label}: missing personas {missing}")
    return by_persona


def compute_scorecard(
    before_list: list[dict[str, Any]],
    after_list: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate Stage 1/Stage 4 payloads, enforce anti-inflation clamping,
    and deterministically compute parameter rows, sub-averages, composite scores, and deltas.
    """
    before_by_persona = _index_persona_payloads(before_list, BEFORE_SCORECARD_SCHEMA, "before")
    after_by_persona = _index_persona_payloads(after_list, AFTER_SCORECARD_SCHEMA, "after")

    outcome_by_id: dict[str, dict[str, str]] = {}
    for persona in PERSONA_ORDER:
        for outcome in after_by_persona[persona]["recommendation_outcomes"]:
            outcome_by_id[outcome["id"]] = outcome

    # Group Stage 1 recommendations by parameter to enforce anti-inflation clamping.
    recs_by_param: dict[int, list[dict[str, Any]]] = {pid: [] for pid in range(1, 13)}
    all_recommendations: list[dict[str, Any]] = []
    for persona in PERSONA_ORDER:
        for rec in before_by_persona[persona]["recommendations"]:
            recs_by_param[rec["param_id"]].append(rec)
            all_recommendations.append({"persona": persona, **rec})

    parameters: list[dict[str, Any]] = []
    persona_summaries: dict[str, dict[str, Any]] = {}
    anti_inflation_clamps: list[dict[str, Any]] = []

    for persona in PERSONA_ORDER:
        before_scores = {s["param_id"]: s for s in before_by_persona[persona]["scores"]}
        after_scores = {s["param_id"]: s for s in after_by_persona[persona]["scores"]}

        p_before_vals: list[float] = []
        p_after_vals: list[float] = []

        for pid in PERSONA_PARAM_IDS[persona]:
            b_val = round(float(before_scores[pid]["score"]), 1)
            raw_a_val = round(float(after_scores[pid]["score"]), 1)
            a_val = raw_a_val

            param_recs = recs_by_param[pid]
            if param_recs:
                statuses = [
                    outcome_by_id.get(r["id"], {}).get("status", "Deferred")
                    for r in param_recs
                ]
                if all(st == "Deferred" for st in statuses) and a_val > b_val:
                    a_val = b_val
                    anti_inflation_clamps.append(
                        {
                            "param_id": pid,
                            "persona": persona,
                            "raw_after": raw_a_val,
                            "clamped_after": a_val,
                            "reason": "All Stage 1 recommendations for parameter remained Deferred.",
                        }
                    )

            p_before_vals.append(b_val)
            p_after_vals.append(a_val)
            improvement_note = after_scores[pid]["key_improvement_applied"].strip()
            if a_val == b_val and any(c["param_id"] == pid for c in anti_inflation_clamps):
                improvement_note = f"{improvement_note} *(Score held at Before baseline: linked recommendations Deferred.)*"

            parameters.append(
                {
                    "param_id": pid,
                    "persona": persona,
                    "name": PARAMETER_NAMES[pid],
                    "before": b_val,
                    "after": a_val,
                    "delta": format_delta(b_val, a_val),
                    "key_improvement": improvement_note,
                    "rationale": before_scores[pid]["rationale"].strip(),
                }
            )

        sub_before = round(sum(p_before_vals) / 4.0, 1)
        sub_after = round(sum(p_after_vals) / 4.0, 1)
        persona_summaries[persona] = {
            "before": sub_before,
            "after": sub_after,
            "delta": format_delta(sub_before, sub_after),
        }

    overall_before = round(sum(row["before"] for row in parameters) / 12.0, 1)
    overall_after = round(sum(row["after"] for row in parameters) / 12.0, 1)

    priority_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    execution_log: list[dict[str, str]] = []
    for rec in sorted(all_recommendations, key=lambda r: (priority_rank.get(r["priority"], 9), r["id"])):
        outcome = outcome_by_id.get(rec["id"], {})
        execution_log.append(
            {
                "id": rec["id"],
                "persona": rec["persona"],
                "priority": rec["priority"],
                "change": rec["change"],
                "status": outcome.get("status", "Deferred"),
                "article_section_updated": outcome.get("article_section_updated", rec["target_section"]),
            }
        )

    return {
        "parameters": parameters,
        "persona_summaries": persona_summaries,
        "overall": {
            "before": overall_before,
            "after": overall_after,
            "delta": format_delta(overall_before, overall_after),
        },
        "before_by_persona": before_by_persona,
        "after_by_persona": after_by_persona,
        "execution_log": execution_log,
        "anti_inflation_clamps": anti_inflation_clamps,
    }


def _escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def render_review_report(
    article_title: str,
    category: str,
    slug: str,
    review_date: str,
    remediation: dict[str, Any],
    scorecard: dict[str, Any],
) -> str:
    """Render reviews/<category>/<slug>-review.md matching report-template.md and Check 7."""
    validate_against_schema(remediation, REMEDIATION_RESULT_SCHEMA, "remediation")

    overall = scorecard["overall"]
    ps = scorecard["persona_summaries"]
    before_by_p = scorecard["before_by_persona"]
    after_by_p = scorecard["after_by_persona"]

    lines: list[str] = [
        f"# Verification & Review Report: {article_title}",
        "",
        f"**Target Article:** [{article_title}](../../articles/{category}/{slug}.md)",
        f"**Category:** `{category}`",
        f"**Review Date:** {review_date}",
        f"**Overall Score:** `{overall['before']:.1f} / 10` (Before) → `{overall['after']:.1f} / 10` (After) | **Delta:** `{overall['delta']}`",
        "",
        "---",
        "",
        "## 1. Executive Summary & Architectural Verdict",
        "",
        f"* **Verdict:** `{remediation['verdict_label']}` — {remediation['verdict_summary']}",
        f"* **Repo Concept Alignment Status:** `{remediation['alignment_status']}` with the *ThoughtsInWords* philosophy and Digital Garden model.",
        "* **Sub-Scores Summary:**",
        f"  * **Reader Mode:** `{ps['Reader Mode']['before']:.1f} / 10` → `{ps['Reader Mode']['after']:.1f} / 10` (`{ps['Reader Mode']['delta']}`)",
        f"  * **Subject Matter Expert (SME):** `{ps['Subject Expert']['before']:.1f} / 10` → `{ps['Subject Expert']['after']:.1f} / 10` (`{ps['Subject Expert']['delta']}`)",
        f"  * **Technical Architect & Repo Concept:** `{ps['Technical Architect']['before']:.1f} / 10` → `{ps['Technical Architect']['after']:.1f} / 10` (`{ps['Technical Architect']['delta']}`)",
        "",
        "---",
        "",
        "## 2. Before vs. After Scorecard (0–10)",
        "",
        "| Persona Lens | # | Parameter | Before (0–10) | After (0–10) | Delta | Key Improvement Applied |",
        "| :--- | :-: | :--- | :---: | :---: | :---: | :--- |",
    ]

    for persona in PERSONA_ORDER:
        p_rows = [r for r in scorecard["parameters"] if r["persona"] == persona]
        for row in p_rows:
            lines.append(
                f"| **{persona}** | {row['param_id']} | {_escape_cell(row['name'])} | "
                f"{row['before']:.1f} | {row['after']:.1f} | {row['delta']} | "
                f"{_escape_cell(row['key_improvement'])} |"
            )
        sub = ps[persona]
        lines.append(
            f"| **{persona}** | — | **{persona} Sub-Average** | "
            f"**{sub['before']:.1f}** | **{sub['after']:.1f}** | **{sub['delta']}** | — |"
        )

    lines.append(
        f"| **Composite** | **All** | **Overall Composite Score (0–10)** | "
        f"**{overall['before']:.1f}** | **{overall['after']:.1f}** | **{overall['delta']}** | "
        "**Verified via multi-persona schema re-evaluation & `verify_links.sh`** |"
    )

    # Section 3: Reader Mode Review
    rm_b = before_by_p["Reader Mode"]
    rm_a = after_by_p["Reader Mode"]
    lines.extend([
        "",
        "---",
        "",
        "## 3. Reader Mode Review",
        "",
        "### Initial Assessment (Before)",
        f"* **Strengths:** {'; '.join(rm_b['strengths'])}",
        f"* **Friction Points:** {'; '.join(rm_b['gaps'])}",
        "",
        "### Verified Improvements (After)",
    ])
    for item in rm_a["verified_improvements"]:
        lines.append(f"* {item}")

    # Section 4: Subject Matter Expert (SME) Review
    sme_b = before_by_p["Subject Expert"]
    sme_a = after_by_p["Subject Expert"]
    lines.extend([
        "",
        "---",
        "",
        "## 4. Subject Matter Expert (SME) Review",
        "",
        "### Initial Assessment (Before)",
        f"* **Technical Accuracy & Depth Check:** {'; '.join(sme_b['strengths'])}",
        f"* **Missing Edge Cases / Citations / Currency Gaps:** {'; '.join(sme_b['gaps'])}",
        "",
        "### Verified Improvements (After)",
    ])
    for item in sme_a["verified_improvements"]:
        lines.append(f"* {item}")

    # Section 5: Technical Architect & Repo Concept Review
    ta_b = before_by_p["Technical Architect"]
    ta_a = after_by_p["Technical Architect"]
    notes = ta_b.get("philosophy_alignment_notes", {})
    oss_audit = ta_b.get("pure_oss_audit") or "Audited against Invariant 1 (Pure Open-Source Systems Mandate & Scope & Licensing Note)."
    logic_emotion = notes.get("logic_and_emotion") or "; ".join(ta_b["strengths"])
    eng_check = notes.get("engineers_philosophy_check") or "; ".join(ta_b["gaps"])
    interconn = notes.get("interconnectivity_and_metadata") or "Verified ## Related Articles cross-links and Invariants 2–3 lifecycle metadata."

    lines.extend([
        "",
        "---",
        "",
        "## 5. Technical Architect & Repo Concept Review",
        "",
        "### Architecture & Trade-Off Verification",
        f"* **Solution Viability, NFRs & Failure Modes:** {'; '.join(ta_b['strengths'])}",
        f"* **Pure Open-Source Systems & Scope Note Audit:** {oss_audit}",
        "",
        "### ThoughtsInWords Concept & Philosophy Alignment",
        f"* **Logic & Emotion / Intellectual Humility:** {logic_emotion}",
        f"* **Engineer's Philosophy Pitfall Check (Anti-Oversimplification):** {eng_check}",
        f"* **Digital Garden Interconnectivity & Metadata Compliance:** {interconn}",
        "",
        "### Verified Improvements (After)",
    ])
    for item in ta_a["verified_improvements"]:
        lines.append(f"* {item}")

    # Section 6: Recommended Changes & Execution Log
    lines.extend([
        "",
        "---",
        "",
        "## 6. Recommended Changes & Execution Log",
        "",
        "| ID | Lens | Priority | Recommendation | Status | Article Section Updated |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ])
    for entry in scorecard["execution_log"]:
        lines.append(
            f"| `{entry['id']}` | {_escape_cell(entry['persona'])} | {entry['priority']} | "
            f"{_escape_cell(entry['change'])} | {entry['status']} | "
            f"{_escape_cell(entry['article_section_updated'])} |"
        )
    lines.append("")
    return "\n".join(lines)


def _run_self_test() -> None:
    before_sample = [
        {
            "persona": "Reader Mode",
            "scores": [
                {"param_id": 1, "name": "Clarity", "score": 7.0, "rationale": "Good summary"},
                {"param_id": 2, "name": "Flow", "score": 7.5, "rationale": "Steady pacing"},
                {"param_id": 3, "name": "Visuals", "score": 6.5, "rationale": "Needs Mermaid diagram"},
                {"param_id": 4, "name": "Takeaway", "score": 7.0, "rationale": "Solid checklist"},
            ],
            "strengths": ["Clear opening hook"],
            "gaps": ["Missing architecture flow diagram"],
            "recommendations": [
                {
                    "id": "R-01",
                    "param_id": 3,
                    "priority": "High",
                    "target_section": "## Architecture",
                    "change": "Add Mermaid topology diagram",
                    "invariant1_violation": False,
                },
                {
                    "id": "R-02",
                    "param_id": 1,
                    "priority": "Low",
                    "target_section": "## Summary",
                    "change": "Tighten opening sentence",
                    "invariant1_violation": False,
                },
            ],
        },
        {
            "persona": "Subject Expert",
            "scores": [
                {"param_id": 5, "name": "Accuracy", "score": 8.0, "rationale": "Sound claims"},
                {"param_id": 6, "name": "Edge Cases", "score": 6.0, "rationale": "Missing timeout mode"},
                {"param_id": 7, "name": "Citations", "score": 7.5, "rationale": "Primary RFC linked"},
                {"param_id": 8, "name": "Currency", "score": 8.0, "rationale": "Up to date"},
            ],
            "strengths": ["Accurate RFC citations"],
            "gaps": ["Missing backpressure failure mode"],
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
        },
        {
            "persona": "Technical Architect",
            "scores": [
                {"param_id": 9, "name": "Trade-Offs", "score": 7.0, "rationale": "Open-core tool mentioned"},
                {"param_id": 10, "name": "Philosophy", "score": 8.0, "rationale": "Acknowledges legacy cost"},
                {"param_id": 11, "name": "Interconnectivity", "score": 7.0, "rationale": "Only 1 link"},
                {"param_id": 12, "name": "Lifecycle", "score": 7.0, "rationale": "Missing Scope Note"},
            ],
            "strengths": ["Candid migration cost framing"],
            "gaps": ["Included non-pure-OSS option and missing Scope & Licensing Note"],
            "pure_oss_audit": "Replaced open-core reference with pure Apache-2.0 engine and added Scope & Licensing Note.",
            "philosophy_alignment_notes": {
                "logic_and_emotion": "Balances latency metrics with operator cognitive load.",
                "engineers_philosophy_check": "Addresses team adoption friction realistically.",
                "interconnectivity_and_metadata": "Added 3 cross-category links and Review header.",
            },
            "recommendations": [
                {
                    "id": "A-01",
                    "param_id": 9,
                    "priority": "Critical",
                    "target_section": "## Comparison",
                    "change": "Replace open-core option with pure OSS equivalent",
                    "invariant1_violation": True,
                }
            ],
        },
    ]

    after_sample = [
        {
            "persona": "Reader Mode",
            "scores": [
                # param_id 1 had R-02 which is Deferred below -> must clamp from 8.0 back to 7.0!
                {"param_id": 1, "score": 8.0, "key_improvement_applied": "Attempted minor tightening"},
                {"param_id": 2, "score": 7.5, "key_improvement_applied": "Preserved steady pacing"},
                {"param_id": 3, "score": 8.5, "key_improvement_applied": "Added Mermaid topology diagram"},
                {"param_id": 4, "score": 7.0, "key_improvement_applied": "Checklist intact"},
            ],
            "verified_improvements": ["Added Mermaid architecture diagram in ## Architecture."],
            "recommendation_outcomes": [
                {"id": "R-01", "status": "Applied", "article_section_updated": "## Architecture"},
                {"id": "R-02", "status": "Deferred", "article_section_updated": "## Summary"},
            ],
        },
        {
            "persona": "Subject Expert",
            "scores": [
                {"param_id": 5, "score": 8.0, "key_improvement_applied": "Verified technical claims"},
                {"param_id": 6, "score": 8.5, "key_improvement_applied": "Added bounded queue backpressure analysis"},
                {"param_id": 7, "score": 7.5, "key_improvement_applied": "Preserved all primary citations"},
                {"param_id": 8, "score": 8.0, "key_improvement_applied": "Verified 2026 currency"},
            ],
            "verified_improvements": ["Documented bounded queue backpressure and drop thresholds."],
            "recommendation_outcomes": [
                {"id": "S-01", "status": "Applied", "article_section_updated": "## Failure Modes"},
            ],
        },
        {
            "persona": "Technical Architect",
            "scores": [
                {"param_id": 9, "score": 9.0, "key_improvement_applied": "Pure Apache-2.0 stack & trade-off bounds"},
                {"param_id": 10, "score": 8.0, "key_improvement_applied": "Preserved socio-technical nuance"},
                {"param_id": 11, "score": 8.0, "key_improvement_applied": "Added cross-category garden links"},
                {"param_id": 12, "score": 9.0, "key_improvement_applied": "Added Scope & Licensing Note and Review link"},
            ],
            "verified_improvements": ["Enforced Invariant 1 pure-OSS compliance and Scope & Licensing Note."],
            "recommendation_outcomes": [
                {"id": "A-01", "status": "Applied", "article_section_updated": "## Comparison"},
            ],
        },
    ]

    remediation_sample = {
        "article_path": "articles/devops/sample-article.md",
        "article_title": "Sample Architecture Article",
        "date": "November 18, 2026",
        "last_updated": "November 19, 2026",
        "verdict_label": "Production-Ready",
        "verdict_summary": "Resolved Invariant 1 licensing drift, added failure-mode boundaries, and improved visual scannability.",
        "alignment_status": "Partially Aligned → Aligned",
        "changelog_summary": "Applied multi-persona audit, pure-OSS replacements, and Mermaid topology.",
        "applied_recommendation_ids": ["R-01", "S-01", "A-01"],
    }

    handoff_sample = {
        "action": "Reviewed & Updated",
        "article_path": "articles/devops/sample-article.md",
        "title": "Sample Architecture Article",
        "date": "November 18, 2026",
        "last_updated": "November 19, 2026",
        "changelog_summary": remediation_sample["changelog_summary"],
        "review_move": {
            "report_path": "reviews/devops/sample-article-review.md",
            "before_score": 7.2,
            "after_score": 8.2,
            "delta": "+1.0",
            "review_date": "Nov 19, 2026",
        },
    }
    validate_against_schema(handoff_sample, INDEX_HANDOFF_SCHEMA, "handoff")

    result = compute_scorecard(before_sample, after_sample)
    # Verify anti-inflation clamp on param_id 1 (8.0 -> clamped to 7.0)
    p1 = next(r for r in result["parameters"] if r["param_id"] == 1)
    assert p1["after"] == 7.0, f"Expected param 1 clamped to 7.0, got {p1['after']}"
    assert len(result["anti_inflation_clamps"]) == 1

    # Reader Mode: before=(7+7.5+6.5+7)/4=7.0, after=(7+7.5+8.5+7)/4=7.5, delta=+0.5
    assert result["persona_summaries"]["Reader Mode"] == {"before": 7.0, "after": 7.5, "delta": "+0.5"}
    # SME: before=(8+6+7.5+8)/4=7.375->7.4, after=(8+8.5+7.5+8)/4=8.0, delta=+0.6
    assert result["persona_summaries"]["Subject Expert"] == {"before": 7.4, "after": 8.0, "delta": "+0.6"}
    # TA: before=(7+8+7+7)/4=7.25->7.2, after=(9+8+8+9)/4=8.5, delta=+1.3
    assert result["persona_summaries"]["Technical Architect"] == {"before": 7.2, "after": 8.5, "delta": "+1.3"}

    report_md = render_review_report(
        article_title="Sample Architecture Article",
        category="devops",
        slug="sample-article",
        review_date="November 19, 2026",
        remediation=remediation_sample,
        scorecard=result,
    )

    required_headings = [
        r"^## 2\. Before vs\. After Scorecard \(0[–-]10\)\s*$",
        r"^## 3\. Reader Mode Review\s*$",
        r"^## 4\. Subject Matter Expert \(SME\) Review\s*$",
        r"^## 5\. Technical Architect & Repo Concept Review\s*$",
    ]
    for pattern in required_headings:
        assert re.search(pattern, report_md, flags=re.MULTILINE), f"Missing required Check 7 heading: {pattern}"

    ensure_dependencies(["json", "re"])
    ver_cmd = build_python_cmd("--version")
    assert ver_cmd[-2:] == ["-B", "--version"], f"Unexpected build_python_cmd: {ver_cmd}"
    ver_proc = subprocess.run(ver_cmd, env=get_uv_env(), capture_output=True, text=True, check=True)
    assert "Python" in (ver_proc.stdout or ver_proc.stderr)

    print("✅ schemas.py self-test passed (4 schemas, uv/pip helpers, anti-inflation clamp, math & Check 7 renderer verified).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review workflow JSON schemas and scorecard utilities.")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic unit self-tests.")
    args = parser.parse_args()
    if args.self_test:
        _run_self_test()
    else:
        parser.print_help()
