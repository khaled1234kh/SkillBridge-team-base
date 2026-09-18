# Phase 1 Report — Restore Fresh-Install and Test Integrity

- Base checkpoint: `99950b0` ("Checkpoint: latest local Phase 4C.1 work")
- Date: 2026-09-18
- Scope: Phase 1 of `SKILLBRIDGE_COMPLETE_UPGRADE_OPENCODE_GUIDE.txt`
- Status: **code complete; STOPPED for human approval**
- Working copy used: `/private/tmp/skillbridge-team-latest` (byte-identical mirror of the checkout)

## 0. Delivery note (sandbox restriction)

The real project path (`/Users/aboodmr/Desktop/skillbridge-team-latest`) is
read-and-write restricted in this session's shell sandbox: existing files cannot
be opened for read, truncated, renamed onto, or deleted; only brand-new files
can be created. The dedicated `read`/`write` file tools are also denied for
existing paths there.

Therefore the Phase 1 changes are delivered as a reviewable unified patch that
must be applied from a normal (non-sandboxed) terminal:

```
cd /Users/aboodmr/Desktop/skillbridge-team-latest
git apply --index PHASE1_99950B0.patch
```

`PHASE1_99950B0.patch` (761 lines, 17 files) was generated with `git diff HEAD`
from the mirror and includes the `VoiceOrb.tsx` deletion. Nothing was committed.
After applying, run `git status` to confirm the 17 expected files.

## 1. Scope decision (user-approved)

Phase 1 task #4 ("Reconcile the `LearningAgentActionType` contract … and every
action required by `check-learning-phase3-agentic.mjs`") only requires the
action-type/API contract. The checker additionally asserts Phase-3
page-rendering strings (`agentDecision.action_type`, "Why this step?", static
check labels/handoff, language control, retry/roadmap) that do not exist in
`frontend/src/pages/LearningPage.tsx` at `99950b0`.

Per the guide, Phase 3 is "finish the incomplete agentic-learning work", so the
agentic UI was **deferred to Phase 3** with the user's explicit approval. Phase 1
ships the type + API seam; `check-learning-phase3-agentic.mjs` is expected to
fail at the next assertion ("agent action is not rendered") until Phase 3.

## 2. Changes (by guide task)

1. **SpeechRecognition dependency.** `backend/requirements.txt` now pins
   `SpeechRecognition==3.17.0`, plus `audioop-lts==0.2.2` and
   `standard-aifc==3.13.0` under `python_version >= "3.13"` (3.13 removed
   `audioop`/`aifc`; 3.17.0 imports them unguarded).
2. **Learning orchestrator route.** Registered
   `GET /api/students/{student_id}/learning/{skill_id}/orchestrator/next` before
   the SPA catch-all; auth is enforced with `_current_user` + `_own_diagnostic`,
   so 401/403/404 responses are JSON.
3. **Orchestrator ↔ learning state.** The route calls
   `learning_orchestrator.observe_and_decide`, which reads persisted
   diagnostic/path/lesson/practice state. The Verified Skill boundary is
   unchanged; `models.get_latest_completed_diagnostic` and path `stale` /
   `latest_diagnostic_id` were added to support currency checks.
4. **Action-type contract.** `frontend/src/lib/types.ts` adds
   `LearningAgentActionType` (all seven actions including `EXPLAIN`),
   `LearningAgentEvidence` and `LearningAgentDecision`; `frontend/src/lib/api.ts`
   adds `api.learningAgentNext`. Page UI deferred (see §1).
5. **Legacy orb removed.** `frontend/src/components/VoiceOrb.tsx` deleted after
   confirming zero imports; `MentorOrb.tsx` is the single canonical orb.
6. **Curated diagnostic/product contract.** Curated diagnostics come from
   `knowledge_base.curated_diagnostic_questions` with deliberate defaults
   (`options: []` for free-text, generated ids); non-curated skills still use
   `genai.generate_diagnostic`. Python's trusted blueprint is limited to the two
   authored topics so no invented topics leak into diagnostics/paths. Relative
   progress ledger:
   `skill_blueprint.py` adds the narrow Python blueprint; `path_builder.py`
   normalizes slug/label forms for prerequisite ordering.
7. **Providers disabled under pytest.** Autouse `_no_live_providers` fixture in
   `backend/tests/conftest.py` nulls `ANTHROPIC_KEY`/`OPENAI_KEY`/`NIM_KEY`
   (tests that exercise providers set their own key afterwards). A session-scoped
   `_isolated_file_db` fixture points `database.DB_PATH` at a seeded temp file,
   so a clean checkout (no `backend/skillbridge.db`) no longer double-seeds the
   in-memory test DB via the startup handler and never touches the developer's
   database.
