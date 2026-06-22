"""Console Listener — type instead of talk.

Critical for development and CI: it lets you exercise the entire agent loop
with zero audio hardware or model downloads. This is the provider you build
against first (see the MVP plan), before wiring real speech.
"""

from __future__ import annotations

from src.core.types import Utterance
from src.io.interfaces import Listener


class ConsoleListener(Listener):
    def listen(self) -> Utterance:
        text = input("you> ").strip()
        # In console mode we trust the operator, so speaker is 'verified'.
        return Utterance(text=text, speaker_verified=True, confidence=1.0)
