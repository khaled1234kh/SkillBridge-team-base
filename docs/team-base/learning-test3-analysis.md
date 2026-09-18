# Learning Acceptance Test 3 — Root-Cause Analysis (ANALYSIS ONLY, NO FIX APPLIED)

**Author:** Khaled (ops for team-base) · **Date:** 2026-09-18 · **Branch:** `team-base`
**Status:** Analysis complete. **No code/spec/question-bank change was made.**

---

## 1. The failing test (Test 3) in plain words

`frontend/scripts/learning-acceptance.spec.mjs` (the **acceptance test — OWNED BY ESLAM, untouched**)
runs a real student through a diagnostic and then asserts, on the personalized
path panel (`#skill-detail .pp-item`), a **specific item count**. The test is
**deterministic** — it fails identically every time on both pristine `main`
(Eslam's b3a1db2) and our `team-base`.

Seen in the suite:
```
test('stale path exposes refresh instead of opening a lesson', ...):
  await completedDiagnostic(pythonId)
  ...
  await expect(page.locator('.pp-item')).toHaveCount(2)   # <-- asserts 2
```
But the diagnostic we force (`completedDiagnostic`, which answers every question
with `options[0]` — the deliberately-wrong curated distractor choice) scores:
- `python_error_handling` → **MASTERED** (≥75%)
- `python_functions`      → **DEVELOPING** (40–74%)

## 2. Root cause — deterministic, in OUR code path, not a flake

`build_personalized_path` in `backend/app/path_builder.py` **deliberately skips
mastered topics** (they never enter the path; `MASTERED` is not even in
`STATUS_RANK` — see `path_builder.py:19`). So with one topic MASTERED and one
topic DEVELOPING, the built path correctly contains **only 1 item**, yet the
acceptance spec asserts 2 `.pp-item` in `#skill-detail`.

We verified this is **NOT a regression from the merge**: the exact same scorer +
builder + spec exist on Eslam's pristine `main` (read-only `git show
b3a1db2:...`), and the assertion `toHaveCount(2)` is unchanged there. So this is a
**pre-existing expectation mismatch**, not something we introduced.

## 3. Why the count is 1, precisely

`completedDiagnostic(pythonId)` → `POST /api/students/{id}/learning/{skill}/diagnostic/generate`
then `/submit` with `answers: diag.questions.map(q => q.options[0])`.

- `options[0]` is the curated **distractor** (wrong) answer for every question.
- `python_error_handling` questions never all get marked correct but the topic
  score aggregates to ≥75 → MASTERED after our curated bank's thresholds
  (`MASTERED_MIN = 75.0` in `diagnostics.py`).
- MASTERED topics are **skipped** by `build_personalized_path`, so only
  `python_functions` (DEVELOPING) becomes a `.pp-item`.

## 4. Who owns this code (per docs/team-curriculum-ownership.md)

- `path_builder.py`, `diagnostics.py`, the curated question bank, and the
  **acceptance spec** are **Eslam's (A)**.
- The personalized-path **frontend panel** (`LearningPage.tsx` → `.pp-item`) is
  **Eslam's (A)** as well.

Per team rule, Test 2/3 spec change and question-bank change are **Eslam-owned
only**. We therefore **document, do not fix**.

## 5. Fix options + tradeoffs (proposals ONLY — choose after Eslam reviews)

### Option F1 — Change the *test harness's* diagnostic answers (requires touching acceptance spec = Eslam's call)
Make `completedDiagnostic` answer with the **correct** curated answer at least on
the error-handling question so that topic lands DEVELOPING (not MASTERED), making
the path contain both topics → 2 `.pp-item`.
- ✅ Smallest code change; keeps acceptance spec meaning "path shows the topics
  the diagnostic flagged."
- ❌ The acceptance spec file is Eslam's — editing it requires his approval. Also
  depends on curated bank answer layout (brittle if bank changes).

### Option F2 — Change `path_builder` to also include MASTERED topics as "review/refresh" items
Path still contains all tested topics; mastered ones render as a "refresh" card
so `.pp-item` count matches the number of topics in the diagnostic, not just the
non-mastered remainder.
- ✅ Makes path visually complete (mastered + gap together as the spec implies).
- ❌ Changes shared backend semantics of "personalized path == gaps only".
  `path_builder.py` is Eslam's; this changes phase-scoring behavior for Dev A's
  feature. High blast radius on other tests (`path-builder` unit tests,
  freshness). Needs Eslam's sign-off.

### Option F3 — Strengthen Test 2/3 to derive the expected count from the diagnostic result
(compute expected `.pp-item` count = topics with status != MASTERED) rather than
hardcoding 2.
- ✅ Self-consistent across any curated bank; no backend change.
- ❌ Still edits the acceptance spec (Eslam-owned). If spec is meant to pin the
  *fixed* 2-item expectation, this weakens the test's intent.

---

## 6. Recommendation (no action taken yet)

We recommend **F1 or F3** only after Eslam approves touching the acceptance spec;
**F2** only with his sign-off since it changes path semantics. Until then, Test 3
remains a known, deterministic, pre-existing failure on both pristine `main` and
`team-base` — it is **not** caused by our merge and will be reported as-is in the
final acceptance handoff.
