#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Hybrid single/batch content workflow orchestrator for Antigravity `run_workflow` (Option H3).

Supports `mode` in {"create", "update", "simplify"} across single (`article_path`)
or parallel batch (`article_paths` / `items`) targets, enforcing Invariants 1-3 and
zero-loss link retention via `verify_article_mutation()` before single-writer
reconciliation in `reconcile_indexes.py`.

Invoke via `run_workflow`:
  run_workflow(
      Script=(
          "import runpy\\n"
          "mod = runpy.run_path('.agent/skills/create_article/scripts/run_content_workflow.py', init_globals=globals())\\n"
          "await mod['run_pipeline'](globals())\\n"
      ),
      Args={"mode": "simplify", "article_paths": ["articles/<category>/<slug>.md"]},
      Description="Run schema-validated hybrid content workflow",
  )

Self-test locally without LLM calls (via uv/pip runner):
  bash .agent/skills/organize_readme/scripts/run_python.sh .agent/skills/create_article/scripts/run_content_workflow.py --self-test
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import runpy
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[4]
REVIEW_SCRIPTS_DIR = DEFAULT_REPO_ROOT / ".agent" / "skills" / "review_article" / "scripts"
RECONCILER_SCRIPT = (
    DEFAULT_REPO_ROOT / ".agent" / "skills" / "organize_readme" / "scripts" / "reconcile_indexes.py"
)
REVIEW_WORKFLOW_SCRIPT = REVIEW_SCRIPTS_DIR / "run_review_workflow.py"

if str(REVIEW_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(REVIEW_SCRIPTS_DIR))

from schemas import (  # noqa: E402
    CONTENT_MUTATION_RESULT_SCHEMA,
    INDEX_HANDOFF_SCHEMA,
    SchemaValidationError,
    build_python_cmd,
    ensure_dependencies,
    extract_markdown_links,
    get_uv_env,
    validate_against_schema,
    verify_article_mutation,
)

MODE_TO_ACTION: dict[str, str] = {
    "create": "Added",
    "update": "Updated",
    "simplify": "Simplified",
}

ARTICLE_PATH_RE = re.compile(r"^articles/([a-z0-9-]+)/([a-z0-9-]+)\.md$")


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


