#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import glob
import os
import re
import sys
from datetime import datetime

errors = []

def strip_fenced_code(text: str) -> str:
    # Remove fenced code blocks so example snippets are ignored while keeping inline `[NEW]` badges
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)

def strip_code(text: str) -> str:
    # Remove fenced code blocks and inline code spans so example snippets are ignored
    text = strip_fenced_code(text)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text

def extract_md_links(text: str):
    cleaned = strip_code(text)
    links = []
    for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", cleaned):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.endswith(".md"):
            links.append(target)
    return links

# Discover all articles on disk
all_articles = sorted(
    f for f in glob.glob("articles/**/*.md", recursive=True)
    if f not in {"articles/README.md", "articles/CHANGELOG.md"}
)

# Check 1: Every relative .md link in articles/README.md resolves to an existing file in articles/
with open("articles/README.md", encoding="utf-8") as fh:
    readme_text = fh.read()

readme_links = extract_md_links(readme_text)
resolved_readme_targets = set()
broken_readme = []

for link in readme_links:
    full_path = os.path.normpath(os.path.join("articles", link))
    if not os.path.isfile(full_path):
        broken_readme.append((link, full_path))
    else:
        resolved_readme_targets.add(full_path)

if broken_readme:
    for link, full_path in broken_readme:
        errors.append(f"[Check 1] Broken link in articles/README.md: {link} -> {full_path}")
else:
    print(f"✅ Check 1 passed: All {len(readme_links)} links in articles/README.md resolve to existing files.")

# Also verify relative .md links in root README.md and articles/CHANGELOG.md
if os.path.isfile("README.md"):
    with open("README.md", encoding="utf-8") as fh:
        root_links = extract_md_links(fh.read())
    for link in root_links:
        full_path = os.path.normpath(link)
        if not os.path.isfile(full_path):
            errors.append(f"[Check 1b] Broken link in README.md: {link} -> {full_path}")

if os.path.isfile("articles/CHANGELOG.md"):
    with open("articles/CHANGELOG.md", encoding="utf-8") as fh:
        changelog_links = extract_md_links(fh.read())
    for link in changelog_links:
        full_path = os.path.normpath(os.path.join("articles", link))
        if not os.path.isfile(full_path):
            errors.append(f"[Check 1c] Broken link in articles/CHANGELOG.md: {link} -> {full_path}")

# Check 2: Every .md file under articles/ (excluding articles/README.md) is referenced in articles/README.md
unlisted = sorted(set(all_articles) - resolved_readme_targets)
if unlisted:
    for path in unlisted:
        errors.append(f"[Check 2] Unlisted article missing from articles/README.md: {path}")
else:
    print(f"✅ Check 2 passed: All {len(all_articles)} articles on disk are indexed in articles/README.md (0 orphans).")

# Check 3: Every relative .md link inside every article resolves cleanly
broken_internal = []
internal_link_count = 0
linked_articles = 0

for article in all_articles:
    with open(article, encoding="utf-8") as fh:
        content = fh.read()
    links = extract_md_links(content)
    if links:
        linked_articles += 1
    article_dir = os.path.dirname(article)
    for link in links:
        internal_link_count += 1
        target_path = os.path.normpath(os.path.join(article_dir, link))
        if not os.path.isfile(target_path):
            broken_internal.append((article, link, target_path))

if broken_internal:
    for article, link, target_path in broken_internal:
        errors.append(f"[Check 3] Broken internal link in {article}: {link} -> {target_path}")
else:
    print(f"✅ Check 3 passed: All {internal_link_count} internal cross-links across {linked_articles} articles resolve cleanly.")

# Check 4: Zero empty directories under articles/ and 100% lowercase kebab-case.md filenames
empty_dirs = []
for root, dirs, files in os.walk("articles"):
    if not dirs and not files:
        empty_dirs.append(root)

kebab_re = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
non_kebab = []
for article in all_articles:
    basename = os.path.basename(article)
    if not kebab_re.match(basename):
        non_kebab.append(article)

if empty_dirs:
    for d in empty_dirs:
        errors.append(f"[Check 4] Empty directory under articles/: {d}")
if non_kebab:
    for path in non_kebab:
        errors.append(f"[Check 4] Filename is not lowercase kebab-case.md: {path}")
if not empty_dirs and not non_kebab:
    print(f"✅ Check 4 passed: 0 empty directories and 100% lowercase kebab-case.md compliance ({len(all_articles)} files).")

