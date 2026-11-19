---
name: Commit and Push with JJ
description: Verify repository health (verify_links.sh Checks 1-8), commit working copy changes to a target bookmark (default main), and push to remote using Jujutsu (jj).
---

# Commit and Push (JJ)

This skill executes a **two-phase guarded publication workflow** using Jujutsu (`jj`) to prevent pushing broken links, orphan files, badge drift, or invalid review scorecards.

## Usage

When you want to save your progress and sync with the remote repository:

1.  **Step 1 — Verify Repository Health & Stage Bookmark (Local / Sandboxed)**:
    Run the atomic pre-push staging script. It enforces `bash verify_links.sh` (Checks 1–8) **before** describing `@` or advancing the target bookmark (`main` by default; pass an optional second argument to override):
    ```bash
    bash .agent/skills/commit_and_push/scripts/prepare_commit.sh "YOUR_COMMIT_MESSAGE" main
    ```
    * **Hard Gate Rule:** If `prepare_commit.sh` exits non-zero, **abort immediately**. Do **not** run `jj describe`, `jj bookmark set`, or `jj git push` manually to bypass the failure.
    * **Self-Healing Routing:** If `verify_links.sh` reports index, badge (`[NEW]`/`[UPDATED]`), count, or broken-link errors, run the [`organize_readme`](../organize_readme/SKILL.md) skill (or fix the reported check directly), then re-run Step 1 until it exits `0`.

2.  **Step 2 — Push Staged Bookmark to Remote (Network Step)**:
    **Only after Step 1 exits `0`**, push the staged bookmark to the git remote:
    ```bash
    jj git push --bookmark main
    ```

## Notes
- This workflow defaults to the `main` bookmark; pass a different bookmark name as the second argument to `prepare_commit.sh` and to `--bookmark` when targeting another branch.
- Keeping `prepare_commit.sh` (local verification + metadata staging) separate from `jj git push` isolates network access strictly to Step 2.
- If `jj git push` causes a conflict, run `jj git fetch` and rebase first, then re-run Step 1 before pushing.
