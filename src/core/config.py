"""Central, validated configuration (loaded once, injected everywhere).

Why a dedicated config object instead of reading os.environ all over the code:
- Single Responsibility — one place knows how the app is wired.
- Dependency Inversion — the orchestrator receives a Settings object; it does
  not reach into the environment itself, so tests can pass a fake.
- Security — secrets come from the environment / .env and are never hard-coded
  or logged.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal

from dotenv import load_dotenv

load_dotenv()  # read .env if present; real env vars still win.

Mode = Literal["local", "cloud", "hybrid"]


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings.

    frozen=True so nothing mutates config mid-run — a whole class of bugs gone.
    """

    # Which tier of components to prefer. "hybrid" = local I/O, cloud planner.
    mode: Mode = field(default_factory=lambda: os.getenv("AURA_MODE", "hybrid"))  # type: ignore

    # LLM routing — litellm model strings. Flash for cheap planning, Pro for
    # hard reasoning, a local Ollama model as the offline fallback.
    planner_model: str = field(default_factory=lambda: os.getenv("AURA_PLANNER_MODEL", "gemini/gemini-1.5-flash"))
    heavy_model: str = field(default_factory=lambda: os.getenv("AURA_HEAVY_MODEL", "gemini/gemini-1.5-pro"))
    local_model: str = field(default_factory=lambda: os.getenv("AURA_LOCAL_MODEL", "ollama/llama3.1"))

    # Secrets (never logged). Empty string means "not configured".
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""), repr=False)

    # I/O provider selection — resolved by the factories.
    asr_provider: str = field(default_factory=lambda: os.getenv("AURA_ASR", "whisper_local"))
    tts_provider: str = field(default_factory=lambda: os.getenv("AURA_TTS", "piper_local"))

    # Safety: actions in this tier always need an explicit human confirm.
    require_confirmation: bool = field(default_factory=lambda: os.getenv("AURA_CONFIRM", "1") == "1")

    data_dir: str = field(default_factory=lambda: os.getenv("AURA_DATA_DIR", os.path.expanduser("~/.aura")))

    def validate(self) -> None:
        """Fail fast with a clear message rather than a confusing error later."""
        if self.mode not in ("local", "cloud", "hybrid"):
            raise ValueError(f"Invalid AURA_MODE: {self.mode}")
        if self.mode in ("cloud", "hybrid") and not self.gemini_api_key:
            raise ValueError(
                "Cloud planning selected but GEMINI_API_KEY is unset. "
                "Set it in .env or switch AURA_MODE=local."
            )
