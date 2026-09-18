# Merge Day Runbook — `team-base` → Eslam's `main`

**Owner:** Khaled (ops for team-base)  
**Branch:** `team-base` (our integration branch)  
**Target:** `https://github.com/eslamkan121-sketch/SkillBridge-Final` → `main`  
**Rule:** Eslam runs the merge; we push **nothing** to his repo. This runbook is for Eslam to execute.

---

## 0. Preconditions (must be green before Eslam starts)

| Gate | Required State | Evidence |
|------|----------------|----------|
| Backend tests | `1586 passed / 0 failed` | `python -m pytest backend/tests -q` |
| Frontend typecheck | `npx tsc --noEmit` clean | `cd frontend && npm run typecheck` |
| Frontend build | `npm run build` clean | `cd frontend && npm run build` |
| Contracts (acceptance) | `29/29` contracts pass | `SKILLBRIDGE_FRONTEND_URL=http://localhost:3000 SKILLBRIDGE_BACKEND_URL=http://localhost:8000 node scripts/learning-acceptance.spec.mjs` |
| Voice unit tests | `226/0` pass | `node scripts/check-copilot-voice-unit.mjs` |
| Mentor live check | `10/10` pass | `node scripts/check-mentor-live-phase4b1.mjs` |
| Manual verification log | Updated with today's findings | `docs/team-base/manual-verification-log.md` |
| Test baseline | Snapshotted | `docs/team-base/test-baseline.md` |

**Do not start merge if any gate is RED.**

---

## 1. Prepare Eslam's Machine

```bash
# On Eslam's machine — fresh clone of HIS repo (SkillBridge-Final)
git clone https://github.com/eslamkan121-sketch/SkillBridge-Final.git
cd SkillBridge-Final
git checkout main

# Add our backup as a remote (read-only for Eslam)
git remote add team-base https://github.com/khaled1234kh/SkillBridge-team-base.git
git fetch team-base

# Verify the branch exists
git log --oneline team-base/team-base -5
```

---

## 2. Pre-Merge Inspection (Eslam reviews)

```bash
# Show diff: what team-base brings that main doesn't
git diff main..team-base/team-base --stat

# Key files Eslam should spot-check (A-owned — his acceptance baseline):
# - docs/curriculum/45-topic-CS-curriculum.md
# - learning-acceptance.spec.mjs
# - frontend/src/pages/Learning/LearningPage.tsx
# - backend/app/path_builder.py
# - backend/app/diagnostics.py
# These must NOT be changed by team-base (our constraint).
```

**Eslam decision point:** If any A-owned file appears in the diff with changes → **STOP**, investigate before proceeding.

---

## 3. Merge Options (pick one — see MERGE_PLAN_FOR_ESLAM.md)

### Option A: PR Review (recommended)
```bash
# On Eslam's GitHub UI:
# 1. Create PR from team-base/team-base → main
# 2. Review diff, run CI if configured
# 3. Merge (squash or merge commit — Eslam's choice)
```

### Option B: Local Merge + Push
```bash
# On Eslam's machine:
git checkout main
git merge --no-ff team-base/team-base -m "Merge team-base: voice/STT + tutor + backend plumbing (see team-base runbook)"
git push origin main
```

### Option C: Cherry-pick Critical Fixes Only
```bash
# If Eslam wants only specific commits:
git checkout main
git cherry-pick <commit-hash>  # repeat for each needed commit
git push origin main
```

**Rule:** Eslam picks the method. We do NOT push.

---

## 4. Post-Merge Verification (Eslam runs on HIS main)

```bash
# After merge lands on main:
cd SkillBridge-Final  # his repo, now on updated main
git pull origin main

# Fresh environment
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt

# Backend tests
cd backend
..\.venv\Scripts\python.exe -m pytest tests -q
# Expect: 1586 passed / 0 failed (or Eslam's baseline)

# Frontend
cd ..\frontend
npm ci
npm run build
npm run typecheck

# Acceptance contracts (requires real keys + Docker)
SKILLBRIDGE_FRONTEND_URL=http://localhost:3000 \
SKILLBRIDGE_BACKEND_URL=http://localhost:8000 \
  node scripts/learning-acceptance.spec.mjs

# Voice unit gates
node scripts/check-copilot-voice-unit.mjs
node scripts/check-mentor-live-phase4b1.mjs
```

**All must pass on Eslam's main before declaring merge complete.**

---

## 5. Post-Merge Sync (team-base catches up)

```bash
# After Eslam confirms main is green:
# On our machine (SkillBridge-team-base repo):
cd SkillBridge-team-base
git checkout team-base
git pull origin team-base  # our backup remote

# Fast-forward to Eslam's new main (which now includes our merge)
git fetch https://github.com/eslamkan121-sketch/SkillBridge-Final.git main
git merge --ff-only FETCH_HEAD
# If fast-forward fails → manual rebase (shouldn't happen if Eslam used our commits)

git push origin team-base
```

---

## 6. Rollback Plan (if post-merge fails)

If any gate fails on Eslam's main after merge:

```bash
# On Eslam's machine:
git checkout main
git reset --hard HEAD~1  # or revert the merge commit
git push origin main --force-with-lease

# Notify team-base: merge reverted, investigate
# We DO NOT force-push to team-base/team-base — only reset our local and re-evaluate.
```

---

## 7. Contacts & Escalation

| Role | Contact |
|------|---------|
| Eslam (A — merge authority) | GitHub: eslamkan121-sketch |
| Khaled (B — team-base ops) | GitHub: khaled1234kh |
| Backup repo | https://github.com/khaled1234kh/SkillBridge-team-base |

---

## 8. Checklist (Eslam signs off)

- [ ] All preconditions green (Section 0)
- [ ] Diff reviewed — no A-owned file changes
- [ ] Merge method selected (A/B/C)
- [ ] Merge executed
- [ ] Post-merge gates pass on Eslam's main
- [ ] team-base fast-forwarded to new main
- [ ] `TEAM_STATUS.md` updated with merge commit hash
- [ ] Manual verification log archived

**Signed:** _________________ **Date:** _________________