def _normalize_items(wf_args: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize single (`article_path`) or batch (`article_paths` / `items`) workflow arguments."""
    raw_items: list[dict[str, Any]] = []
    if wf_args.get("items"):
        for entry in wf_args["items"]:
            if not isinstance(entry, dict) or not entry.get("article_path"):
                raise ValueError("Each entry in 'items' must be an object containing 'article_path'.")
            raw_items.append(dict(entry))
    elif wf_args.get("article_paths"):
        for path in wf_args["article_paths"]:
            raw_items.append({"article_path": path})
    elif wf_args.get("article_path"):
        raw_items.append({"article_path": wf_args["article_path"]})
    else:
        raise ValueError(
            "Missing target specification: provide 'article_path', 'article_paths', or 'items'."
        )

    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for item in raw_items:
        rel_path = str(item["article_path"]).strip().lstrip("./")
        if not ARTICLE_PATH_RE.match(rel_path):
            raise ValueError(
                f"article_path must match 'articles/<category>/<kebab-case>.md', got: {item['article_path']!r}"
            )
        if rel_path in seen:
            raise ValueError(f"Duplicate target article_path in batch: {rel_path!r}")
        seen.add(rel_path)
        item["article_path"] = rel_path
        normalized.append(item)
    return normalized


def _build_scoped_prompt(
    mode: str,
    action: str,
    item: dict[str, Any],
    wf_args: dict[str, Any],
    today_long: str,
    today_short: str,
    baseline: dict[str, Any],
) -> str:
    rel_path = item["article_path"]
    category = rel_path.split("/", 2)[1]
    instructions = item.get("instructions") or wf_args.get("instructions") or ""
    source_url = item.get("source_url") or wf_args.get("source_url") or ""
    title_hint = item.get("title") or wf_args.get("title") or ""

    shared_guard = (
        "STRICT WRITE SCOPE (Option A4 + H3 Single-Writer Partitioning):\n"
        f"- Target article: `{rel_path}` (category: `{category}`).\n"
        "- NEVER edit `README.md`, `articles/README.md`, `reviews/README.md`, or `articles/CHANGELOG.md`. "
        "`reconcile_indexes.py` handles all singleton index/badge/changelog mutations in Stage 4.\n"
        "- Strictly enforce `.agent/rules/AGENTS.md` Invariants 1-3:\n"
        "  * Invariant 1: Pure OSI-approved open-source systems only; include the exact `Scope & Licensing Note` callout when covering tools/systems.\n"
        "  * Invariant 2: Lowercase `kebab-case.md` layout inside existing `articles/<category>/` directories.\n"
        "  * Invariant 3: Bottom section order `## Related Articles` (2-3 valid relative `.md` links) -> `## References` (if present) -> `## Changelog` (at very bottom, reverse chronological).\n"
    )

    extra_lines: list[str] = []
    if title_hint:
        extra_lines.append(f"- Suggested Title: `{title_hint}`")
    if source_url:
        extra_lines.append(f"- Source URL to summarize/cite: `{source_url}`")
    if instructions:
        extra_lines.append(f"- Task Instructions: {instructions}")
    extra_block = ("\n".join(extra_lines) + "\n") if extra_lines else ""

    if mode == "create":
        mode_guidance = (
            f"MODE: Create New Article (`action: '{action}'`)\n"
            f"- Author `{rel_path}` with `# <Title>`, optional `**Source:** [Host](URL)`, `**Date:** {today_long}`, "
            "`## Summary`, `## Key Points`, structured body sections, `## Related Articles` (2-3 verified relative `.md` links), "
            f"optional `## References`, and `## Changelog` seeded with `- **{today_short}:** Initial publication.`.\n"
            "- If you add reciprocal links into closely related sibling articles, update their `**Last Updated:**` and `## Changelog` "
            "and list those exact paths in `reciprocal_articles_touched`.\n"
        )
    elif mode == "update":
        orig_date = baseline.get("original_date") or "<existing Date>"
        mode_guidance = (
            f"MODE: Update Existing Article (`action: '{action}'`)\n"
            f"- Read `{rel_path}` completely before editing.\n"
            f"- PRESERVE immutable `**Date:** {orig_date}` and add/update `**Last Updated:** {today_long}` directly beneath it.\n"
            f"- Preserve ALL {baseline['link_count']} existing links/citations and `## References`.\n"
            f"- Prepend `- **{today_short}:** <concise summary>.` to `## Changelog` at the very bottom (seeding `Initial publication.` if missing).\n"
            "- List any sibling articles modified for reciprocal cross-links in `reciprocal_articles_touched`.\n"
        )
    else:  # simplify
        orig_date = baseline.get("original_date") or "<existing Date>"
        mode_guidance = (
            f"MODE: Simplify & Refactor Article (`action: '{action}'`)\n"
            f"- Read `{rel_path}` completely before editing.\n"
            "- Normalize header hierarchy (`#` -> `##` -> `###`), break up dense paragraphs/cluttered lists, add blank lines around headings/lists, "
            "and add a Mermaid diagram if complex structure warrants visualization.\n"
            f"- PRESERVE immutable `**Date:** {orig_date}` and add/update `**Last Updated:** {today_long}` directly beneath it.\n"
            f"- CRITICAL ZERO-LOSS GUARANTEE: Preserve 100% of the {baseline['link_count']} existing markdown links, citations, `## References`, "
            "`## Related Articles`, and prior `## Changelog` entries.\n"
            f"- Prepend `- **{today_short}:** Simplified formatting and structure (preserving all references and links).` to `## Changelog`.\n"
        )

    return (
        f"You are a Scoped Content Agent for ThoughtsInWords.\n\n"
        f"{shared_guard}\n"
        f"{mode_guidance}"
        f"{extra_block}\n"
        "Return your final structured JSON payload strictly via `finish` matching CONTENT_MUTATION_RESULT_SCHEMA."
    )


async def run_pipeline(runtime_env: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute the 4-stage hybrid content workflow inside `run_workflow` or a mock runtime."""
    ensure_dependencies()
    env: dict[str, Any] = runtime_env if runtime_env is not None else globals()
    repo_root = _resolve_repo_root(env)

    log_fn: Callable[..., Any] = _get_primitive("log", env, default=print)
    phase_fn: Callable[[str], Any] = _get_primitive("phase", env, default=lambda _name: None)
    agent_fn: Callable[..., Any] = _get_primitive("agent", env)
    parallel_fn: Callable[..., Any] = _get_primitive("parallel", env)
    wf_args: dict[str, Any] = _get_primitive("args", env, default={}) or {}

    mode = str(wf_args.get("mode", "")).strip().lower()
    if mode not in MODE_TO_ACTION:
        raise ValueError(f"Unsupported mode {mode!r}; expected one of {sorted(MODE_TO_ACTION)}.")
    action = MODE_TO_ACTION[mode]

    items = _normalize_items(wf_args)
    default_workspace = "share" if len(items) > 1 else "inherit"
    workspace = str(wf_args.get("workspace") or default_workspace)
    if workspace not in {"inherit", "share", "branch"}:
        raise ValueError(f"Invalid workspace mode {workspace!r}; expected 'inherit', 'share', or 'branch'.")

    model = wf_args.get("model")
    chain_review = bool(wf_args.get("chain_review", False))
    dry_run = bool(wf_args.get("dry_run", False))

    today_dt = datetime.now()
    today_long = _format_long_date(today_dt)
    today_short = _format_short_date(today_dt)

    # ------------------------------------------------------------------
    # Stage 1: Baseline Snapshot & Scope Validation
    # ------------------------------------------------------------------
    phase_fn("Stage 1: Baseline Snapshot & Scope Validation")
    baselines: dict[str, dict[str, Any]] = {}
    for item in items:
        rel_path = item["article_path"]
        abs_path = repo_root / rel_path
        if mode == "create":
            if abs_path.exists():
                raise FileExistsError(f"Target article already exists for mode='create': {abs_path}")
            baselines[rel_path] = {
                "before_text": None,
                "original_date": None,
                "links": set(),
                "link_count": 0,
            }
        else:
            if not abs_path.is_file():
                raise FileNotFoundError(f"Target article does not exist on disk for mode={mode!r}: {abs_path}")
            before_text = abs_path.read_text(encoding="utf-8")
            date_m = re.search(r"^\*\*Date:\*\*\s*(.+?)\s*$", before_text[:2000], flags=re.MULTILINE)
            links = extract_markdown_links(before_text)
            baselines[rel_path] = {
                "before_text": before_text,
                "original_date": date_m.group(1).strip() if date_m else None,
                "links": links,
                "link_count": len(links),
            }

    log_fn(
        f"Validated {len(items)} target article(s) for mode='{mode}' "
        f"(action='{action}', workspace='{workspace}')."
    )

    # ------------------------------------------------------------------
    # Stage 2: Scoped Content Subagent Execution
    # ------------------------------------------------------------------
    phase_fn("Stage 2: Scoped Content Subagent Execution")

    def _launch_item(item: dict[str, Any]) -> Any:
        rel_path = item["article_path"]
        prompt = _build_scoped_prompt(
            mode=mode,
            action=action,
            item=item,
            wf_args=wf_args,
            today_long=today_long,
            today_short=today_short,
            baseline=baselines[rel_path],
        )
        kwargs: dict[str, Any] = {
            "schema": CONTENT_MUTATION_RESULT_SCHEMA,
            "role": f"Content {action}: {Path(rel_path).name}",
            "workspace": workspace,
        }
        if model:
            kwargs["model"] = model
        return agent_fn(prompt, **kwargs)

    if len(items) == 1:
        raw_results = [await _launch_item(items[0])]
    else:
        raw_results = await parallel_fn(items, _launch_item)

    # ------------------------------------------------------------------
    # Stage 3: Deterministic Pre-Handoff Article & Link-Retention Gate
    # ------------------------------------------------------------------
    phase_fn("Stage 3: Deterministic Pre-Handoff Article & Link-Retention Gate")
    handoffs: list[dict[str, Any]] = []
    verified_articles: list[dict[str, Any]] = []

    for item, result in zip(items, raw_results):
        rel_path = item["article_path"]
        validate_against_schema(result, CONTENT_MUTATION_RESULT_SCHEMA, f"content_result[{rel_path}]")
        if result["article_path"] != rel_path:
            raise SchemaValidationError(
                f"Subagent returned mismatched article_path {result['article_path']!r}; expected {rel_path!r}."
            )
        if result["action"] != action:
            raise SchemaValidationError(
                f"Subagent returned mismatched action {result['action']!r}; expected {action!r}."
            )

        abs_path = repo_root / rel_path
        if not abs_path.is_file():
            raise FileNotFoundError(f"Expected article was not written to disk: {abs_path}")
        after_text = abs_path.read_text(encoding="utf-8")

        gate = verify_article_mutation(
            before_text=baselines[rel_path]["before_text"],
            after_text=after_text,
            action=action,
            enforce_link_retention=(action in {"Simplified", "Updated"}),
        )

        handoff: dict[str, Any] = {
            "action": action,
            "article_path": rel_path,
            "title": result["title"],
            "date": gate["date"],
            "changelog_summary": result["changelog_summary"],
        }
        if gate["last_updated"]:
            handoff["last_updated"] = gate["last_updated"]
        elif result.get("last_updated"):
            handoff["last_updated"] = result["last_updated"]

        recip_list = result.get("reciprocal_articles_touched") or []
        if recip_list:
            handoff["reciprocal_articles_touched"] = recip_list

        validate_against_schema(handoff, INDEX_HANDOFF_SCHEMA, f"handoff[{rel_path}]")
        handoffs.append(handoff)
        verified_articles.append(
            {
                "article_path": rel_path,
                "title": result["title"],
                "retained_links_count": gate["retained_links_count"],
                "reciprocal_articles_touched": recip_list,
            }
        )

    log_fn(f"Passed deterministic pre-handoff invariant & link-retention gate for {len(handoffs)} article(s).")

    # ------------------------------------------------------------------
    # Stage 4: Single-Writer Index Reconciliation & Optional Review Chain
    # ------------------------------------------------------------------
    phase_fn("Stage 4: Single-Writer Index Reconciliation & Optional Review Chain")

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
        cmd = build_python_cmd(str(RECONCILER_SCRIPT), "--handoff", json.dumps(handoffs))
        proc = subprocess.run(
            cmd,
            cwd=str(repo_root),
            env=get_uv_env(),
            capture_output=True,
            text=True,
            check=True,
        )

    if proc.stdout.strip():
        log_fn(proc.stdout.strip())
    if proc.stderr.strip():
        log_fn(f"reconcile_indexes stderr: {proc.stderr.strip()}")

    review_results: Any = None
    if chain_review:
        log_fn(f"Chaining into run_review_workflow.py for {len(items)} article(s)...")
        review_mod = runpy.run_path(str(REVIEW_WORKFLOW_SCRIPT), init_globals=dict(env))
        review_env = dict(env)
        review_args = {
            k: v
            for k, v in wf_args.items()
            if k in {"dry_run", "reviewer_type", "reviewer_model", "remediator_model"}
        }
        review_args["article_paths"] = [item["article_path"] for item in items]
        review_env["args"] = review_args
        review_results = await review_mod["run_pipeline"](review_env)

    summary = {
        "mode": mode,
        "action": action,
        "processed_count": len(verified_articles),
        "articles": verified_articles,
        "handoffs": handoffs,
        "review_results": review_results,
    }
    print(json.dumps(summary, indent=2))
    return summary


def _run_self_test() -> None:
    """Exercise create, update, batch simplify, and link-drop rejection with mock agents."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        (tmp_root / "articles" / "devops").mkdir(parents=True, exist_ok=True)
        (tmp_root / "articles" / "tools").mkdir(parents=True, exist_ok=True)

        sibling_path = tmp_root / "articles" / "devops" / "sibling-guide.md"
        sibling_path.write_text(
            "# Sibling Guide\n\n"
            "**Date:** November 10, 2026\n\n"
            "## Related Articles\n\n"
            "- [Other](other.md) — context.\n\n"
            "## Changelog\n\n"
            "- **Nov 10, 2026:** Initial publication.\n",
            encoding="utf-8",
        )

        # 1. Test mode="create"
        new_rel = "articles/devops/hybrid-demo.md"

        def _make_mock_env(wf_args: dict[str, Any], drop_link: bool = False) -> tuple[dict[str, Any], list[str]]:
            phases_seen: list[str] = []

            async def _mock_agent(prompt: str, schema: dict[str, Any] | None = None, role: str = "", **_kw: Any) -> dict[str, Any]:
                assert schema == CONTENT_MUTATION_RESULT_SCHEMA
                mode = wf_args["mode"]
                m_path = re.search(r"Target article:\s*`([^`]+)`", prompt)
                assert m_path, f"Missing target path in prompt: {prompt}"
                target_rel = m_path.group(1)
                abs_target = tmp_root / target_rel

                if mode == "create":
                    abs_target.write_text(
                        "# Hybrid Control Plane Demo\n\n"
                        "**Date:** November 20, 2026\n\n"
                        "> **Scope & Licensing Note:** This article strictly covers pure open-source systems. "
                        "Premium, proprietary/vendor-locked, and community-edition (open-core) systems are currently not included.\n\n"
                        "## Summary\n\nDemo with [Sibling Guide](sibling-guide.md) and [Spec](https://example.org/spec).\n\n"
                        "## Related Articles\n\n"
                        "- [Sibling Guide](sibling-guide.md) — baseline context.\n\n"
                        "## References\n\n"
                        "- [Spec](https://example.org/spec)\n\n"
                        "## Changelog\n\n"
                        "- **Nov 20, 2026:** Initial publication.\n",
                        encoding="utf-8",
                    )
                    return {
                        "action": "Added",
                        "article_path": target_rel,
                        "title": "Hybrid Control Plane Demo",
                        "date": "November 20, 2026",
                        "changelog_summary": "Created hybrid control plane demo article",
                        "reciprocal_articles_touched": ["articles/devops/sibling-guide.md"],
                    }

                if mode == "update":
                    existing = abs_target.read_text(encoding="utf-8")
                    updated = existing.replace(
                        "**Date:** November 20, 2026\n",
                        "**Date:** November 20, 2026\n**Last Updated:** November 20, 2026\n",
                    ).replace(
                        "## Changelog\n\n",
                        "## Changelog\n\n- **Nov 20, 2026:** Expanded architecture section.\n",
                    )
                    abs_target.write_text(updated, encoding="utf-8")
                    return {
                        "action": "Updated",
                        "article_path": target_rel,
                        "title": "Hybrid Control Plane Demo",
                        "date": "November 20, 2026",
                        "last_updated": "November 20, 2026",
                        "changelog_summary": "Expanded architecture section",
                    }

                # mode == "simplify"
                existing = abs_target.read_text(encoding="utf-8")
                updated = existing.replace(
                    "**Date:** November 10, 2026\n",
                    "**Date:** November 10, 2026\n**Last Updated:** November 20, 2026\n",
                )
                if "**Last Updated:**" not in updated:
                    updated = updated.replace(
                        "**Date:** November 20, 2026\n",
                        "**Date:** November 20, 2026\n**Last Updated:** November 20, 2026\n",
                    )
                updated = updated.replace(
                    "## Changelog\n\n",
                    "## Changelog\n\n- **Nov 20, 2026:** Simplified formatting.\n",
                )
                if drop_link:
                    updated = updated.replace("[Spec](https://example.org/spec)", "Spec")
                abs_target.write_text(updated, encoding="utf-8")
                return {
                    "action": "Simplified",
                    "article_path": target_rel,
                    "title": abs_target.stem.replace("-", " ").title(),
                    "date": "November 20, 2026" if "hybrid-demo" in target_rel else "November 10, 2026",
                    "last_updated": "November 20, 2026",
                    "changelog_summary": "Simplified formatting and structure",
                }

            async def _mock_parallel(items_list: list[Any], fn: Callable[[Any], Any]) -> list[Any]:
                return await asyncio.gather(*(fn(item) for item in items_list))

            env: dict[str, Any] = {
                "WORKSPACES": (str(tmp_root),),
                "args": wf_args,
                "log": lambda _msg: None,
                "phase": phases_seen.append,
                "agent": _mock_agent,
                "parallel": _mock_parallel,
            }
            return env, phases_seen

        # Run create
        create_env, create_phases = _make_mock_env({"mode": "create", "article_path": new_rel, "dry_run": True})
        res_create = asyncio.run(run_pipeline(create_env))
        assert len(create_phases) == 4
        assert res_create["processed_count"] == 1
        assert res_create["handoffs"][0]["reciprocal_articles_touched"] == ["articles/devops/sibling-guide.md"]

        # Run update
        update_env, _ = _make_mock_env({"mode": "update", "article_path": new_rel, "dry_run": True})
        res_update = asyncio.run(run_pipeline(update_env))
        assert res_update["action"] == "Updated"
        assert res_update["articles"][0]["retained_links_count"] == 2

        # Run batch simplify across 2 files
        batch_env, _ = _make_mock_env(
            {
                "mode": "simplify",
                "article_paths": [new_rel, "articles/devops/sibling-guide.md"],
                "dry_run": True,
            }
        )
        res_batch = asyncio.run(run_pipeline(batch_env))
        assert res_batch["processed_count"] == 2

        # Negative test: dropped link during simplify must fail Stage 3 gate
        drop_env, _ = _make_mock_env(
            {"mode": "simplify", "article_path": new_rel, "dry_run": True},
            drop_link=True,
        )
        try:
            asyncio.run(run_pipeline(drop_env))
            raise AssertionError("Expected SchemaValidationError when link was dropped during simplify")
        except SchemaValidationError:
            pass

        print(
            "✅ run_content_workflow.py self-test passed "
            "(create, update, batch parallel simplify, link-drop rejection & dry-run reconciler verified)."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hybrid content workflow runner and offline self-test.")
    parser.add_argument("--self-test", action="store_true", help="Run offline mock content pipeline self-test.")
    cli_args = parser.parse_args()
    if cli_args.self_test:
        _run_self_test()
    else:
        parser.print_help()
