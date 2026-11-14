#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import glob
import os
import re
import sys

errors = []

def strip_code(text: str) -> str:
    # Remove fenced code blocks and inline code spans so example snippets are ignored
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
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
    if f != "articles/README.md"
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

# Also verify relative .md links in root README.md
if os.path.isfile("README.md"):
    with open("README.md", encoding="utf-8") as fh:
        root_links = extract_md_links(fh.read())
    for link in root_links:
        full_path = os.path.normpath(link)
        if not os.path.isfile(full_path):
            errors.append(f"[Check 1b] Broken link in README.md: {link} -> {full_path}")

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
