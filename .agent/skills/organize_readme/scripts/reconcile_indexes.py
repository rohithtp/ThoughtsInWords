#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Deterministic single-writer index, badge cohort, review index, and changelog
reconciler for ThoughtsInWords (Option A4).

Usage (via uv/pip wrapper or direct python3):
  bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py
  bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --dry-run
  bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff '<json>'
  bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/organize_readme/scripts/reconcile_indexes.py --handoff-file path/to/handoff.json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "review_article" / "scripts"
if str(SCHEMAS_DIR) not in sys.path:
    sys.path.insert(0, str(SCHEMAS_DIR))

from schemas import INDEX_HANDOFF_SCHEMA, get_uv_env, validate_against_schema  # noqa: E402

CATEGORY_CONFIG: dict[str, dict[str, Any]] = {
    "ai": {
        "index_heading": "### AI",
        "root_label": "[AI](./articles/README.md#ai)",
        "dir_label": "[AI](#ai)",
        "subsection_labels": {
            "#### Agents & Tooling": "Agents & Tooling",
            "#### Strategy & Impact": "Strategy & Impact",
        },
    },
    "cloud-native": {
        "index_heading": "### Cloud Native",
        "root_label": "[Cloud Native](./articles/README.md#cloud-native)",
        "dir_label": "[Cloud Native](#cloud-native)",
        "subsection_labels": {},
    },
    "design": {
        "index_heading": "### Design",
        "root_label": "[Design](./articles/README.md#design)",
        "dir_label": "[Design](#design)",
        "subsection_labels": {},
    },
    "devops": {
        "index_heading": "### DevOps & Infrastructure",
        "root_label": "[DevOps & Infrastructure](./articles/README.md#devops--infrastructure)",
        "dir_label": "[DevOps & Infrastructure](#devops--infrastructure)",
        "subsection_labels": {
            "#### APIs & Specifications": "APIs & Specs",
            "#### Authentication & Authorization": "Auth",
            "#### Git & Version Control": "Git",
            "#### Observability & Operations": "Ops",
            "#### Platform & Scaling": "Platform",
        },
    },
    "distributed-systems": {
        "index_heading": "### Distributed Systems",
        "root_label": "[Distributed Systems](./articles/README.md#distributed-systems)",
        "dir_label": "[Distributed Systems](#distributed-systems)",
        "subsection_labels": {},
    },
    "environment": {
        "index_heading": "### Environment",
        "root_label": "[Environment](./articles/README.md#environment)",
        "dir_label": "[Environment](#environment)",
        "subsection_labels": {},
    },
    "frontend": {
        "index_heading": "### Frontend",
        "root_label": "[Frontend](./articles/README.md#frontend)",
        "dir_label": "[Frontend](#frontend)",
        "subsection_labels": {},
    },
    "licensing": {
        "index_heading": "### Licensing",
        "root_label": "[Licensing](./articles/README.md#licensing)",
        "dir_label": "[Licensing](#licensing)",
        "subsection_labels": {},
    },
    "philosophy": {
        "index_heading": "### Philosophy",
        "root_label": "[Philosophy](./articles/README.md#philosophy)",
        "dir_label": "[Philosophy](#philosophy)",
        "subsection_labels": {
            "#### Career & Growth": "Career",
            "#### Critical Thinking & Emotions": "Critical Thinking",
            "#### Information & Thought": "Info & Thought",
            "#### Personal & Wellness": "Wellness",
            "#### Programming Philosophy": "Programming",
        },
    },
    "testing": {
        "index_heading": "### Testing",
        "root_label": "[Testing](./articles/README.md#testing)",
        "dir_label": "[Testing](#testing)",
        "subsection_labels": {},
    },
    "tools": {
        "index_heading": "### Tools",
        "root_label": "[Tools](./articles/README.md#tools)",
        "dir_label": "[Tools](#tools)",
        "subsection_labels": {},
    },
    "travel": {
        "index_heading": "### Travel",
        "root_label": "[Travel](./articles/README.md#travel)",
        "dir_label": "[Travel](#travel)",
        "subsection_labels": {},
    },
}

HEADING_TO_CATEGORY = {cfg["index_heading"]: cat for cat, cfg in CATEGORY_CONFIG.items()}
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")


def parse_long_date(raw: str) -> date | None:
    raw_clean = raw.strip()
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(raw_clean, fmt).date()
        except ValueError:
            continue
    return None


