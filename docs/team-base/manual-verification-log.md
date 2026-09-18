# Manual Verification Log — Live Voice / TTS / Docker

**Owner:** Khaled (ops for team-base) · **Branch:** `team-base` · **Date:** 2026-09-18
**Rule applied:** anything requiring a **real browser, real credentials, or a
Docker daemon** cannot be proven from a headless shell — so each item below is
logged with an **exact numbered runbook** for Eslam to execute on his machine.
Nothing here was claimed "passing" — these are **open manual gates**, not verified.

---

## Gate 1 — Brave Live Voice (acceptance Test Three's live-voice path) — BLOCKED on automation, needs your real browser

Verify in **Brave** (not a synthetic headless pass). Run on Eslam's machine within
the `team-base` worktree:

```bash
# 1) start the stack on the SAME machines as the acceptance run
docker compose up --build -d          # backend + frontend + db
# 2) confirm both services respond
curl -fsS http://localhost:8000/api/system/health
curl -fsS http://localhost:3000
# 3) open the Learning page -> Python -> start the Live-Voice lesson
#    and speak 2-3 practice responses out loud. Record the console/browser
#    trace lines the UI logs between STT start and the transcript rendering.
# 4) paste the captured [voice-live] trace here so we keep the pass as evidence:
```

> **Expectation:** STT transcript appears in the practice box; the lesson advances
> to the Mini Check without manual typing. If the panel shows a microphone-deny
> or a silent clip, note the exact browser console error — that's an A-side
> (voice) backend concern we will document for Eslam, **not** a team-base change.

---

## Gate 2 — ElevenLabs TTS — 401 is EXPECTED until real keys are set

We run ElevenLabs through `ELEVENLABS_API_KEY`. Locally on the dev machine the
key is NOT set, so the provider reports HTTP 401. **That is the expected,
documented state — a 401 is not a regression.**

To confirm after keys are present (Eslam):
```bash
# set a real key first
$env:ELEVENLABS_API_KEY='...'
# from team-base root
curl -fsS -X POST http://localhost:8000/api/tutor/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"hello","voice":"jessica"}'
# 2xx with audio bytes => provider healthy
```

---

## Gate 3 — Docker image + container startup (local)

The backend runs in Docker via `docker-compose.yml` (B-side file). On a machine
with a Docker daemon:

```bash
docker compose build backend            # image build
docker compose up -d backend            # container start
docker compose logs -f backend          # watch for "SkillBridge backend up"
curl -fsS http://localhost:8000/api/system/db-status   # health probe
```
Expected: image builds without warnings-as-errors beyond the declared model
download; container stays `Up`; db-status returns 200. If the container exits
with a model-download timeout, that is a network/environment factor, not a
merge artifact — log the trace under `docs/team-base/` and we will review before
declaring anything.

---

## Summary state (do not mark these green until Eslam runs the above)

| Gate | Status now | Action needed |
|------|-----------|---------------|
| Brave Live Voice | ⛔ not run (needs real browser) | Eslam runs step 1, pastes `[voice-live]` trace |
| ElevenLabs TTS | 🟡 401 expected (no key in env) | set key, then re-run Gate 2 |
| Docker image/container | ⏸️ not run on a Docker host | Eslam runs Gate 3, paste `docker logs` |

These are the **only** gates that cannot be proven from a headless shell; backend
unit (`1586 passed`) and frontend build/tsc/acceptance-contract runs (`29/29`)
are logged in `docs/team-base/` test reports and in `TEAM_STATUS.md`.
