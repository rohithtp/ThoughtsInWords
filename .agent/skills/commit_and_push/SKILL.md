---
name: Commit and Push with JJ
description: Commit all current changes to the main branch and push to remote using Jujutsu (jj).
---

# Commit and Push (JJ)

This skill commits all working copy changes to the `main` bookmarks and pushes them to the git remote.

## Usage

When you want to save your progress and sync with the remote repository:

1.  **Describe the Change**:
    Set a description for the current working copy changes. Replace "YOUR_COMMIT_MESSAGE" with a summary of your changes.
    ```bash
    jj describe -m "YOUR_COMMIT_MESSAGE"
    ```

2.  **Update Main Bookmark**:
    Move the `main` bookmark to the current revision (`@`).
    ```bash
    jj bookmark set main -r @
    ```

3.  **Push to Remote**:
    Push the changes to the git remote.
    ```bash
    jj git push
    ```

## Notes
- This workflow assumes you want to update the `main` branch.
- If `jj git push` causes a conflict, you may need to `jj git fetch` and rebase first.
