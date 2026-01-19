# JJ Usage and Git Comparison

**Date:** 2026-01-19  
**Tags:** #jj #git #version-control #developer-tools

This document captures the `jj` (Jujutsu) commands used in a recent workflow to pull changes, and provides a broader comparison between `jj` and `git` commands for common tasks.

## Workflow: Pulling and Updating

In the recent session, we performed a "pull" operation. Unlike `git pull`, which is often a compound command (fetch + merge/rebase), `jj` encourages a more explicit flow.

### Commands Used

1.  **`jj status`**
    *   **Usage:** Checks the state of the repo and the current working copy.
    *   **Context:** Confirmed we were on an empty working copy with no pending changes.

2.  **`jj git fetch`**
    *   **Usage:** Fetches new commits from the remote repository (similar to `git fetch`).
    *   **Context:** Retrieved the latest commits from `origin`, updating the immutable remote pointers.

3.  **`jj log -r "main | main@origin"`**
    *   **Usage:** Shows the revision history graph. The `-r` flag specifies a "revset" to filter what is shown.
    *   **Context:** Used to visualize the local `main` vs the remote `main@origin` to understand divergence.

4.  **`jj new main`**
    *   **Usage:** Creates a new, empty working copy commit on top of the specified revision (in this case, `main`).
    *   **Context:** Effectively "checked out" the latest state of `main`. Since `jj` always keeps you on a working copy commit, `jj new` is how you move your workspace to a new parent.

---

## JJ vs Git: Common Command Primer

Jujutsu (`jj`) introduces a different mental model. The most significant shift is that the **working copy is also a commit** (implicitly created), and you rarely "modify" history in the way Git warns against; in `jj`, everything is mutable until pushed.

### 1. Status and History

| Action | Git Command | JJ Command | Notes |
| :--- | :--- | :--- | :--- |
| **Check Status** | `git status` | `jj status` (`jj st`) | `jj st` often gives a concise summary of the parent, working copy, and conflicts. |
| **View Log** | `git log --graph --oneline` | `jj log` | `jj log` is the default view and shows a topological graph. |

### 2. Creating and Committing

| Action | Git Command | JJ Command | Notes |
| :--- | :--- | :--- | :--- |
| **Start Work** | `git checkout -b feature` | `jj new main` | `jj` creates an anonymous branch (revision) by default. You don't need to name it immediately. |
| **Save Changes** | `git add . && git commit -m "msg"` | `jj describe -m "msg"` | In `jj`, the working copy *is* the commit. You just describe it to "finalize" it. |
| **Create New Commit** | (Implicit in next edit) | `jj new` | Once described, `jj new` starts a *fresh* working copy on top of the previous one. |

### 3. Branching and Bookmarks

`jj` calls named branches "bookmarks".

| Action | Git Command | JJ Command | Notes |
| :--- | :--- | :--- | :--- |
| **Create Branch** | `git branch name` | `jj bookmark set name -r @` | Assigns a name to the current revision (`@`). |
| **Switch Branch** | `git checkout name` | `jj edit name` | `jj edit` sets the working copy to point to that revision. |

### 4. Moving and Editing History

| Action | Git Command | JJ Command | Notes |
| :--- | :--- | :--- | :--- |
| **Amend Last Commit** | `git commit --amend` | `jj squash` (into parent) | `jj` treats the working copy as a child of the previous commit. Squashing merges them. |
| **Rebase** | `git rebase main` | `jj rebase -d main` | Rebase the current revision onto a destination (`-d`). |

### 5. Syncing with Remote

| Action | Git Command | JJ Command | Notes |
| :--- | :--- | :--- | :--- |
| **Fetch** | `git fetch` | `jj git fetch` | Identical function. |
| **Pull** | `git pull` | `jj git fetch` then `jj rebase` or `jj new` | `jj` prefers manual updating of your working copy over auto-merging. |
| **Push** | `git push` | `jj git push` | Pushes bookmarks to the remote. |
