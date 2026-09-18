# Phase 3 — Agentic Learning UI

**Checkpoint:** `99950b0` · **Depends on:** `PHASE1_99950B0.patch` + `PHASE2_99950B0.patch`
**Deliverable:** `PHASE3_99950B0.patch` (5 files, 401 insertions, 3 deletions)
**Status:** complete, all in-scope gates green, stopped for approval.

---

## 1. Scope

Phase 1 shipped the learning-agent seam (`LearningAgentActionType`,
`LearningAgentDecision`, `api.learningAgentNext`, and the
`/orchestrator/next` route) and deliberately deferred the page UI to Phase 3.
The authoritative contract is `frontend/scripts/check-learning-phase3-agentic.mjs`
(the full guide text was not available on disk this session, so every assertion
in that checker is treated as the Phase 3 acceptance list).

Honesty boundary preserved: the agent **recommends** — it never grades, never
completes a topic and never verifies a skill. Only a passed Final Assessment
creates a Verified Skill.

---

## 2. What changed

### `frontend/src/pages/LearningPage.tsx` (new `LearningAgentPanel`)
- Calls the real orchestrator via `api.learningAgentNext(studentId, skillId)`
  and renders `agentDecision.action_type`, `next_step`, `objective` and a
  type-specific open action. Action → tab map:
  `EXPLAIN→learn`, `PRACTICE/GIVE_HINT→practice`, `MINI_CHECK→mini_check`,
  `REVIEW_PREREQUISITE/ADVANCE/REQUEST_REASSESSMENT→learn`.
- **"Why this step?"** disclosure lists each `evidence` item (`kind: detail`)
  returned by the deterministic backend policy.
- **Practice / Mini Check** stay on the real lesson APIs: the panel routes into
  the existing `LessonView`, which submits through `lessonSubmitPractice` and
  `lessonMiniCheck`. The panel only recommends.
- **Static-check honesty.** When the latest practice attempt carries a
  `practice_task.static_check`, the panel shows the bilingual label
  `Static code check / فحص ثابت للكود` and the disclosure
  *"Python code is not executed here…"*. The Mini Check handoff is offered only
  when `latestAttempt?.practice_task?.static_check?.status === 'looks_structurally_sound'`
  (or the review is `ready`), matching the backend policy. The structural check
  never changes the practice score and never verifies a skill.
- **Persistent language control.** An English / `العربية المصرية` toggle writes
  `localStorage['sb_learning_language']` (`sb_learning_language`) and switches
  every panel string (title, why-this-step, static-check disclosure, retry,
  roadmap, disclaimer).
- **Error → retry.** A failed recommendation shows the error plus a
  `Retry recommendation` button that bumps `setRetryKey`, refetching.
- **`View full roadmap`** scrolls to the existing `#career-roadmap` section.
- Mounted in `SkillDetailPanel` for the selected gap; `onOpenTopic` reuses the
  page's `openLessonTopic` focus signal so the correct lesson/tab opens.

### `frontend/src/lib/types.ts`
- `PracticeStaticCheck` (`status: 'looks_structurally_sound' | 'needs_fix'`,
  `note`, `checks[]`) and `PracticeTask.static_check?`.

### `frontend/src/index.css`
- `.agent-*` styles (panel, language switch, evidence list, static-check block,
  actions, unverified disclaimer), reusing existing tokens.

### Tests
- `backend/tests/test_agentic_learning_phase3.py` (3): the decision exposes every
  UI field; the static-check payload carries the non-execution note and checks
  without changing the score; a reassessment decision still renders the full
  contract.
- `backend/tests/test_runtime_learning_phase3_agentic_frontend.py` (1): runs
  `check-learning-phase3-agentic.mjs` as part of the suite (it previously had no
  runtime test binding it).

---

## 3. Contract coverage (`check-learning-phase3-agentic.mjs`)

| Assertion | Status |
|---|---|
| seven `LearningAgentActionType` members in `types.ts` | PASS (Phase 1 seam) |
| `api.learningAgentNext` present | PASS (Phase 1 seam) |
| `agentDecision.action_type` rendered | PASS |
| `Why this step?` evidence disclosure | PASS |
| `lessonSubmitPractice` + `lessonMiniCheck` integration | PASS |
| `Python code is not executed here` disclosure | PASS |
| `Static code check / فحص ثابت للكود` label | PASS |
| `static_check?.status === 'looks_structurally_sound'` gating | PASS |
| `sb_learning_language` + `العربية المصرية` persistent control | PASS |
| `Retry recommendation` + `setRetryKey` | PASS |
| `View full roadmap` | PASS |

---

## 4. Gates

**Backend** (`backend/`, Python 3.12 `.venv`):
- Full suite: **1592 passed, 5 skipped, 0 failed** in 494s
  (Phase 2 baseline: 1588). +4 tests.
- Focused: `test_agentic_learning_phase3.py`,
  `test_learning_orchestrator.py`, `test_learning_path_currency.py`,
  `test_learning_practice.py`,
  `test_runtime_learning_phase3_agentic_frontend.py` → 33 passed.

**Frontend** (`frontend/`):

| Gate | Result |
|---|---|
| `npx tsc --noEmit` | PASS (exit 0) |
| `npm run build` | PASS |
| `check-learning-phase3-agentic.mjs` | **PASS** (was the deferred red gate) |
| `check-learning-phase1.mjs` | PASS |
| `check-learning-phase2-practice.mjs` | PASS |
| `check-learning-phase3-remediation.mjs` | PASS |
| `check-learning-phase4-resources.mjs` | PASS |
| `check-learning-polish.mjs` | PASS |
| `check-roles-discovery-phase2.mjs` | PASS |
| `check-data-truth-phase2.mjs` | PASS |
| `check-mentor-live-phase4b1.mjs` | PASS |
| `check-tutor-profiles.mjs` | PASS |
| `check-learning-tabs.mjs` | FAIL — **pre-existing at `99950b0`**, not referenced by any test; see §5 |

Patch integrity:

```
$ git apply --check PHASE3_99950B0.patch   # on top of Phase 1 + Phase 2
APPLY_CHECK_OK
```

---

## 5. Notes / out of scope

- `check-learning-tabs.mjs` expects a separate "My Skills / Continue /
  Completed tabs sourced from the student-profile API" implementation
  (`api.student`, `profileSkills`, `currentTabCopy`, `profileSource=…`). None of
  those strings exist at `99950b0` (verified with `git show 99950b0:…`), so the
  checker already failed before any of these phases, no test binds it, and it is
  **not part of the agentic contract**. Flagged, not changed.
- `jobs.py::_student_seniority` still infers seniority partly from self-reported
  levels (documented follow-up from Phase 2; the value is never rendered).

---

## 6. Apply instructions

From a normal (non-sandboxed) terminal:

```bash
cd /Users/aboodmr/Desktop/skillbridge-team-latest
git apply --index PHASE1_99950B0.patch   # if not already applied
git apply --index PHASE2_99950B0.patch   # if not already applied
git apply --index PHASE3_99950B0.patch
```

## 7. Deliverables

- `PHASE3_99950B0.patch` — incremental on top of Phase 1 + Phase 2 (5 files).
- `PHASE3_99950B0_REPORT.md` — this report.
- New source: `backend/tests/test_agentic_learning_phase3.py`,
  `backend/tests/test_runtime_learning_phase3_agentic_frontend.py`.
