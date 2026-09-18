# TEAM ONBOARDING

**Branch:** `team-base` (our shared integration branch) · **Repo (read/write):**
`https://github.com/khaled1234kh/SkillBridge-team-base`
**Eslam's repo (READ-ONLY reference for us; ESALM MERGES):**
`https://github.com/eslamkan121-sketch/SkillBridge-Final`

Welcome to the SkillBridge unified build. Read this before touching anything.

---

## Who is who

| Dev | Repo / role | Owns (in `team-base`) |
|-----|-------------|------------------------|
| **A — Eslam** | Your repo `SkillBridge-Final` (`main` = your accepted build) | curated 45-topic question bank, acceptance spec (`learning-acceptance.spec.mjs`), scorer `diagnostics.py`, builder `path_builder.py`, Learning UI panel (`.pp-item`) |
| **B — Khaled** | Backup `SkillBridge-team-base` (this repo) | backend plumbing, tutor, voice/STT, Docker/UX shell, onboarding/tracking docs |

`team-base` is the **merge of both** — a superset. Your `main` is **never** touched
by us; Eslam approves the merge (see `docs/team-base/MERGE_PLAN_FOR_ESLAM.md`).

---

## What this repo IS vs Eslam's `main`

- `team-base` = complete source tree (A learning superset + B UI base) on our
  integration branch. Living backup, kept in our own repo.
- Eslam's `main` = his accepted baseline `b3a1db2`; we merge **into** it only
  when **he** runs the merge (branch → PR he reviews, or Option B/C in the plan).
- Rule: if a file's owner is **Eslam (A)**, we do not fix it — we **document**
  (see Test 2/3 in `docs/team-base/`).

---

## How to run

```bash
# backend (Docker)
docker compose up --build -d
curl -fsS http://localhost:8000/api/system/health
# tests
python -m pytest backend/tests -q            # 1586 passed / 3 skipped (full)
# frontend
cd frontend && npm ci && npm run build && npm run typecheck
# acceptance contracts (requires live instance + Brave for voice gate)
SKILLBRIDGE_FRONTEND_URL=http://localhost:3000 \
SKILLBRIDGE_BACKEND_URL=http://localhost:8000 \
  node scripts/learning-acceptance.spec.mjs   # Test 2/3 = known Eslam-side notes
```

---

## Open questions / handoffs

1. **Merge method** — Pick A/B/C in `docs/team-base/MERGE_PLAN_FOR_ESLAM.md`
   (we push nothing until **Eslam** picks).
2. **Learning Test 3** — documented, pre-existing, 1-vs-2 `.pp-item` mismatch;
   root cause + fix options in `docs/team-base/learning-test3-analysis.md`.
3. **Learning Test 2 (flaky panel timing)** — Eslam's `LearningPage.tsx` panel;
   documented, not fixed by us.
4. **Voice/STT + ElevenLabs 401 + Docker** — manual gates in
   `docs/team-base/manual-verification-log.md`; need Eslam's real browser/keys/daemon.

## Where the reports live

- Root: `TEAM_STATUS.md`, `TEAM_ONBOARDING.md` (this file)
- Team reports: `docs/team-base/`
- Ownership map: `docs/team-curriculum-ownership.md`
- Curriculum (45-topic CS): `docs/curriculum/45-topic-CS-curriculum.md`