# Check 5: Hybrid Window [NEW] policy (7-day window from latest article date, min 3, max 5) & count parity
article_dates = {}
for article in all_articles:
    with open(article, encoding="utf-8") as fh:
        head = fh.read(1000)
    m = re.search(r"^\*\*Date:\*\*\s*([A-Za-z]+ \d{1,2}, \d{4})\s*$", head, flags=re.MULTILINE)
    if m:
        try:
            article_dates[article] = datetime.strptime(m.group(1).strip(), "%B %d, %Y").date()
        except ValueError:
            pass

cleaned_articles_readme = strip_fenced_code(readme_text)
articles_readme_new = {
    os.path.normpath(os.path.join("articles", match))
    for match in re.findall(
        r"^\s*-\s*\[[^\]]+\]\(([^)]+\.md)\)\s*\[NEW\]\s*$",
        cleaned_articles_readme,
        flags=re.MULTILINE,
    )
}

root_readme_text = ""
if os.path.isfile("README.md"):
    with open("README.md", encoding="utf-8") as fh:
        root_readme_text = fh.read()
cleaned_root_readme = strip_fenced_code(root_readme_text)
root_readme_new = {
    os.path.normpath(match)
    for match in re.findall(
        r"^\s*\*\s*\[[^\]]+\]\(([^)]+\.md)\).*\[NEW\]",
        cleaned_root_readme,
        flags=re.MULTILINE,
    )
}

check5_ok = True
if not article_dates:
    errors.append("[Check 5] No valid **Date:** headers found in articles/ to evaluate Hybrid Window.")
    check5_ok = False
else:
    latest_date = max(article_dates.values())
    within_7d = [f for f, dt in article_dates.items() if (latest_date - dt).days <= 7]
    expected_new_count = min(5, max(min(3, len(article_dates)), len(within_7d)))

    if articles_readme_new != root_readme_new:
        only_articles = sorted(articles_readme_new - root_readme_new)
        only_root = sorted(root_readme_new - articles_readme_new)
        if only_articles:
            errors.append(f"[Check 5] [NEW] entries in articles/README.md missing from README.md: {only_articles}")
        if only_root:
            errors.append(f"[Check 5] [NEW] entries in README.md missing from articles/README.md: {only_root}")
        check5_ok = False

    if len(articles_readme_new) != expected_new_count:
        errors.append(
            f"[Check 5] Expected {expected_new_count} [NEW] articles under Hybrid Window "
            f"(7d from {latest_date}: {len(within_7d)} within 7d, min 3, max 5), found {len(articles_readme_new)}."
        )
        check5_ok = False

    missing_dates = sorted(p for p in articles_readme_new if p not in article_dates)
    if missing_dates:
        errors.append(f"[Check 5] [NEW] articles missing valid **Date:** header: {missing_dates}")
        check5_ok = False
    elif articles_readme_new:
        selected_dates = [article_dates[p] for p in articles_readme_new]
        unselected_dates = [dt for p, dt in article_dates.items() if p not in articles_readme_new]
        if unselected_dates and min(selected_dates) < max(unselected_dates):
            errors.append(
                f"[Check 5] [NEW] selection skipped newer article(s): oldest selected is "
                f"{min(selected_dates)}, newest unselected is {max(unselected_dates)}."
            )
            check5_ok = False

cat_dir_match = re.search(r"## Category Directory \((\d+) Articles\)", readme_text)
if not cat_dir_match:
    errors.append("[Check 5] Missing '## Category Directory (<N> Articles)' header in articles/README.md.")
    check5_ok = False
elif int(cat_dir_match.group(1)) != len(all_articles):
    errors.append(
        f"[Check 5] Total count mismatch in articles/README.md Category Directory: "
        f"header says {cat_dir_match.group(1)}, disk has {len(all_articles)}."
    )
    check5_ok = False

root_count_match = re.search(r"Browse Full Article Index \((\d+) Articles\)", root_readme_text)
if not root_count_match:
    errors.append("[Check 5] Missing 'Browse Full Article Index (<N> Articles)' in README.md.")
    check5_ok = False
elif int(root_count_match.group(1)) != len(all_articles):
    errors.append(
        f"[Check 5] Total count mismatch in README.md: "
        f"header says {root_count_match.group(1)}, disk has {len(all_articles)}."
    )
    check5_ok = False

if check5_ok:
    print(
        f"✅ Check 5 passed: Hybrid Window [NEW] parity verified ({len(articles_readme_new)}/{expected_new_count} "
        f"within 7d of {latest_date}) and total count ({len(all_articles)}) synced across both READMEs."
    )

