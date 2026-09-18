# SkillBridge — PHASE 0 Baseline Report (checkpoint `99950b0`)

**Date:** 2026-09-17
**Checkpoint:** `99950b0` "Checkpoint: latest local Phase 4C.1 work"
**Parent commit:** `fbf9ad5` "Initial upload of SkillBridge project"
**Author of this report:** opencode (Phase 0 audit only — no behavior changes made)

---

## 1. Scope and method

Phase 0 only. Read `SKILLBRIDGE-OPENCODE-INSTRUCTIONS.txt`, the newest
`AGENTS.md` entry, `HANDOFF_FRIEND.md`, `HANDOFF.md`,
`docs/HANDOFF_2026-09-17.md`, `TEAM_HANDOFF_CURRENT_STATUS.md`, `README.md`,
`.env.example`, and inspected the actual code. Ran every baseline gate, launched
an isolated instance on an unused port against a **copy** of the private
database, and recorded results. **No product behavior was changed.**

> Note on the private database: `backend/skillbridge.db` was never opened for
> write. The isolated instance ran against `SKILLBRIDGE_DB=/tmp/sb_baseline_demo.db`
> (a byte-for-byte copy of `backend/skillbridge.db`, 770,048 bytes).

## 2. Git state

| Item | Value |
|---|---|
| Branch | `main` |
| HEAD | `99950b0` (matches the checkpoint target of the guide) |
| Working tree at start | clean (`nothing to commit, working tree clean`) |
| Files ignored by Git | confirmed via `git check-ignore -v` |

Ignored successfully (verified): `.env`, `env`, `*.db` (incl.
`backend/skillbridge.db`, `backend/skillbridge.seed-partial.db`),
`frontend/node_modules/`, `.venv/`, `frontend/dist/`,
`frontend/tsconfig.tsbuildinfo`, `__pycache__/`, `.pytest_cache/`.

## 3. Architecture summary (inspected, not inferred)

### Backend — `backend/app/`
FastAPI + Uvicorn, SQLite via stdlib `sqlite3`.
- `main.py` (3,546 lines): all routes + SPA static serving + auth guards.
- `database.py`: schema, ordered **13 migrations** (`0001`…`0013`) with an
  applied-migrations ledger; `SKILLBRIDGE_DB` env override; per-test in-memory
  DB support (`set_db_for_test`).
- `models.py` data layer; `matching.py`; `match_explain.py`; `integrity.py`;
  `genai.py` (NIM provider + deterministic fallback); `tts.py` (ElevenLabs,
  4 mentor voices via `load_root_env`); `auth.py`; `jobs.py` +
  provider federation; `learning_orchestrator.py` (**module present but NOT
  registered** — see §6); `lessons.py`, `knowledge_base.py`,
  `skill_blueprint.py`, `practice.py`, `scenarios.py`, `copilot.py`,
  `career_roadmap.py`, `recommendations.py`, `seed.py`, `resources.py`,
  `escoe.py`, `esco_import.py`, `role_mapping.py`, `role_intent.py`, and more.

Route inventory (main.py): **119 routes** — GET 59, POST 48, PUT 4, PATCH 1,
DELETE 7, plus the SPA catch-all `GET /{full_path:path}` at line 3534.
Auth: bearer-token sessions (`_current_user`, `_require_roles`,
`_own_student`), local + Google demo login, hashed session tokens.
Roles: Student / Company / University Admin.

Key registered surfaces (all reachable, 200s on the isolated instance):
- Auth: `/api/auth/*` (signup, login, logout, me, google, reset, verify).
- Students: `/api/students/{id}` CRUD + analysis/activity, CV upload
  `/cv`, artifacts, target-role `/target-role/esco`, learning
  `/learning*`, diagnostic, personalized-path, lessons, practice,
  mini-check, final-assessment status, scenarios, saved/recent roles,
  tutor (`/tutor`, `/tutor/tts`, `/tutor/stt`, `/tutor/conversations`,
  preference), copilot + onboarding, interviews, assessments + integrity,
  jobs tracker/saved/link-reports, match breakdowns.
- Careers/jobs: `/api/jobs/recent`, `/api/roles*`, `/api/skills`,
  `/api/companies`, ESCO import endpoints.
- Public: `/api/public/verified/{id}`, university cohort/stats
  (aggregated, anonymized), `/api/config/demo-mode` (redacted),
  `/api/system/db-status`, `/api/debug/tutor-system`.

### Frontend — `frontend/src/`
React 18 + TypeScript + Vite (SPA state machine in `App.tsx`, pages:
Login, Dashboard, SkillsRoles, Learning, Scenarios, Assessments,
University, PublicProfile). `lib/` API + types + voice engine
(`voiceSession.ts`, `useVoiceSession.ts`, `voiceStates.ts`, `useTTSPlayer.ts`,
`browserDetect.ts`, `interviewSession.ts`, `webcamIntegrity.ts`,
`tutorProfiles.ts`, `copilotArchetypes.ts`). `index.css` single stylesheet.

