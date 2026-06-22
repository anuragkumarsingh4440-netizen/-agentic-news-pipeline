"""Console Speaker — prints instead of talking. Dev/CI default."""

from __future__ import annotations

from src.io.interfaces import Speaker


class ConsoleSpeaker(Speaker):
    def speak(self, text: str) -> None:
        print(f"aura> {text}")
