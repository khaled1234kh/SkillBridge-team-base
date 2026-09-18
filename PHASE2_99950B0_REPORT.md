# Phase 2 — Data Truth, Match Consistency and Trust Language

**Checkpoint:** `99950b0` · **Depends on:** `PHASE1_99950B0.patch` (apply Phase 1 first)
**Deliverable:** `PHASE2_99950B0.patch` (14 files, 704 insertions, 45 deletions)
**Status:** complete, all gates green, stopped for approval.

---

## 1. Goal and acceptance

Every score and claim must be explainable and internally consistent. The guide's
acceptance criteria and how they are met:

| Acceptance criterion | Status | Evidence |
|---|---|---|
| One metric has one name, formula and value across pages | ✅ | `backend/app/metrics.py` registry; frontend reads backend values (no recompute) |
| A visible gap prevents claims of complete requirement coverage | ✅ | `all_requirements_met` + gap-aware copy; Docker case fixed |
| No education/profile statement is treated as proven competence | ✅ | roadmap checkpoints made conditional; regression test |
| Stale diagnostic/path data is labelled and cannot silently override current completed diagnostic evidence | ✅ | `path_stale` guard + UI note; regression test |
| Trust-language tests pass in English and Arabic | ✅ | `test_data_truth_phase2.py` EN/AR assertions |

---

## 2. The Junior AI Engineer contradiction (task 4)

Observed before Phase 2: the same "Junior AI Engineer" target could show **~88%**
(Dashboard ring, backend `match_score` 87.5), **100%** (Skills & Roles target
subtitle), and **42%** (a job-feed posting) while **Docker** remained a gap
(Beginner vs required Intermediate).

Root cause: `frontend/src/pages/SkillsRolesPage.tsx` computed its own target
percentage from **raw required-skill name overlap**:

```ts
// removed in Phase 2
const targetPct = Math.round((matchedNames / required_skills.length) * 100)
```

Docker's *name* was present in the CV, so the page counted it as covered and
reached 100% even though the backend (which is level-aware and gives partial
credit) correctly showed 87.5. `LearningPage.tsx` had the same class of bug
(`strong / total` recompute). The 42% was a genuinely different metric — a
job-posting match — but was never named as such.

**Fix:** the target number now comes only from the backend canonical metric
`analysis.metrics.target_requirement_coverage`; the name-overlap helper is kept
only as a clearly labelled **Catalogue similarity** metric, and the job-feed
number is labelled **Job posting match**.

---

## 3. Canonical metric registry — `backend/app/metrics.py` (new)

One key, one label, one formula, one rounding rule (1 decimal):

| Key | Label | Formula | Evidence source |
|---|---|---|---|
| `target_requirement_coverage` | Target requirement coverage | `sum(credit)/count(required) * 100` | best evidence per skill (verified > self-reported); partial credit below level |
| `career_readiness` | Career readiness (requirements met) | `count(met at/above level)/count(required) * 100` | same evidence, all-or-nothing per requirement |
| `verified_evidence_coverage` | Verified evidence coverage | `count(verified)/count(required) * 100` | only `verified_skills` (passed Final Assessment) |
| `catalogue_similarity` | Catalogue similarity | `count(names present)/count(required) * 100` | name presence only — never a competence/verification claim |

Exposed through:

- `matching.analyze_student()` now returns `metrics`, `metric_definitions`,
  `all_requirements_met`, `missing_requirements` (back-compatible; `match_score`
  and `gap_count` unchanged).
- `GET /api/metrics/definitions` returns the registry for tooltips/explainers.
- `match_explain.py` breakdowns carry `metric_key` / `metric_label`; the target
  breakdown also carries `complete`.

The frontend mirrors the keys in `frontend/src/lib/types.ts`
(`CanonicalMetricKey`, `MetricDefinition`, `Analysis.metrics`,
`all_requirements_met`, `missing_requirements`).

---

## 4. Frontend changes (no recomputation)

- **`SkillsRolesPage.tsx`** — target coverage read from
  `analysis.metrics.target_requirement_coverage`; subtitle names *Target
  requirement coverage* and states the number of open requirements, so a gap can
  never read as "complete". The name-overlap fallback is labelled *Catalogue
  similarity* everywhere (cards, drawer, modal, reference roles) and documented as
  "name overlap only … not a verification claim". `displayMatchOf` records which
  canonical metric it returned.
- **`LearningPage.tsx`** — hero uses the backend coverage metric, relabelled
  *Current requirement coverage*. A stale path now shows a labelled banner and the
  Final Assessment coverage section explains stale topics are **not counted**.
