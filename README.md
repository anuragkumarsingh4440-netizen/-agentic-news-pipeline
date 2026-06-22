# AURA — Autonomous User Response Agent

A local-first, voice + face driven desktop agent (a practical "Jarvis"): you
speak, it plans, it operates your machine through a set of reliable tools, and
it speaks back. Built on SOLID principles so it stays maintainable as it grows,
and designed to ship as a downloadable desktop app.

> Rename freely — `aura` is a placeholder package name.

## Why this design

The hard part of a Jarvis is **not** wiring an LLM to a microphone. It is
**reliability** (OS automation fails constantly) and **safety** (an agent that
sends email or runs shell commands "with no human in the loop" is a liability).
So the architecture is built around two ideas:

1. **Everything external sits behind an interface.** Speech, vision, the LLM,
   and OS control are all swappable (local ↔ cloud) without touching the core.
2. **One central safety gate.** Every non-trivial action is classified by risk
   and passes through a single confirmation + identity policy.

## Architecture

```
voice/face ─► ASR ─► Planner (LLM tool-loop) ─► Tools ─► OS / Email / Web
   ▲                     │            ▲   │
   └──── TTS ◄───────────┘   security gate (risk + identity + confirm)
```

| Layer | Folder | Interface | Swap local ↔ cloud |
|-------|--------|-----------|--------------------|
| Wake word | `src/io/wake` | `WakeDetector` | AlwaysOn ↔ openWakeWord |
| Speech-in | `src/io/asr` | `Listener` | Console ↔ faster-whisper ↔ Deepgram |
| Speech-out| `src/io/tts` | `Speaker` | Console ↔ Piper ↔ ElevenLabs |
| Face auth | `src/auth` | `Authenticator` | Trusting ↔ InsightFace |
| Brain | `src/llm` | `LLMProvider` | Gemini Flash / Pro / local Ollama (via litellm) |
| Hands | `src/tools` | `Tool` + `ToolRegistry` | open_app, send_email, run_command, … |
| Safety | `src/security` | `ConfirmationPolicy` | — |
| Memory | `src/memory` | `ConversationMemory` | InMemory ↔ SQLite ↔ vector |
| Wiring | `src/factories`, `src/orchestrator.py` | — | composition root |

## How SOLID maps here

- **S**ingle responsibility — each tool/provider does exactly one thing.
- **O**pen/closed — add a tool or model provider by registering it; the planner
  and registry never change.
- **L**iskov — any `Listener`/`LLMProvider`/`Tool` is interchangeable with any
  other; the orchestrator can't tell which concrete one it got.
- **I**nterface segregation — interfaces are tiny (`listen`, `speak`, `verify`).
- **D**ependency inversion — the orchestrator depends on interfaces; the
  factories inject concretes. That's the whole reason local/cloud is a config
  switch, not a rewrite.

## Models: Gemini (both) + local

Routing lives in `src/llm/litellm_provider.py`:

- normal planning → `gemini-1.5-flash` (cheap, fast)
- hard reasoning → `gemini-1.5-pro`
- any cloud failure / offline → local `ollama/llama3.1` fallback

The rest of the app never knows which answered.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # add GEMINI_API_KEY, or set AURA_MODE=local
python scripts/verify_setup.py
python main.py
```

Console mode (default) lets you type instead of talk, so you can exercise the
whole agent loop with no audio hardware. Try: `open echo`.

Fully offline:

```bash
AURA_MODE=local python main.py   # needs Ollama running locally
```

## The safety model (read this before enabling real tools)

Actions are tiered in `src/core/types.py`:

- `SAFE` — read-only / reversible → auto-runs (e.g. open an app).
- `SENSITIVE` — sends/changes something → requires confirmation (e.g. email).
- `DESTRUCTIVE` — irreversible / shell / payments → always confirmed **and**
  allow-listed (see `run_command`).

Non-`SAFE` actions also require a verified operator (`Authenticator`). Keep the
human confirm on the dangerous ~5%, automate the safe ~95% — that's the right
meaning of "end to end."

## Build order (MVP → full)

1. **Loop first (no audio):** Console listener/speaker + planner + 3 tools. ✅ shipped here.
2. **Voice:** wire `WhisperListener` (mic capture) + Piper TTS + a wake word.
3. **Identity:** implement `FaceAuthenticator` (enroll once, verify per session).
4. **Reach:** add browser control (Playwright) and Gmail/Calendar API tools.
5. **Memory + audit:** persist context; log every (request, plan, result) — this
   log is your eval/regression dataset.

## Packaging as a desktop download

- One-file build: `pyinstaller --onefile --name AURA main.py` → ship the binary.
- Bundle local models (whisper/piper) or download on first run.
- Sign the binary per-OS so Windows SmartScreen / macOS Gatekeeper don't block it.
- Distribute via your site / GitHub Releases; gate premium features with a
  license key checked at startup.

## Testing

```bash
pytest -q       # fast, no network — the LLM is faked in tests
ruff check .    # lint
```

## License

MIT — see `LICENSE`.
