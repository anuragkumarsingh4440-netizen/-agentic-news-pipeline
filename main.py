"""AURA entry point.

    python main.py            # run the interactive loop
    AURA_MODE=local python main.py   # fully offline (local LLM via Ollama)

Keep this file thin: all wiring lives in the Orchestrator/factories so the
entry point has nothing to test.
"""

from __future__ import annotations

from src.core.config import Settings
from src.orchestrator import Orchestrator


def main() -> None:
    settings = Settings()
    Orchestrator(settings).run_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nbye.")