- **`DashboardPage.tsx`** — eyebrow and ring labelled *Target requirement
  coverage* / *Requirement coverage* with an explainer built from the backend
  `metric_definitions`; completion copy gated on `all_requirements_met`.
- **`widgets.tsx`** — `ScoreRing` takes a `label`/`explainer`; default is
  *Requirement coverage*, never a bare "Match".
- **`index.css`** — `.pp-stale-note` / `.pp-stale-inline` styling.

---

## 5. Stale data cannot override current evidence

`api_final_assessment_status` (`backend/app/main.py`) previously keyed off
`get_latest_diagnostic` and could let a superseded path satisfy readiness. Now it:

- uses `models.get_latest_completed_diagnostic`;
- computes `path_stale = path.diagnostic_id != latest_completed.id`;
- passes **empty** path items/progress/skipped to
  `coverage.final_assessment_ready` when stale, so only current completed
  diagnostic evidence counts;
- returns `path_stale` and `latest_diagnostic_id`.

The public path payload already exposes `stale` / `latest_diagnostic_id`
(Phase 1); the UI now renders it.

---

## 6. Trust language (tasks 6, 8, 9)

- `career_roadmap.py`: phase-6 checkpoint changed from the past-tense
  "You have passed the role's skill assessments…" to a conditional
  "Once you pass the role's Final Assessments… Until then, any level here is
  self-reported." Summary no longer promises "from zero to a job-ready". This
  removes a case where a CV-only profile could read a checkpoint it never earned.
- Verified-skills fallbacks (`genai._verified_skills_fallback`) keep the
  official-vs-reported distinction in **English and Arabic** (locked by test).
- Education/CV/profile fields are never converted into a competence claim;
  regression test drives a profile with only university/education and asserts no
  proficiency is stated.

---

## 7. Tests and gates

**Backend** (`backend/`, Python 3.12 `.venv`):

- Full suite: **1588 passed, 5 skipped, 0 failed** in 482s
  (baseline Phase 1: 1575 passed). +13 tests.
- New: `tests/test_data_truth_phase2.py` (12) and
  `tests/test_runtime_data_truth_phase2_frontend.py` (1).
  Covers the registry, endpoint, analysis payload parity, gap-blocks-completion,
  catalogue-vs-coverage (Docker), verified-only coverage, stale readiness,
  conditional roadmap checkpoint, education non-claim, match-explain labels,
  and EN/AR trust language.

**Frontend** (`frontend/`):

| Gate | Result |
|---|---|
| `npx tsc --noEmit` | PASS (exit 0) |
| `npm run build` | PASS (2.60s) |
| `check-roles-discovery-phase2.mjs` | PASS |
| `check-mentor-live-phase4b1.mjs` | PASS |
| `check-copilot-voice-unit.mjs` | PASS (226/0) |
| `check-tutor-profiles.mjs` | PASS (4 profiles) |
| `check-data-truth-phase2.mjs` (new) | PASS |
| `check-learning-phase3-agentic.mjs` | **FAIL (expected)** — agentic UI deferred to Phase 3 by explicit decision |

Patch integrity:

```
$ git apply --check PHASE2_99950B0.patch   # on top of the Phase 1 tree
APPLY_CHECK_OK
```

---

## 8. Apply instructions

From a normal (non-sandboxed) terminal:

```bash
cd /Users/aboodmr/Desktop/skillbridge-team-latest
# Phase 1 first (if not already applied):
git apply --index PHASE1_99950B0.patch
# then Phase 2:
git apply --index PHASE2_99950B0.patch
```

The sandbox here cannot modify existing files on the Desktop path, so the patch
and this report were delivered as **new files** only. No commit was made.

---

## 9. Deliverables

- `PHASE2_99950B0.patch` — incremental on top of Phase 1 (14 files).
- `PHASE2_99950B0_REPORT.md` — this report.
- New source: `backend/app/metrics.py`, `backend/tests/test_data_truth_phase2.py`,
  `backend/tests/test_runtime_data_truth_phase2_frontend.py`,
  `frontend/scripts/check-data-truth-phase2.mjs`.

## 10. Deferred (not Phase 2)

- `check-learning-phase3-agentic.mjs` remains red until the Phase 3 agentic
  learning page is implemented (action rendering, "Why this step?", static-check
  labels, persistent EN/EG-AR language control, retry, full roadmap link).
- `jobs.py::_student_seniority` still infers seniority partly from self-reported
  levels; the number is never rendered, so it is a low-risk documented follow-up.
