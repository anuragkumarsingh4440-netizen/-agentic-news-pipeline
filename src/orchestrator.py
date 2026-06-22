"""Orchestrator — wires the layers and runs the top-level loop.

It depends ONLY on interfaces handed to it by the factories. Read it top to
bottom and you understand the whole system without opening any provider.
"""

from __future__ import annotations

from src.agent.planner import Planner
from src.core.config import Settings
from src.core.logging import get_logger
from src.factories.component_factory import (
    build_authenticator,
    build_listener,
    build_llm,
    build_speaker,
    build_tools,
    build_wake,
)
from src.memory.in_memory import InMemoryConversation
from src.security.policy import ConfirmationPolicy

log = get_logger("aura")


class Orchestrator:
    def __init__(self, settings: Settings) -> None:
        settings.validate()
        self._s = settings
        self._listener = build_listener(settings)
        self._speaker = build_speaker(settings)
        self._wake = build_wake(settings)
        auth = build_authenticator(settings)
        self._policy = ConfirmationPolicy(settings, auth)
        self._planner = Planner(
            llm=build_llm(settings),
            tools=build_tools(settings),
            memory=InMemoryConversation(),
            policy=self._policy,
            speaker=self._speaker,
        )

    def _confirm(self, prompt: str) -> bool:
        self._speaker.speak(prompt)
        return input("confirm [y/N]> ").strip().lower() == "y"

    def run_forever(self) -> None:
        self._speaker.speak("AURA ready. Say something (Ctrl+C to quit).")
        while True:
            self._wake.wait_for_wake()
            utt = self._listener.listen()
            if not utt.text:
                continue
            if utt.text.lower() in {"quit", "exit"}:
                self._speaker.speak("Goodbye.")
                return
            answer = self._planner.handle(utt, confirm_fn=self._confirm)
            self._speaker.speak(answer)