def format_short_date(dt: date) -> str:
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def format_long_date(dt: date) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def scan_articles(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Scan articles/**/*.md and parse title, **Date:**, **Last Updated:**, and ## Changelog."""
    articles: dict[str, dict[str, Any]] = {}
    pattern = str(repo_root / "articles" / "**" / "*.md")
    for abs_path_str in sorted(glob.glob(pattern, recursive=True)):
        abs_path = Path(abs_path_str)
        rel_path = abs_path.relative_to(repo_root).as_posix()
        if rel_path in {"articles/README.md", "articles/CHANGELOG.md"}:
            continue
        parts = Path(rel_path).parts
        if len(parts) != 3 or not KEBAB_RE.match(abs_path.name):
            raise ValueError(f"Invariant 2 violation: invalid article path {rel_path}")
        category = parts[1]
        content = abs_path.read_text(encoding="utf-8")
        head = content[:1500]

        title_match = re.search(r"^#\s+(.+?)\s*$", head, flags=re.MULTILINE)
        title = title_match.group(1).strip() if title_match else abs_path.stem.replace("-", " ").title()

        date_match = re.search(r"^\*\*Date:\*\*\s*(.+?)\s*$", head, flags=re.MULTILINE)
        pub_date = parse_long_date(date_match.group(1)) if date_match else None

        lu_match = re.search(r"^\*\*Last Updated:\*\*\s*(.+?)\s*$", head, flags=re.MULTILINE)
        last_updated = parse_long_date(lu_match.group(1)) if lu_match else None

        has_valid_changelog = False
        latest_cl_note = ""
        cl_match = re.search(r"^## Changelog\s*$", content, flags=re.MULTILINE)
        if cl_match:
            cl_body = content[cl_match.end():]
            next_h2 = re.search(r"^##\s+", cl_body, flags=re.MULTILINE)
            if next_h2:
                cl_body = cl_body[:next_h2.start()]
            bullet_match = re.search(r"^\s*[-*]\s+\*\*[^*]+:\*\*\s*(.+)$", cl_body, flags=re.MULTILINE)
            if bullet_match:
                has_valid_changelog = True
                latest_cl_note = bullet_match.group(1).strip().rstrip(".")

        articles[rel_path] = {
            "rel_path": rel_path,
            "articles_rel_path": f"{category}/{abs_path.name}",
            "category": category,
            "title": title,
            "date": pub_date,
            "last_updated": last_updated,
            "has_valid_changelog": has_valid_changelog,
            "latest_cl_note": latest_cl_note,
        }
    return articles


def parse_existing_badges_and_titles(
    root_readme_text: str,
    articles_readme_text: str,
) -> dict[str, Any]:
    """Capture current [NEW], [UPDATED], existing order, display titles, and summaries."""
    new_set: set[str] = set()
    updated_set: set[str] = set()
    display_titles: dict[str, str] = {}

    in_index = False
    for line in articles_readme_text.splitlines():
        if line.strip() == "## Article Index":
            in_index = True
            continue
        if not in_index:
            continue
        m = re.match(r"^\s*-\s*\[([^\]]+)\]\(([^)]+\.md)\)(.*)$", line)
        if m:
            title, rel_from_articles, suffix = m.group(1), m.group(2), m.group(3)
            norm = os.path.normpath(os.path.join("articles", rel_from_articles)).replace(os.sep, "/")
            display_titles[norm] = title
            if "[NEW]" in suffix:
                new_set.add(norm)
            if "[UPDATED]" in suffix:
                updated_set.add(norm)

    root_new_pos: dict[str, int] = {}
    root_updated_pos: dict[str, int] = {}
    root_updated_summaries: dict[str, str] = {}

    new_idx = 0
    upd_idx = 0
    for line in root_readme_text.splitlines():
        m_new = re.match(
            r"^\s*\*\s*\[([^\]]+)\]\(([^)]+\.md)\)\s*\*\([^)]+\)\*\s*`\[NEW\]`\s*$",
            line,
        )
        if m_new:
            norm = os.path.normpath(m_new.group(2)).replace(os.sep, "/")
            display_titles.setdefault(norm, m_new.group(1))
            root_new_pos[norm] = new_idx
            new_idx += 1
            continue

        m_upd = re.match(
            r"^\s*\*\s*\[([^\]]+)\]\(([^)]+\.md)\)\s*\*\(Updated\s+[^—]+—\s*(.+?)\)\*\s*`\[UPDATED\]`\s*$",
            line,
        )
        if m_upd:
            norm = os.path.normpath(m_upd.group(2)).replace(os.sep, "/")
            display_titles.setdefault(norm, m_upd.group(1))
            root_updated_pos[norm] = upd_idx
            root_updated_summaries[norm] = m_upd.group(3).strip()
            upd_idx += 1

    return {
        "current_new_set": new_set,
        "current_updated_set": updated_set,
        "display_titles": display_titles,
        "root_new_pos": root_new_pos,
        "root_updated_pos": root_updated_pos,
        "root_updated_summaries": root_updated_summaries,
    }


def compute_badge_cohorts(
    articles: dict[str, dict[str, Any]],
    existing_state: dict[str, Any],
    handoffs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute deterministic Hybrid Window [NEW] cohort and [UPDATED] set (Invariant 4)."""
    dated = {p: meta["date"] for p, meta in articles.items() if meta["date"] is not None}
    if not dated:
        raise ValueError("No articles with valid **Date:** headers found.")

    handoff_added = {h["article_path"] for h in handoffs if h["action"] == "Added"}
    handoff_updated = {
        h["article_path"]
        for h in handoffs
        if h["action"] in {"Updated", "Simplified", "Reviewed & Updated"}
    }

    current_new = existing_state["current_new_set"]
    root_new_pos = existing_state["root_new_pos"]
    current_updated = existing_state["current_updated_set"]
    root_updated_pos = existing_state["root_updated_pos"]

    latest_date = max(dated.values())
    within_7d = [p for p, dt in dated.items() if (latest_date - dt).days <= 7]
    expected_new_count = min(5, max(min(3, len(dated)), len(within_7d)))

    # Tie-breaker favors newly added handoffs, then existing [NEW] holders and existing root order.
    ranked_new_candidates = sorted(
        dated.keys(),
        key=lambda p: (
            -dated[p].toordinal(),
            0 if p in handoff_added else 1,
            0 if p in current_new else 1,
            root_new_pos.get(p, 999999),
            p,
        ),
    )
    new_cohort_list = ranked_new_candidates[:expected_new_count]
    new_cohort_set = set(new_cohort_list)
    evicted_new = sorted(current_new - new_cohort_set)

    # [UPDATED] holds at most 5 revised articles outside [NEW], preserving active entries + handoffs.
    updated_pool = {
        p
        for p in (current_updated | handoff_updated)
        if p in articles
        and p not in new_cohort_set
        and articles[p]["last_updated"] is not None
        and articles[p]["has_valid_changelog"]
    }
    ranked_updated = sorted(
        updated_pool,
        key=lambda p: (
            -articles[p]["last_updated"].toordinal(),
            0 if p in handoff_updated else 1,
            root_updated_pos.get(p, 999999),
            p,
        ),
    )
    updated_cohort_list = ranked_updated[:5]
    updated_cohort_set = set(updated_cohort_list)

    return {
        "latest_date": latest_date,
        "within_7d_count": len(within_7d),
        "expected_new_count": expected_new_count,
        "new_cohort_list": new_cohort_list,
        "new_cohort_set": new_cohort_set,
        "evicted_new": evicted_new,
        "updated_cohort_list": updated_cohort_list,
        "updated_cohort_set": updated_cohort_set,
    }


def reconcile_articles_readme(
    original_text: str,
    articles: dict[str, dict[str, Any]],
    cohorts: dict[str, Any],
    handoff_titles: dict[str, str],
) -> tuple[str, dict[str, str]]:
    """Update articles/README.md index entries, badges, tree counts, and Category Directory counts."""
    lines = original_text.splitlines()
    new_set = cohorts["new_cohort_set"]
    updated_set = cohorts["updated_cohort_set"]

    # Map basename -> unique path for moved-link self-healing
    by_basename: dict[str, list[str]] = {}
    for rel_path, meta in articles.items():
        by_basename.setdefault(Path(rel_path).name, []).append(meta["articles_rel_path"])

    # Locate ## Article Index
    index_start = next((i for i, ln in enumerate(lines) if ln.strip() == "## Article Index"), None)
    if index_start is None:
        raise ValueError("Missing '## Article Index' in articles/README.md")

    header_lines = lines[: index_start + 1]
    index_lines = lines[index_start + 1 :]

    # Parse ## Article Index into category/subsection blocks, self-heal moved links, strip old badges
    indexed_paths: set[str] = set()
    updated_index_lines: list[str] = []

    current_cat: str | None = None
    current_sub: str | None = None
    cat_entries: dict[str, int] = {cat: 0 for cat in CATEGORY_CONFIG}
    sub_entries: dict[str, dict[str, int]] = {
        cat: {sub: 0 for sub in cfg["subsection_labels"]}
        for cat, cfg in CATEGORY_CONFIG.items()
    }

    # First pass: locate category insertion points and normalize existing entry lines
    first_block_end_line: dict[str, int] = {}
    for raw_line in index_lines:
        stripped = raw_line.strip()
        if stripped in HEADING_TO_CATEGORY:
            current_cat = HEADING_TO_CATEGORY[stripped]
            current_sub = None
            updated_index_lines.append(raw_line)
            continue
        if current_cat and stripped.startswith("#### "):
            current_sub = stripped
            updated_index_lines.append(raw_line)
            continue

        m = re.match(r"^(\s*-\s*\[)([^\]]+)(\]\()([^)]+\.md)(\))(?:\s*\[(?:NEW|UPDATED)\])?\s*$", raw_line)
        if m:
            prefix, title, mid, target_rel, close_paren = m.groups()
            norm_full = os.path.normpath(os.path.join("articles", target_rel)).replace(os.sep, "/")
            if norm_full not in articles:
                candidates = by_basename.get(Path(target_rel).name, [])
                if len(candidates) == 1:
                    target_rel = candidates[0]
                    norm_full = f"articles/{target_rel}"
            indexed_paths.add(norm_full)
            badge = ""
            if norm_full in new_set:
                badge = " [NEW]"
            elif norm_full in updated_set:
                badge = " [UPDATED]"
            updated_index_lines.append(f"{prefix}{title}{mid}{target_rel}{close_paren}{badge}")
            continue

        updated_index_lines.append(raw_line)

    # Insert any missing articles alphabetically into their target category / first subsection
    missing_paths = sorted(set(articles.keys()) - indexed_paths)
    if missing_paths:
        missing_by_cat: dict[str, list[dict[str, Any]]] = {}
        for mp in missing_paths:
            meta = articles[mp]
            missing_by_cat.setdefault(meta["category"], []).append(meta)

        rebuilt: list[str] = []
        i = 0
        while i < len(updated_index_lines):
            ln = updated_index_lines[i]
            stripped = ln.strip()
            if stripped in HEADING_TO_CATEGORY:
                cat = HEADING_TO_CATEGORY[stripped]
                rebuilt.append(ln)
                i += 1
                if cat in missing_by_cat:
                    # Advance past optional blank line and optional first #### subsection header
                    while i < len(updated_index_lines) and updated_index_lines[i].strip() == "":
                        rebuilt.append(updated_index_lines[i])
                        i += 1
                    if i < len(updated_index_lines) and updated_index_lines[i].strip().startswith("#### "):
                        rebuilt.append(updated_index_lines[i])
                        i += 1
                        while i < len(updated_index_lines) and updated_index_lines[i].strip() == "":
                            rebuilt.append(updated_index_lines[i])
                            i += 1

                    # Collect contiguous bullet lines in this target block
                    block_bullets: list[str] = []
                    while i < len(updated_index_lines) and re.match(r"^\s*-\s*\[", updated_index_lines[i]):
                        block_bullets.append(updated_index_lines[i])
                        i += 1

                    for meta in missing_by_cat[cat]:
                        rp = meta["rel_path"]
                        title = handoff_titles.get(rp, meta["title"])
                        badge = " [NEW]" if rp in new_set else (" [UPDATED]" if rp in updated_set else "")
                        block_bullets.append(f"- [{title}]({meta['articles_rel_path']}){badge}")

                    block_bullets.sort(
                        key=lambda b: (m.group(1).lower() if (m := re.match(r"^\s*-\s*\[([^\]]+)\]", b)) else b.lower())
                    )
                    rebuilt.extend(block_bullets)
                    continue
            else:
                rebuilt.append(ln)
                i += 1
        updated_index_lines = rebuilt

    # Second pass: compute exact category and subsection counts & collect final titles
    final_titles: dict[str, str] = {}
    current_cat = None
    current_sub = None
    for ln in updated_index_lines:
        stripped = ln.strip()
        if stripped in HEADING_TO_CATEGORY:
            current_cat = HEADING_TO_CATEGORY[stripped]
            current_sub = None
            continue
        if current_cat and stripped.startswith("#### "):
            current_sub = stripped
            continue
        m = re.match(r"^\s*-\s*\[([^\]]+)\]\(([^)]+\.md)\)", ln)
        if m and current_cat:
            norm_full = os.path.normpath(os.path.join("articles", m.group(2))).replace(os.sep, "/")
            final_titles[norm_full] = m.group(1)
            cat_entries[current_cat] += 1
            if current_sub and current_sub in sub_entries[current_cat]:
                sub_entries[current_cat][current_sub] += 1

    total_articles = sum(cat_entries.values())

    # Update header_lines (## Organization tree & ## Category Directory table)
    new_header_lines: list[str] = []
    for ln in header_lines:
        # Organization tree lines: ├── ai/ ... (17)
        tree_match = re.match(r"^(.*?(?:├──|└──)\s+([a-z0-9-]+)/.*?\()(\d+)(\).*)$", ln)
        if tree_match and tree_match.group(2) in cat_entries:
            cat = tree_match.group(2)
            ln = f"{tree_match.group(1)}{cat_entries[cat]}{tree_match.group(4)}"
            new_header_lines.append(ln)
            continue

        # Category Directory heading: ## Category Directory (114 Articles)
        if ln.startswith("## Category Directory ("):
            ln = f"## Category Directory ({total_articles} Articles)"
            new_header_lines.append(ln)
            continue

        # Category Directory table rows
        matched_row = False
        for cat, cfg in CATEGORY_CONFIG.items():
            prefix = f"| {cfg['dir_label']} |"
            if ln.startswith(prefix):
                if cfg["subsection_labels"]:
                    sub_parts = [
                        f"{short_label} ({sub_entries[cat].get(sub_heading, 0)})"
                        for sub_heading, short_label in cfg["subsection_labels"].items()
                    ]
                    sub_col = ", ".join(sub_parts)
                else:
                    sub_col = "—"
                ln = f"| {cfg['dir_label']} | {cat_entries[cat]} | {sub_col} |"
                matched_row = True
                break
        new_header_lines.append(ln)

    result_text = "\n".join(new_header_lines + updated_index_lines)
    if original_text.endswith("\n"):
        result_text += "\n"
    return result_text, final_titles


def reconcile_root_readme(
    original_text: str,
    articles: dict[str, dict[str, Any]],
    cohorts: dict[str, Any],
    final_titles: dict[str, str],
    existing_state: dict[str, Any],
    handoff_summaries: dict[str, str],
) -> str:
    """Update README.md total count, Recent Additions ([NEW]), Recently Updated ([UPDATED]), and topic counts."""
    lines = original_text.splitlines()
    total_articles = len(articles)

    # Category counts from scanned articles on disk
    cat_counts: dict[str, int] = {cat: 0 for cat in CATEGORY_CONFIG}
    for meta in articles.values():
        cat_counts[meta["category"]] = cat_counts.get(meta["category"], 0) + 1

    # Build Recent Additions block
    new_bullets: list[str] = []
    for rp in cohorts["new_cohort_list"]:
        title = final_titles.get(rp, articles[rp]["title"])
        short_dt = format_short_date(articles[rp]["date"])
        new_bullets.append(f"  * [{title}](./{rp}) *({short_dt})* `[NEW]`")

    # Build Recently Updated block
    updated_bullets: list[str] = []
    existing_summaries = existing_state["root_updated_summaries"]
    for rp in cohorts["updated_cohort_list"]:
        title = final_titles.get(rp, articles[rp]["title"])
        short_dt = format_short_date(articles[rp]["last_updated"])
        summary = (
            handoff_summaries.get(rp)
            or existing_summaries.get(rp)
            or articles[rp]["latest_cl_note"]
            or "updated content and cross-links"
        )
        summary = summary.rstrip(".")
        updated_bullets.append(f"  * [{title}](./{rp}) *(Updated {short_dt} — {summary})* `[UPDATED]`")

    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]

        if "* **[Browse Full Article Index (" in ln:
            ln = re.sub(
                r"\(\d+ Articles\)",
                f"({total_articles} Articles)",
                ln,
            )
            out.append(ln)
            i += 1
            continue

        if ln.startswith("* **Recent Additions ("):
            out.append(ln)
            i += 1
            while i < len(lines) and re.match(r"^\s+\*\s+\[", lines[i]):
                i += 1
            out.extend(new_bullets)
            continue

        if ln.startswith("* **Recently Updated ("):
            out.append(ln)
            i += 1
            while i < len(lines) and re.match(r"^\s+\*\s+\[", lines[i]):
                i += 1
            out.extend(updated_bullets)
            continue

        # Topic table row update: | [Category](./articles/README.md#anchor) | <count> | Focus Areas |
        replaced = False
        for cat, cfg in CATEGORY_CONFIG.items():
            prefix = f"| {cfg['root_label']} |"
            if ln.startswith(prefix):
                parts = ln.split("|")
                if len(parts) >= 5:
                    parts[2] = f" {cat_counts[cat]} "
                    ln = "|".join(parts)
                    replaced = True
                break
        out.append(ln)
        i += 1

    result = "\n".join(out)
    if original_text.endswith("\n"):
        result += "\n"
    return result


def parse_review_report_metadata(report_path: Path, repo_root: Path) -> dict[str, Any] | None:
    """Fallback parser to register an unlisted review report in reviews/README.md."""
    text = report_path.read_text(encoding="utf-8")
    rel = report_path.relative_to(repo_root).as_posix()
    parts = Path(rel).parts
    if len(parts) != 3 or not parts[2].endswith("-review.md"):
        return None
    category = parts[1]
    slug = parts[2][: -len("-review.md")]

    title_m = re.search(r"^#\s+Verification & Review Report:\s*(.+)$", text, flags=re.MULTILINE)
    title = title_m.group(1).strip() if title_m else slug
    date_m = re.search(r"^\*\*Review Date:\*\*\s*(.+)$", text, flags=re.MULTILINE)
    dt = parse_long_date(date_m.group(1)) if date_m else None
    short_dt = format_short_date(dt) if dt else (date_m.group(1).strip() if date_m else "")

    score_m = re.search(
        r"\*\*Overall Score:\*\*\s*`([0-9.]+)\s*/\s*10`\s*\(Before\)\s*(?:→|->)\s*`([0-9.]+)\s*/\s*10`\s*\(After\)\s*\|\s*\*\*Delta:\*\*\s*`([^`]+)`",
        text,
    )
    if not score_m:
        return None

    return {
        "article_path": f"articles/{category}/{slug}.md",
        "title": title,
        "category": category,
        "report_path": rel,
        "before_score": float(score_m.group(1)),
        "after_score": float(score_m.group(2)),
        "delta": score_m.group(3).strip(),
        "review_date": short_dt,
    }


def reconcile_reviews_readme(
    original_text: str,
    repo_root: Path,
    handoffs: list[dict[str, Any]],
    final_titles: dict[str, str],
) -> str:
    """Insert or update rows in reviews/README.md for handoff review_move payloads and disk reports."""
    rows_to_upsert: dict[str, dict[str, Any]] = {}

    # Scan existing review reports on disk so missing ones are self-healed
    for abs_str in sorted(glob.glob(str(repo_root / "reviews" / "**" / "*-review.md"), recursive=True)):
        meta = parse_review_report_metadata(Path(abs_str), repo_root)
        if meta:
            rows_to_upsert[meta["report_path"]] = meta

    # Apply explicit handoff review_move payloads with authoritative values
    for h in handoffs:
        rm = h.get("review_move")
        if not rm:
            continue
        ap = h["article_path"]
        category = Path(ap).parts[1]
        rpath = rm["report_path"]
        dt_parsed = parse_long_date(rm["review_date"])
        short_dt = format_short_date(dt_parsed) if dt_parsed else rm["review_date"]
        rows_to_upsert[rpath] = {
            "article_path": ap,
            "title": final_titles.get(ap, h["title"]),
            "category": category,
            "report_path": rpath,
            "before_score": float(rm["before_score"]),
            "after_score": float(rm["after_score"]),
            "delta": rm["delta"],
            "review_date": short_dt,
        }

    lines = original_text.splitlines()
    table_header_idx = next(
        (i for i, ln in enumerate(lines) if ln.strip().startswith("| Article | Category | Review Report |")),
        None,
    )
    if table_header_idx is None:
        return original_text

    prefix_lines = lines[: table_header_idx + 2]
    existing_rows = lines[table_header_idx + 2 :]

    updated_rows: list[str] = []
    seen_reports: set[str] = set()
    for ln in existing_rows:
        if not ln.strip().startswith("|"):
            updated_rows.append(ln)
            continue
        m = re.search(r"\]\(([^)]+-review\.md)\)", ln)
        if m:
            rpath = f"reviews/{m.group(1)}"
            seen_reports.add(rpath)
            if rpath in rows_to_upsert:
                info = rows_to_upsert[rpath]
                rel_from_reviews = Path(info["report_path"]).relative_to("reviews").as_posix()
                updated_rows.append(
                    f"| [{info['title']}](../{info['article_path']}) | `{info['category']}` | "
                    f"[Review Report]({rel_from_reviews}) | `{info['before_score']:.1f}` | "
                    f"`{info['after_score']:.1f}` | `{info['delta']}` | {info['review_date']} |"
                )
                continue
        updated_rows.append(ln)

    # Prepend newly added review reports that were not already in reviews/README.md
    new_rows: list[str] = []
    for rpath, info in sorted(rows_to_upsert.items()):
        if rpath not in seen_reports:
            rel_from_reviews = Path(info["report_path"]).relative_to("reviews").as_posix()
            new_rows.append(
                f"| [{info['title']}](../{info['article_path']}) | `{info['category']}` | "
                f"[Review Report]({rel_from_reviews}) | `{info['before_score']:.1f}` | "
                f"`{info['after_score']:.1f}` | `{info['delta']}` | {info['review_date']} |"
            )

    result = "\n".join(prefix_lines + new_rows + updated_rows)
    if original_text.endswith("\n"):
        result += "\n"
    return result


def reconcile_changelog(
    original_text: str,
    articles: dict[str, dict[str, Any]],
    cohorts: dict[str, Any],
    handoffs: list[dict[str, Any]],
    final_titles: dict[str, str],
) -> str:
    """Insert handoff events and [NEW] rotation notices into articles/CHANGELOG.md idempotently."""
    events_by_date: dict[date, list[str]] = {}
    new_set = cohorts["new_cohort_set"]

    latest_handoff_date: date | None = None
    for h in handoffs:
        ap = h["article_path"]
        meta = articles.get(ap)
        if not meta:
            continue
        art_rel = meta["articles_rel_path"]
        title = final_titles.get(ap, h["title"])
        action = h["action"]
        summary = h["changelog_summary"].strip().rstrip(".")

        raw_date = h.get("last_updated") or h["date"]
        ev_date = parse_long_date(raw_date) or cohorts["latest_date"]
        if latest_handoff_date is None or ev_date > latest_handoff_date:
            latest_handoff_date = ev_date

        if action == "Added":
            bullet = f"* **Added:** [{title}]({art_rel}) — {summary}."
        elif action == "Updated":
            bullet = f"* **Updated:** [{title}]({art_rel}) — {summary}."
        elif action == "Simplified":
            bullet = f"* **Simplified:** [{title}]({art_rel}) — {summary}."
        elif action == "Reviewed & Updated":
            rm = h.get("review_move")
            if rm:
                report_rel = f"../{rm['report_path']}"
                bullet = f"* **Reviewed & Updated:** [{title}]({art_rel}) — {summary} ([Review Report]({report_rel}))."
            else:
                bullet = f"* **Reviewed & Updated:** [{title}]({art_rel}) — {summary}."
            if ap in new_set:
                bullet += " *(Retains active `[NEW]` badge.)*"
        else:
            continue
        events_by_date.setdefault(ev_date, []).append(bullet)

    # Record [NEW] rotations if any occurred
    if cohorts["evicted_new"]:
        rot_date = latest_handoff_date or cohorts["latest_date"]
        for evicted_path in cohorts["evicted_new"]:
            meta = articles.get(evicted_path)
            if not meta:
                continue
            title = final_titles.get(evicted_path, meta["title"])
            art_rel = meta["articles_rel_path"]
            bullet = (
                f"* **Rotated (`[NEW]`):** [{title}]({art_rel}) "
                "rotated out of the 5-article `Recent Additions` cap."
            )
            events_by_date.setdefault(rot_date, []).append(bullet)

    if not events_by_date:
        return original_text

    lines = original_text.splitlines()
    for ev_date in sorted(events_by_date.keys()):
        month_header = f"## {ev_date.strftime('%B %Y')}"
        day_header = f"### {format_long_date(ev_date)}"
        bullets = events_by_date[ev_date]

        # Ensure month header exists
        if month_header not in lines:
            sep_idx = next((i for i, ln in enumerate(lines) if ln.strip() == "---"), None)
            insert_at = (sep_idx + 1) if sep_idx is not None else len(lines)
            lines[insert_at:insert_at] = ["", month_header]

        month_idx = lines.index(month_header)

        # Ensure day header exists in reverse chronological position inside month section
        if day_header not in lines:
            # Find first ### heading inside this month older than ev_date
            insert_idx = month_idx + 1
            while insert_idx < len(lines):
                ln = lines[insert_idx].strip()
                if ln.startswith("## ") and ln != month_header:
                    break
                if ln.startswith("### "):
                    existing_dt = parse_long_date(ln[4:])
                    if existing_dt and existing_dt < ev_date:
                        break
                insert_idx += 1
            lines[insert_idx:insert_idx] = ["", day_header]

        day_idx = lines.index(day_header)
        # Collect existing bullets under this day_header for idempotency
        day_end = day_idx + 1
        while day_end < len(lines) and not lines[day_end].startswith(("## ", "### ")):
            day_end += 1

        existing_day_block = "\n".join(lines[day_idx:day_end])
        to_insert = []
        for b in bullets:
            # Check exact match or matching (action prefix + target path)
            action_link_m = re.match(r"^(\*\s+\*\*[^*]+\*\*\s+\[[^\]]+\]\([^)]+\))", b)
            sig = action_link_m.group(1) if action_link_m else b
            if b not in existing_day_block and sig not in existing_day_block:
                to_insert.append(b)

        if to_insert:
            insert_pos = day_idx + 1
            lines[insert_pos:insert_pos] = to_insert

    result = "\n".join(lines)
    if original_text.endswith("\n"):
        result += "\n"
    return result


def load_handoffs(handoff_arg: str | None, handoff_file: str | None) -> list[dict[str, Any]]:
    raw_items: list[dict[str, Any]] = []
    for raw_source in (handoff_arg, Path(handoff_file).read_text(encoding="utf-8") if handoff_file else None):
        if not raw_source:
            continue
        parsed = json.loads(raw_source)
        if isinstance(parsed, dict):
            raw_items.append(parsed)
        elif isinstance(parsed, list):
            raw_items.extend(parsed)
        else:
            raise ValueError("Handoff payload must be a JSON object or JSON array of objects.")

    for idx, item in enumerate(raw_items):
        validate_against_schema(item, INDEX_HANDOFF_SCHEMA, f"handoff[{idx}]")
    return raw_items


def write_if_changed(path: Path, new_text: str, dry_run: bool) -> bool:
    old_text = path.read_text(encoding="utf-8") if path.exists() else ""
    if new_text == old_text:
        return False
    if dry_run:
        print(f"[dry-run] Would update {path.relative_to(REPO_ROOT).as_posix()}")
    else:
        path.write_text(new_text, encoding="utf-8")
        print(f"✅ Updated {path.relative_to(REPO_ROOT).as_posix()}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Single-writer index, badge, review & changelog reconciler.")
    parser.add_argument("--handoff", help="JSON string of one INDEX_HANDOFF_SCHEMA object or array.")
    parser.add_argument("--handoff-file", help="Path to JSON file containing handoff payload(s).")
    parser.add_argument("--dry-run", action="store_true", help="Preview mutations without writing files.")
    parser.add_argument("--skip-verify", action="store_true", help="Skip running bash verify_links.sh.")
    args = parser.parse_args()

    handoffs = load_handoffs(args.handoff, args.handoff_file)
    articles = scan_articles(REPO_ROOT)

    root_readme_path = REPO_ROOT / "README.md"
    articles_readme_path = REPO_ROOT / "articles" / "README.md"
    changelog_path = REPO_ROOT / "articles" / "CHANGELOG.md"
    reviews_readme_path = REPO_ROOT / "reviews" / "README.md"

    root_readme_orig = root_readme_path.read_text(encoding="utf-8")
    articles_readme_orig = articles_readme_path.read_text(encoding="utf-8")
    changelog_orig = changelog_path.read_text(encoding="utf-8")
    reviews_readme_orig = reviews_readme_path.read_text(encoding="utf-8")

    existing_state = parse_existing_badges_and_titles(root_readme_orig, articles_readme_orig)
    cohorts = compute_badge_cohorts(articles, existing_state, handoffs)

    handoff_titles = {h["article_path"]: h["title"] for h in handoffs}
    handoff_summaries = {
        h["article_path"]: h["changelog_summary"]
        for h in handoffs
        if h["action"] in {"Updated", "Simplified", "Reviewed & Updated"}
    }

    articles_readme_new, final_titles = reconcile_articles_readme(
        articles_readme_orig,
        articles,
        cohorts,
        handoff_titles,
    )
    root_readme_new = reconcile_root_readme(
        root_readme_orig,
        articles,
        cohorts,
        final_titles,
        existing_state,
        handoff_summaries,
    )
    reviews_readme_new = reconcile_reviews_readme(
        reviews_readme_orig,
        REPO_ROOT,
        handoffs,
        final_titles,
    )
    changelog_new = reconcile_changelog(
        changelog_orig,
        articles,
        cohorts,
        handoffs,
        final_titles,
    )

    changed = False
    changed |= write_if_changed(articles_readme_path, articles_readme_new, args.dry_run)
    changed |= write_if_changed(root_readme_path, root_readme_new, args.dry_run)
    changed |= write_if_changed(reviews_readme_path, reviews_readme_new, args.dry_run)
    changed |= write_if_changed(changelog_path, changelog_new, args.dry_run)

    if not changed:
        print(
            f"ℹ️ No index/changelog drift detected ({len(articles)} articles, "
            f"{len(cohorts['new_cohort_list'])}/{cohorts['expected_new_count']} [NEW], "
            f"{len(cohorts['updated_cohort_list'])}/5 [UPDATED])."
        )

    if not args.dry_run and not args.skip_verify:
        proc = subprocess.run(["bash", "verify_links.sh"], cwd=str(REPO_ROOT), env=get_uv_env(), check=False)
        return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
