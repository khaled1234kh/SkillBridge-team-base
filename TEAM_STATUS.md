# TEAM_STATUS.md — SkillBridge-Unified shared development checkpoint

Branch: `team-base` (created from this checkpoint)
Repo:  `C:\Users\khale\Downloads\SkillBridge-Unified` (git newly initialised; **no remote yet**)
Date: 2026-09-18 (integration verification complete)

This file is the single source of truth for the team hand-off. Keep it updated per
release. Do NOT commit secrets, env files, databases, real student data, or uploads.

---

## 1. What was successfully merged

Version B (newer UI superset) is the base; Version A (learning superset) was layered
on top. Both originals remain untouched in `Downloads\SkillBridge-Final\SkillBridge-Final` (A)
and `Downloads\skillbridge-team-latest\skillbridge-team-latest` (B).

Backend (all verified content-identical to A / superset rules):
- knowledge_base, lessons, practice (PracticeGraderUnavailable path), path_builder
  (prerequisite_rank), skill_blueprint v2, models (INSERT OR IGNORE), plus A's curated
  test files (python reliability, learning, learning path currency, practice,
  trusted cs knowledge base, learning localization, curated sql foundations).
- genai.py / main.py: B base + A edits merged (context gating, careers; trusted
  diagnostic shortcut; learning orchestrator route; practice static checks + cache
  reuse; PracticeGraderUnavailable -> HTTP 503). tutor_memory.py differs (B's).
- requirements.txt adds: SpeechRecognition, audioop-lts, standard-aifc (A's voice deps).

Frontend:
- Kept B for: App.tsx, Icons.tsx, SkillsRolesPage.tsx, VoiceMode.tsx, VoiceOrb,
  useTTSPlayer, useVoiceSession, voiceSession, browserDetect, CopilotPanel (bar copy),
  index.css (B base).
- Replaced with A for: LearningPage.tsx, learning.tsx, types.ts, learning scripts,
  learning-acceptance.spec.mjs, HANDOFF.md, learning screenshot.
- Merged: index.css (B + A's lesson-language + pp-stale blocks), api.ts (learningAgentNext),
  CopilotPanel (learning context pill), MentorOrb (a11y), VoiceOrb removed from unified.

## 2. Actual test results (final, post-fix)

Run via isolated per-file pytest (each file capped; deterministic fallbacks, no
provider/network hangs). Complete backend suite: **111 test files, 1586 passed,
0 failed, 0 errors, 3 skipped** (1589 collected). The earlier interim tally "109
passed / 2 failed" predated two test-file fixes (test_tutor_stt_fallback.py,
test_scenarios_phase4_ux.py); both now pass — there is no remaining backend failure.

- Frontend: `tsc --noEmit` PASS; `npm run build` PASS (13.5s).
- 29 frontend `check-*.mjs` contract scripts: 29/29 PASS.
- Voice/STT: 72 backend tests PASS (TTS config, spoken tutor, STT fallback, provider,
  voice frontend UX, interview voice UX).
- Learning acceptance: 2 of 5 passing on the tested browser set; see section 3.

## 3. Known Learning acceptance failures (pre-existing, NOT merge regressions)

Covered by `backend/tests/test_scenarios_learning_phase1_frontend.py` (browser
acceptance spec, run manually in a headed browser). Failure 3 is deterministic and
pre-existing (it exists on original A too, verified): after the spec submits the
curated diagnostic answers, the dashboard's personalized-path builder emits a
1-item path because `python_functions` is still "developing"; the spec expects 2.
This is a product-behaviour gap (remediation ordering), not an integration fault.
Failures affect tests 3-5 of the spec. The curated question bank is unchanged (per
team rule: do not alter curated content just to satisfy a test).

## 4. Unverified / not fully validated on this machine

- Live Voice in the Brave browser: B's partial fix (isBrave + server-side STT) is
  present but cannot be auto-validated headlessly; needs a real-browser manual pass.
- ElevenLabs TTS returns 401 locally (env-only key, not in repo). STT/TTS provider
  health requires real keys on the dev machine.
- Docker images / containerised startup were not re-run in this merge pass.
- Learning browser acceptance (2 of 5) — see section 3.

## 5. Curriculum plan (45-topic CS goal) — file ownership

Root plan + 45-topic list: `docs/curriculum/45-topic-CS-curriculum.md`;
per-developer ownership map: `docs/curriculum/team-curriculum-ownership.md`.

Split (each developer owns disjoint files/dirs so they never edit the same backend
file):
- Developer A — SQL (10 topics) + Git (11 topics): `cs_sql_*` + `cs_git_*` lesson
  files and test files only.
- Developer B — Docker (11 topics) + Machine Learning (11 topics): `cs_docker_*` +
  `ml_*` lesson/test files only.
- Developer C — Core app improvements, learning stability, voice/other product
  features: shared app code/backend (uses team-base branch).

Existing two Python topics (curated python reliability) are preserved intact and are
shared context (do not delete).

IMPORTANT: Lessons are NOT generated yet. Only the plan + ownership split exist.
Do not generate the remaining lessons until each developer accepts their slice.

## 6. Branch workflow for teammates (pulling team-base)

1. Clone the finished repo (remote + URL to be added after approval — local only for now):
   `git clone <repo-url> SkillBridge-Unified`
   `cd SkillBridge-Unified`
2. Fetch and track the integration branch:
   `git fetch origin`
   `git checkout -b team-base origin/team-base`
3. Cut your own feature branch (NEVER commit directly to team-base):
   `git checkout -b dev-<name>/<feature> team-base`
4. Develop only files you own (see section 5). Commit small, write clear messages.
5. Push and open a Pull Request into `team-base`:
   `git push -u origin dev-<name>/<feature>`
6. After your PR is approved/merged, re-sync:
   `git checkout team-base && git pull && git checkout -b dev-<name>/<next-feature> team-base`

## 7. Safety / hygiene (never violated)

- Never commit: `.env`, `*.db`, `users_dump.txt`, uploads, `node_modules/`, `.venv/`,
  `dist/`, `__pycache__/`, `*.tsbuildinfo`, any real student data, or API keys.
- All secrets live in env files that are git-ignored + git-excluded.