8. **Deterministic, fast, offline seeding.** `genai.generate_learning_item` and
   `genai.generate_quiz` gained a `deterministic=` path that skips the provider
   and reuses the existing fallback/sanitization; `seed.py` uses it for
   pre-generated learning and assessment questions. Provider enrichment is now
   lazy (on skill open), not startup.
9. **Env consistency.** Confirmed unchanged: `app/dotenv_local.py` loads only
   `ELEVENLABS_*`, process env wins, no-op under pytest. No secret values are
   logged.
10. **Writable project-local npm cache.** `scripts/lib.mjs` injects
    `npm_config_cache=<repo>/.npm-cache` for every npm invocation (and
    `scripts/start.mjs` for the dev-server spawn); `start.ps1` sets the same env
    var. `.npm-cache/` is git-ignored. No sudo/chown guidance is required.
11. **Unknown `/api/*` returns JSON.** The SPA catch-all now returns
    `{"detail": "Not Found"}` with status 404 for `api` / `api/…` paths.

Additional correctness fix found while testing: personalized-path generation now
keys off the latest **completed** diagnostic
(`models.get_latest_completed_diagnostic`), so a newer unanswered diagnostic can
no longer hide the completed one the path was built from. Curated practice
resubmissions of an identical answer reuse the stored attempt; curated practice
provider failure returns a retryable 503 instead of a fallback grade.

## 3. Gate results

### Backend — full suite (`../.venv/bin/python -m pytest tests -q`)

| | Before (`99950b0`) | After |
|---|---|---|
| Failed | 61 | **0** |
| Passed | 1514 | **1575** |
| Skipped | 5 | 5 |
| Time | 448.94s | 451.82s |

### Fresh-checkout validation (independent of the working mirror)

A detached `git worktree` at `99950b0`, this patch applied, **no**
`backend/skillbridge.db`, and `frontend/node_modules` present (the result of
`npm install`), was run end to end:

```
../.venv/bin/python -m pytest tests -q
-> 1575 passed, 5 skipped, 0 failed in 463.76s
```

This reproduces Phase 1 acceptance "full backend suite passes from a clean
venv/checkout". Two node-based contract tests
(`test_runtime_webcam_integrity_frontend`, `test_tutor_profiles`) require
`frontend/node_modules`; a fresh checkout must run `npm install` (or the
documented `npm start`) first, exactly as before.

Previously-failing clusters now pass: `test_tutor_stt_fallback` (8),
`test_learning_orchestrator` (6), `test_trusted_cs_knowledge_base` (7),
`test_learning_path_currency` (5), `test_curated_python_reliability` (4),
`test_python_static_check` (3), `test_learning_quality_rescue` (1),
`test_scenarios_phase4_ux` (1), plus learning practice/remediation regressions.

### Frontend (from `frontend/`)

| Gate | Before | After |
|---|---|---|
| `npm run typecheck` | pass | **pass** |
| `check-copilot-voice-unit.mjs` | 226/0 | **226/0** |
| `check-mentor-live-phase4b1.mjs` | FAIL (VoiceOrb) | **OK** |
| `check-tutor-profiles.mjs` | pass | **OK** |
| `check-learning-phase3-agentic.mjs` | FAIL (no EXPLAIN) | **FAIL — deferred to Phase 3** ("agent action is not rendered") |
| `npm run build` | pass | **pass** (built in 2.48s) |

### Fresh-install acceptance

- Fresh, offline seed (`SKILLBRIDGE_DB` on a temp path, provider env unset):
  **`FRESH_SEED_SECONDS=17.85`** (bounded; no network, no provider calls).
- STT endpoint 401/400/403/503 behavior covered by the passing
  `test_tutor_stt_fallback.py` (8 tests) on the fresh in-memory DB.
- Unknown `/api/*` returns JSON 404 (covered by the orchestrator/SPA tests).

## 4. Files changed

`.gitignore`, `start.ps1`, `scripts/lib.mjs`, `scripts/start.mjs`,
`backend/requirements.txt`, `backend/app/{genai,lessons,main,models,path_builder,practice,seed,skill_blueprint}.py`,
`backend/tests/conftest.py`, `frontend/src/lib/{api,types}.ts`,
`frontend/src/components/VoiceOrb.tsx` (deleted).

## 5. Known limitation carried forward

`check-learning-phase3-agentic.mjs` remains red until Phase 3 implements the
agentic-learning page (decision/evidence rendering, honest static-check labels,
persistent language control, retry/roadmap UI).

## 6. Next step

Apply `PHASE1_99950B0.patch`, re-run the backend suite and frontend gates, then
**STOP for human approval** before Phase 2.