# Check 6: Article & Repo Revision Trail Parity (**Last Updated:**, ## Changelog, [UPDATED], articles/CHANGELOG.md)
check6_ok = True
if not os.path.isfile("articles/CHANGELOG.md"):
    errors.append("[Check 6] Missing repository-level activity log: articles/CHANGELOG.md.")
    check6_ok = False

updated_articles_meta = {}
has_changelog_section = set()

for article in all_articles:
    with open(article, encoding="utf-8") as fh:
        content = fh.read()
    head = content[:1000]
    lu_line = re.search(r"^\*\*Last Updated:\*\*(.*)$", head, flags=re.MULTILINE)
    if lu_line:
        lu_raw = lu_line.group(1).strip()
        try:
            lu_date = datetime.strptime(lu_raw, "%B %d, %Y").date()
        except ValueError:
            errors.append(f"[Check 6] Invalid **Last Updated:** format in {article}: {lu_raw!r} (expected 'Month Day, Year').")
            check6_ok = False
            continue

        updated_articles_meta[article] = lu_date
        if article not in article_dates:
            errors.append(f"[Check 6] {article} has **Last Updated:** but is missing a valid **Date:** header.")
            check6_ok = False
        elif lu_date < article_dates[article]:
            errors.append(
                f"[Check 6] {article} has **Last Updated:** ({lu_date}) earlier than **Date:** ({article_dates[article]})."
            )
            check6_ok = False

    cl_match = re.search(r"^## Changelog\s*$", content, flags=re.MULTILINE)
    if cl_match:
        cl_body = content[cl_match.end():]
        next_h2 = re.search(r"^##\s+", cl_body, flags=re.MULTILINE)
        if next_h2:
            cl_body = cl_body[:next_h2.start()]
        if re.search(r"^\s*[-*]\s+\*\*[^*]+:\*\*", cl_body, flags=re.MULTILINE):
            has_changelog_section.add(article)
        elif lu_line:
            errors.append(f"[Check 6] {article} has ## Changelog but no '- **Mon DD, YYYY:** ...' entry.")
            check6_ok = False
    elif lu_line:
        errors.append(f"[Check 6] {article} has **Last Updated:** but is missing a '## Changelog' section.")
        check6_ok = False

articles_readme_updated = {
    os.path.normpath(os.path.join("articles", match))
    for match in re.findall(
        r"^\s*-\s*\[[^\]]+\]\(([^)]+\.md)\)\s*\[UPDATED\]\s*$",
        cleaned_articles_readme,
        flags=re.MULTILINE,
    )
}
root_readme_updated = {
    os.path.normpath(match)
    for match in re.findall(
        r"^\s*\*\s*\[[^\]]+\]\(([^)]+\.md)\).*\[UPDATED\]",
        cleaned_root_readme,
        flags=re.MULTILINE,
    )
}

if articles_readme_updated != root_readme_updated:
    only_articles = sorted(articles_readme_updated - root_readme_updated)
    only_root = sorted(root_readme_updated - articles_readme_updated)
    if only_articles:
        errors.append(f"[Check 6] [UPDATED] entries in articles/README.md missing from README.md: {only_articles}")
    if only_root:
        errors.append(f"[Check 6] [UPDATED] entries in README.md missing from articles/README.md: {only_root}")
    check6_ok = False

if len(articles_readme_updated) > 5:
    errors.append(
        f"[Check 6] Expected at most 5 [UPDATED] articles in Recently Updated, found {len(articles_readme_updated)}."
    )
    check6_ok = False

both_badges = sorted((articles_readme_new & articles_readme_updated) | (root_readme_new & root_readme_updated))
if both_badges:
    errors.append(f"[Check 6] Article(s) cannot hold both [NEW] and [UPDATED] badges: {both_badges}")
    check6_ok = False

for article in sorted(articles_readme_updated):
    if article not in updated_articles_meta:
        errors.append(f"[Check 6] [UPDATED] article missing valid **Last Updated:** header: {article}")
        check6_ok = False
    if article not in has_changelog_section:
        errors.append(f"[Check 6] [UPDATED] article missing valid ## Changelog section: {article}")
        check6_ok = False

if check6_ok:
    print(
        f"✅ Check 6 passed: Revision trail verified ({len(updated_articles_meta)} updated article(s), "
        f"{len(articles_readme_updated)}/5 [UPDATED] badge(s) synced, articles/CHANGELOG.md present)."
    )

print("\n--- Summary ---")
print(f"Total articles: {len(all_articles)}")
print(f"Articles with internal links: {linked_articles} ({internal_link_count} total links)")

if errors:
    print("\n❌ Verification failed:")
    for err in errors:
        print(" ", err)
    sys.exit(1)

print("\n🎉 All checks passed!")
PY