## 4. Environment variable names (no values shown)

`BACKEND_PORT`, `FRONTEND_PORT`, `VITE_API_URL`, `ELEVENLABS_API_KEY`,
`ELEVENLABS_MODEL`, `ELEVENLABS_NOVA/AXEL/SAGE/VEX_VOICE_ID`,
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `NVIDIA_API_KEY`, `NIM_BASE_URL`,
`NIM_MODEL`, `JSEARCH_API_KEY`, `RAPIDAPI_KEY`, `RAPIDAPI_LINKEDIN_KEY`,
`RAPIDAPI_GOOGLE_JOBS_KEY`, `ADZUNA_APP_ID/KEY`, `JOOBLE_API_KEY`,
`USAJOBS_API_KEY`, `LINKEDIN_JOBS_HOST/PATH`, `GOOGLE_JOBS_HOST/PATH`,
`SKILLBRIDGE_DB`, `SKILLBRIDGE_FRONTEND_DIST`, SMTP vars, Google OAuth vars.
`.env` exists in the private project and is git-ignored; values were never
printed or committed. Env loading today: `dotenv_local.py` applies only
`ELEVENLABS_*` from root `.env`, existing process env wins, and it is a no-op
under pytest. (This is the design Phase 1 task #9 will review.)

## 5. Baseline gates

### Backend
```
cd backend && ../.venv/bin/python -m pytest tests -q -p no:cacheprovider
Result: 61 failed, 1514 passed, 5 skipped in 448.94s (0:07:28)
```
Failure breakdown (61 total):
- **35 genuine product failures** (reproduced in a clean context):
  - `test_tutor_stt_fallback.py` (8) — missing `SpeechRecognition`
    dependency → `/tutor/stt` raises 501 "STT not available on this server"
    (confirmed live: POST `/api/students/1/tutor/stt` → 501). **[KNOWN #2]**
  - `test_learning_orchestrator.py` (6) — orchestrator API route is not
    registered in `main.py` (`learning_orchestrator` not imported).
    **[KNOWN #1]**
  - `test_trusted_cs_knowledge_base.py` (7), `test_learning_path_currency.py`
    (5), `test_curated_python_reliability.py` (4),
    `test_python_static_check.py` (3), `test_learning_quality_rescue.py` (1)
    — curated Python topics are reachable in `knowledge_base.complete_lesson`
    (`status=="complete"`), but `lessons.generate_lesson` does not attach the
    canonical content (`content["canonical"]["source"]` is `None`, falls back
    to the generic provider narrative; missing `canonical` key; worked-example
    does not contain the required `def parse_age` string; static checks not
    served for these topics). Reproduced directly:
    `generate_lesson("Python","Python Functions","learn")` →
    canonical source **None**, example lacks code. These are the "Learning
    reliability test mismatch" family. **[KNOWN #5]**
  - `test_scenarios_phase4_ux.py` (1) — `test_follow_up_resolves_skill_id_for_weak_component`
    asserts `follow_up.action == "lesson"` but `scenarios._follow_up` returns
    `"practice"`. **Not on the guide's known-failure list** — flagged as an
    extra genuine mismatch to triage in Phase 1/2 (see §Risks).
- **26 environment-induced failures** (proven NOT product failures): every
  `test_runtime_*_frontend.py` (24) and `test_tutor_profiles.py` (2) failed
  because the node-based source-contract checkers threw
  `EPERM: operation not permitted` opening `/Users/aboodmr/Desktop/...`
  files mid-run (macOS sandbox revoked Desktop reads during the run).
  Re-running every checker from the readable sandbox mirror:
  **24/24 runtime checkers PASS** (incl. `check-scenarios-family-phase3.mjs`,
  `check-webcam-integrity`, `check-tutor-memory`, `check-tutor-language`,
  `check-job-board-phaseN`, etc.) and `check-tutor-profiles.mjs` → **OK**.

### Frontend (from `frontend/`)
| Gate | Result |
|---|---|
| `npx tsc --noEmit` | **PASS** (exit 0, no diagnostics) |
| `node scripts/check-copilot-voice-unit.mjs` | **PASS** — 226 passed, 0 failed |
| `node scripts/check-mentor-live-phase4b1.mjs` | **FAIL** — legacy `VoiceOrb.tsx` is still present; must be removed **[KNOWN #3]** |
| `node scripts/check-learning-phase3-agentic.mjs` | **FAIL** — `LearningAgentActionType` missing `EXPLAIN` in `src/lib/types.ts` **[KNOWN #4]** |
| `node scripts/check-tutor-profiles.mjs` | **PASS** — 4 tutor profiles verified |
| `npm run build` | **PASS** — clean; only the known chunk-size advisory (>500 kB) |

All five of the guide's expected known failures reproduced exactly:
1. Missing learning-orchestrator route — confirmed (not imported in `main.py`).
2. Missing SpeechRecognition dependency — confirmed (not in
   `backend/requirements.txt`; not installed in `.venv`; `/tutor/stt` → 501).
3. Legacy `VoiceOrb.tsx` contract failure — confirmed (file exists, zero
   imports anywhere in `src/`; `check-mentor-live-phase4b1` fails on it).
4. Phase 3 agentic action-type mismatch — confirmed
   (`types.ts` has no `LearningAgentActionType`/`EXPLAIN`; checker crashes on it).
5. Learning reliability test mismatch — confirmed (curated Python content is not
   wired through `generate_lesson` / static-check path).

## 6. Isolated preview instance

```
SKILLBRIDGE_DB=/tmp/sb_baseline_demo.db  (copy of backend/skillbridge.db)
SKILLBRIDGE_FRONTEND_DIST=<frontend>/dist
uvicorn app.main:app --host 127.0.0.1 --port 8091
Running today at:  http://127.0.0.1:8091/
```
Live probes on the isolated instance:
- `GET /api/system/db-status` → engine sqlite, **13/13 migrations applied**
  (0001…0013_tutor_conversations).
- Login `aisha@student.edu` / `demo1234` → 200, bearer token, role Student.
- `GET /api/students/1/analysis` → 200, target "Junior AI Engineer",
  match 87.5, gaps incl. Docker (Beginner vs Intermediate).
- `GET /api/roles`, `/api/students/1/learning`, `/api/students/1/tutor` → 200.
- Company `hr@northstar.com` → `/api/roles` 200, `/api/company/roles/1/candidates` 200.
- University `admin@univ.edu` → `/api/university/cohort` 200, `/api/university/stats` 200.
- `GET /` → serves the SPA (index.html, 1,098 bytes).
- `POST /api/students/1/tutor/stt` → **501** (missing dependency — known).
- `GET /api/nonexistent-route` → currently returns **SPA index.html (200)**
  because the catch-all serves HTML before clients reach a structured
  `/api/*` 404 handler. **This is the Phase 1 task "unknown /api routes
  return structured API errors, never index.html".**

Browser verification (Puppeteer + system Chrome, against the isolated
instance): **Phase 6 regression 91/91 PASS** across desktop 1440 / tablet 820 /
mobile 390 for 4 students (omar, leila, aisha, yara) + Company + University —
sign-in renders, dashboards render, scenario security-family gating correct,
**no horizontal overflow, and no unexpected console errors** across all runs.

Screenshots captured in `docs/baseline-99950b0/`: `login-1440.png`,
`aisha-dashboard-1440.png`, plus the `p6-<role>-<width>.png` set from the
regression harness (all three roles at 1440/820/390).

## 7. Confirmed current features (present and reachable)

- Auth: signup/login/logout/google-demo/reset/verify; role-based routing;
  bearer sessions; copilot onboarding + settings.
- Student journey: CV upload → self-reported profile → target role → match →
  learning (explain → resources → roadmap) → practice → mini-check → final
  assessment → Verified Skill (authority boundary kept) → jobs/tracker.
- Skills & Roles: role library/explorer, canonical catalogue + ESCO market
  roles, role details/compare/transitions, saved & recent roles.
- Learning: diagnostic, personalized path, lessons (MCQ practice, static
  check UI), mini-check, final-assessment status, curated Python topics
  (content present in knowledge base; **not yet wired** end-to-end — see §6).
- Practice scenarios with save/resume/history, hint policy, integrity.
- Jobs: provider-fed board, jobs cache, tracker (saved/applied/…/archive),
  private notes, link reports, match breakdowns, provider-health diagnostics.
- Tutor: text chat w/ memory + mentor personas (Nova/Axel/Sage/Vex), language
  (EN/AR), Live voice UI (server-side STT fallback declared), TTS configured
  for all 4 mentors.
- University Admin: anonymized cohort stats + cohort-confirm flow.
- Arabic support in tutor/learning surfaces.

## 8. Problems and risks found (honest)

1. **The 5 known failures are all present** (see §5) — they define the Phase 1
   work precisely. No extra scaffolding was done (per Phase 0 freeze).
2. **Extra finding:** `test_scenarios_phase4_ux.py::test_follow_up_resolves_skill_id_for_weak_component`
   is failing and is not part of the guide's known-failure list. Behaviour is
   likely intentional (weak-competency follow-up now routes to *practice*
   instead of *lesson*), but the test was not updated. Must be triaged in
   Phase 1/2 rather than deleted.
3. **Unknown `/api/*` routes return SPA index.html (HTTP 200)** instead of a
   structured JSON 404 — confirmed live; target of Phase 1 task 10/acceptance.
4. **Runtime frontend contract tests depend on node reading workspace files**;
   under the macOS sandbox we observed transient `EPERM` denials that cause
   false failures. Re-verification from a readable context passed 24/24, so
   product code is clean — but this is worth documenting in `AGENTS.md` so
   future runs distinguish sandbox EPERM from real breakage.
5. **Large bundle:** `dist/assets/index-C-p5rRtT.js` ~1.28 MB minified
   (chunk-size advisory). Phase 9 (code splitting) item.
6. **Demo-mode status is honest:** on the private instance
   `/api/config/demo-mode` reported `genai_enabled: true` (NVIDIA super-120b),
   TTS available for all 4 voices, 6 configured jobs providers. No secrets
   appear in any redacted diagnostic output seen.
7. Port 8000 is already occupied by the user's own live uvicorn instance
   (`PID 92917`, system Python 3.14); Phase 0 deliberately used :8091 so the
   existing instance was untouched.
8. `.env.example` contains a stale/misleading "Database (PostgreSQL)" block
   (the app is SQLite); harmless but worth a doc fix in a later phase.

## 9. Files changed during Phase 0

**No product/source files were changed.** Only:
- gitignored tooling artifacts created in the working checkout:
  `scripts/browser-regression/node_modules/` (Puppeteer dev dependency,
  gitignored), `frontend/dist/` rebuilt (gitignored), `frontend/tsconfig.tsbuildinfo`
  (gitignored).
- New report/screenshots dir `docs/baseline-99950b0/` (this report + PNGs).
- `/tmp/sb_baseline_demo.db` — disposable copy of the private DB used for the
  isolated instance (outside the repo).
- The private ZIP `SkillBridge-FULL-PROJECT-PRIVATE.zip` was validated
  (`unzip -t` OK) and left untouched.

Note: during the run, the macOS sandbox intermittently denied Desktop-path
reads and then restored access to writes. All gate results were re-verified in
a readable sandbox context before being recorded above.

## 10. Command log (baseline)

```
unzip -t SkillBridge-FULL-PROJECT-PRIVATE.zip            # OK, no errors
git status && git log --oneline -10                      # clean @ 99950b0
git check-ignore -v                                      # secrets/db/deps ignored
cd backend && ../.venv/bin/python -m pytest tests -q     # 61f/1514p/5s in 448.94s
cd frontend && npx tsc --noEmit                          # exit 0
cd frontend && node scripts/check-copilot-voice-unit.mjs # 226 passed
cd frontend && node scripts/check-mentor-live-phase4b1.mjs   # FAIL: VoiceOrb legacy
cd frontend && node scripts/check-learning-phase3-agentic.mjs# FAIL: action types
cd frontend && node scripts/check-tutor-profiles.mjs     # OK
cd frontend && npm run build                             # PASS (size advisory)
SKILLBRIDGE_DB=/tmp/sb_baseline_demo.db uvicorn app.main:app --port 8091  # preview
node phase6-local.js  (browser-regression @ 1440/820/390) # 91/91 PASS
curl probes: db-status, config/demo-mode, login×3 roles, analysis, cohort,
             /tutor/stt (501), /api/nonexistent-route (SPA html)
```

## 11. Working preview

- **URL:** <http://127.0.0.1:8091/>
- Demo accounts (password `demo1234`): `aisha@student.edu` (Student),
  `omar@student.edu` (Student), `hr@northstar.com` (Company),
  `admin@univ.edu` (University Admin).
- Screenshots: `docs/baseline-99950b0/*.png`.

## 12. Recommended Phase 1 actions (in guide order)

1. Add the exact `SpeechRecognition` package to `backend/requirements.txt`
   and install it (fixes 8 STT tests + live 501).
2. Register the learning-orchestrator route before the SPA catch-all with
   guaranteed JSON responses (fixes 6 orchestrator tests).
3. Wire the orchestrator to existing learning state (authority boundary kept).
4. Reconcile `LearningAgentActionType` incl. `EXPLAIN` in `types.ts` (fixes
   `check-learning-phase3-agentic`).
5. Remove legacy `VoiceOrb.tsx` after confirming no imports (fixes
   `check-mentor-live-phase4b1`).
6. Wire curated Python content through `lessons.generate_lesson`/
   static-check path (fixes 20 learning-reliability failures); handle
   free-text questions deliberately.
7. Ensure provider calls stay disabled under pytest.
8. Deterministic, fast fresh seeding; lazy/queued provider enrichment.
9. Env/Dotenv consistency (existing env vars win).
10. Writable project-local npm cache for startup.
11. Make unknown `/api/*` return structured JSON errors (not index.html).

STOPPED here per the Phase 0 gate — awaiting human approval before Phase 1.