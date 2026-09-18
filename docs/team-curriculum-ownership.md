# Team-base onboarding + curriculum ownership

Companion to `TEAM_STATUS.md`. This file defines how the 45-topic CS curriculum is split
between **three** developers with NON-OVERLAPPING file ownership so they can work in
parallel without touching the same shared backend files.

## Branch / integration workflow (read carefully)

- `team-base` is the shared integration branch. **Never commit directly to it.**
- Each developer works on their OWN feature branch, cut FROM `team-base`, and opens a
  pull request when done.
- Backend is the common integration surface: the platform merges learning, practice,
  practice-remediation and the career path. Backend files list below are NOT owned by
  any single curriculum developer — they already exist and are shared. Curriculum
  developers add CONTENT ONLY in the files/keyed slots that belong to their slice.

## Identity inside curriculum content

Each slice uses a distinct key namespace so merges never collide:

| Dev | Slice owner key | Owned curriculum input files (branches) |
|-----|----------------|------------------------------------------|
| Dev A | `cs_sql` + `cs_git` | owner A — see below |
| Dev B | `cs_docker` + `ml_*` | owner B — see below |
| Dev C | shared app/UX | cross-cutting — see below |

## Dev A — SQL Foundations (10) + Git & Collaboration (11)

- Owned lesson files: `backend/data_sources/lessons/cs_sql_foundations*.yml|json|md`
  (SQL Foundations and advanced SQL topics) and `cs_git_collaboration*`.
- Owned "topic" seed blocks: keys starting with `cs_sql_` and `cs_git_` in the curated
  knowledge base / topic registry.
- Owned tests: `backend/tests/test_curated_sql_foundations*`, `backend/tests/test_trusted_cs_knowledge_base*`
  (SQL/Git slices only). Update ONLY files matching `*sql*sql*`/`*git*` — never whole-suite.

## Dev B — Docker & Container Orchestration (11) + Machine Learning (11)

- Owned lesson files: `cs_docker_*` and `ml_*` (ML theory, ML practice, model eval).
- Owned topic seed blocks: keys `cs_docker_*`, `ml_*`.
- Owned tests: `backend/tests/test_curated_python_reliability.py` is NOT yours (shared);
  add NEW `test_curated_docker_*.py`, `test_curated_ml_*.py`.

## Dev C — Core app improvements, Learning stability, voice & product UX

- Owns frontend/UX (`LearningPage`, `Index.css`, voice/STT hooks, copilot) and the
  shared backend tutor/genai plumbing. BUG-FIX ONLY on shared backend; no topic content.
- Owned tests: existing `test_learning*.py`, `test_runtime_*frontend*.py`, voice/STT tests.

## Curriculum file layout (45 topics total)

The canonical 45-topic list (from the CS curriculum goal) lives in:
`docs/curriculum/45-topic-CS-curriculum.md` (see the goal summary in TEAM_STATUS.md).

## Rules

- One commit per topic-group; one PR per slice owner.
- Never `git rebase --onto` onto comments; use feature branches cut from the latest
  `team-base`.
- Do not generate the remaining lessons yet — the plan is approved for INTAKE only.
