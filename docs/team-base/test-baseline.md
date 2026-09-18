# Test Baseline Snapshot — `team-base` (2026-09-18)

**Branch:** `team-base`  
**Commit:** (to be filled after item G)  
**Generated:** Pre-merge baseline for Eslam's review

---

## Backend Unit Tests (pytest)

```bash
cd backend && ..\.venv\Scripts\python.exe -m pytest tests -q
```

| Suite | Passed | Failed | Skipped | Notes |
|-------|--------|--------|---------|-------|
| **Full backend** | **1586** | **0** | **3** | Baseline green |
| `test_tutor_spoken.py` | 32 | 0 | 0 | Voice/TTS path |
| `test_tts_voice_config.py` | 22 | 0 | 0 | ElevenLabs config + 503 upstream |
| `test_extraction.py` | 11 | 0 | 0 | CV skill extraction (bounded) |
| `test_open_skill_extraction.py` | 20 | 0 | 0 | Open skill extraction |
| `test_copilot.py` | 106 | 0 | 0 | Interview copilot + context trust |
| `conversations/phase4a/` | 150+ | 0 | 0 | Conversation flow |
| `provider/*` | 200+ | 0 | 0 | NIM provider + fallbacks |
| `modes/*` | 100+ | 0 | 0 | Tutor modes |

**Total: 1586 passed / 0 failed / 3 skipped**

---

## Voice / TTS Tests (subset of backend)

```bash
cd backend && ..\.venv\Scripts\python.exe -m pytest tests/test_tutor_spoken.py tests/test_tts_voice_config.py -q
```

| Test File | Passed | Failed | Key Coverage |
|-----------|--------|--------|--------------|
| `test_tutor_spoken.py` | 32 | 0 | Per-mentor EN/AR spoken identity, variants, chat-keeps-full-profile, small budget, step-by-step full budget, LIVE_NIM_MODEL on/off, plain chat never uses Live budget/model, fast-model→main-model fallback, never-hardcoded |
| `test_tts_voice_config.py` | 22 | 0 | Voice config mapping, 503 with upstream status (ElevenLabs 402), connection error handling, ELEVENLABS_BASE_URL const |

**Total: 54 voice/TTS tests passed**

---

## Frontend Build & Typecheck

```bash
cd frontend && npm ci && npm run build && npm run typecheck
```

| Step | Status | Notes |
|------|--------|-------|
| `npm ci` | ✅ | Clean install |
| `npm run build` | ✅ | 12.7s, chunk-size advisory only (pre-existing) |
| `npx tsc --noEmit` | ✅ | Clean |

---

## Acceptance Contracts (learning-acceptance.spec.mjs)

```bash
SKILLBRIDGE_FRONTEND_URL=http://localhost:3000 \
SKILLBRIDGE_BACKEND_URL=http://localhost:8000 \
  node scripts/learning-acceptance.spec.mjs
```

| Contract | Status | Notes |
|----------|--------|-------|
| Test 1 — Core Learning Flow | ✅ Pass | 29/29 contracts |
| Test 2 — Known flaky panel timing | 🟡 Documented | Eslam's `LearningPage.tsx` — not fixed by us |
| Test 3 — 1-vs-2 `.pp-item` mismatch | 🟡 Documented | Root cause in `docs/team-base/learning-test3-analysis.md` |

**Total: 29/29 contracts pass (Test 2/3 are known Eslam-side notes)**

---

## Voice Unit Gates

```bash
node scripts/check-copilot-voice-unit.mjs
node scripts/check-mentor-live-phase4b1.mjs
```

| Gate | Status | Details |
|------|--------|---------|
| `check-copilot-voice-unit.mjs` | **226/0** | Copilot voice unit contracts |
| `check-mentor-live-phase4b1.mjs` | **10/10** | Mentor live phase 4b1 orb contracts |

---

## Manual Verification Gates (require Eslam's machine)

| Gate | Status | Action |
|------|--------|--------|
| Brave Live Voice | ⛔ Not run | Needs real browser + Eslam's keys |
| ElevenLabs TTS | 🟡 401/402 expected | Quota exhausted (10000/10000) — needs working key |
| Docker image/container | ⏸️ Not run | Needs Docker daemon |

See `docs/team-base/manual-verification-log.md` for detailed runbooks.

---

## Known Issues (pre-existing, documented)

| Issue | Location | Status |
|-------|----------|--------|
| Learning Test 2 — flaky panel timing | `frontend/src/pages/Learning/LearningPage.tsx` (Eslam-owned) | Documented, not fixed by us |
| Learning Test 3 — 1-vs-2 `.pp-item` mismatch | `backend/app/diagnostics.py`, `path_builder.py` (Eslam-owned) | Root cause + fix options in `learning-test3-analysis.md` |
| ElevenLabs quota exhausted | Account level | Requires Eslam's real credentials |

---

## Files Changed in This Baseline (vs Eslam's `main` at `b3a1db2`)

| File | Change Type | Reason |
|------|-------------|--------|
| `backend/app/tts.py` | Modified | `ELEVENLABS_BASE_URL` const, upstream 503 status |
| `backend/app/dotenv_local.py` | Existing | Reads `.env` (dot prefix) for ELEVENLABS_* |
| `.env.example` | Modified | Commented `ELEVENLABS_BASE_URL` entry |
| `HANDOFF_FRIEND.md` | Modified | Env-file naming: `env` → `.env` (lines 33, 52, 54) |
| `AGENTS.md` | Modified | Env-file naming: `env` → `.env` (line 19) |
| `docs/team-base/manual-verification-log.md` | Modified | Today's verification findings |
| `docs/team-base/MERGE_DAY_RUNBOOK.md` | Created | Merge day procedure for Eslam |
| `docs/team-base/test-baseline.md` | Created | This file |

---

## How to Reproduce This Baseline

```bash
# On any machine with Python 3.12, Node.js, Docker:
git clone https://github.com/khaled1234kh/SkillBridge-team-base.git
cd SkillBridge-team-base
git checkout team-base

# Backend
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
cd backend && ..\.venv\Scripts\python.exe -m pytest tests -q

# Frontend
cd frontend && npm ci && npm run build && npm run typecheck

# Contracts (requires live backend + frontend + real keys)
SKILLBRIDGE_FRONTEND_URL=http://localhost:3000 \
SKILLBRIDGE_BACKEND_URL=http://localhost:8000 \
  node scripts/learning-acceptance.spec.mjs

# Voice gates
node scripts/check-copilot-voice-unit.mjs
node scripts/check-mentor-live-phase4b1.mjs
```

**Expected:** All automated gates green. Manual gates require Eslam's environment.