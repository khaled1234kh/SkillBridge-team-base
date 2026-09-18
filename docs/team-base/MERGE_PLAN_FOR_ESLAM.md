# Merge / Integration Plan for Eslam

**Prepared by:** Khaled — branch `team-base` (local), report date 2026-09-18
**For:** Eslam — your repo `eslamkan121-sketch/SkillBridge-Final`
**Status:** AWAITING YOUR APPROVAL. **Nothing has been pushed to your repo, to `main`, or anywhere except Eslam's own empty repo `khaled1234kh/SkillBridge-team-base` (used ONLY as our live backup).** Your `main` is untouched and still at `b3a1db2` (verified read-only).

---

## The situation (must read first)

We (the team) prepared **SkillBridge-Unified** — a single working tree that owns **both** of our halves of the codebase without anyone stepping on a shared backend file:

- **A (Eslam):** learning superset — backend `diagnostics`, `path_builder`, learning orchestrator, curated 45-topic curriculum, frontend Learning page + acceptance tests.
- **B (Khaled):** the UI base — backend plumbing, tutor, voice/STT, Docker, and the app/UX shell.

The unified tree lives on our **`team-base`** branch. To keep Eslam's personal repo and `main` pristine, **we did not merge into `main` and we never rewrote history** — we prepared a clean branch and are handing **you** the final say on how (or whether) it enters your repo, since it's your repo and the acceptance spec + curated question bank are yours to approve.

Nothing here touches the curated question bank, the acceptance tests, or your `main`. Everything below is your choice.

---

## Which files are ours vs yours (so you can scan safely)

The unified tree is a **superset**: it is your `SkillBridge-Final` content plus Khaled's UI additions, merged by **file-level ownership** (no shared backend file was edited by both). Full ownership map: `docs/team-curriculum-ownership.md`.

| Area | Owner |
|------|-------|
| `backend/app/diagnostics.py`, `path_builder.py` (scorer, personalized path) | A (Eslam) |
| `backend/app/learning_orchestrator.py`, `path_builder` imports, curated 45-topic curriculum, Learning page + acceptance tests | A (Eslam) |
| Backend main/tutor plumbing, voice/STT, Docker, app/UX shell, `.env.example`, build config | B (Khaled) |

---

## Option A — You pull our `team-base` branch into your repo as a PR (RECOMMENDED)

Keeps your `main` historically linear and lets you review the full unified diff before anything merges)Skip:

```bash
# On YOUR machine, from a clone of https://github.com/eslamkan121-sketch/SkillBridge-Final
git fetch https://github.com/khaled1234kh/SkillBridge-team-base team-base:team-base-incoming
git checkout -b merge/team-base origin/main
git merge team-base-incoming --no-commit --no-ff
# review: git diff --cached, git status
# if you're happy:
git commit -m "Merge unified team-base (learning superset + UI base) for review"
# open the PR from merge/team-base -> main yourself, or push the branch and open via GitHub UI
```

**Risks/effort:** URL-fetch (you don't need to add Khaled as a GitHub collaborator). Effort: ~2 commands + your review. No force-push, no history rewrite.

---

## Option B — We push our `team-base` to your repo as a NEW branch (you review, then YOU decide the merge)

We do **not** merge; we only deliver. On our side:

```bash
git push origin team-base   # where origin = your SkillBridge-Final repo
```

Then you review `team-base` and choose the merge yourself (below). No branch conflicts, `main` untouched.

---

## Option C — We push `team-base` as a "reference" branch and you re-apply selected changes

We deliver the branch read-only as documentation-of-record, and you cherry-pick/apply only the pieces you want at your pace (e.g., only the UI-base shell; skip the learning superset if you already maintain it).

```bash
git fetch https://github.com/khaled1234kh/SkillBridge-team-base team-base:ref/team/team-base
git cherry-pick -n <commit-that-matters-to-you>   # review each, in your own commits
```

**Effort/risk:** low risk (reference only), highest manual effort; forces you to re-introduce each change deliberately.

---

## What each option preserves

| | A (PR) | B (push branch) | C (reference + re-apply) |
|---|---|---|---|
| Your `main` history linear & untouched | ✅ | ✅ | ✅ |
| Your curated question bank + acceptance spec untouched | ✅ | ✅ | ✅ |
| No force-push anywhere | ✅ | ✅ | ✅ |
| You keep full control of what merges | ✅ (you review) | ✅ (you merge) | ✅ (you apply) |
| Effort to get unified code into your repo | Low | Lowest | Highest |

---

## Recommendation

**Option A.** Review the unified diff in a PR while your `main` stays pristine. When you approve, tell us and we'll push `team-base` to the agreed remote (PR URL will point at the backup repo first). Our live backup is always: https://github.com/khaled1234kh/SkillBridge-team-base (branch `team-base`).
