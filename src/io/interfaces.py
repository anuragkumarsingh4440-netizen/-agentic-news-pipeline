"""I/O interfaces — the contracts the orchestrator depends on (DIP)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.types import Utterance


class Listener(ABC):
    """Anything that can turn microphone audio into text."""

    @abstractmethod
    def listen(self) -> Utterance:
        """Block until a complete utterance is captured, then return it."""
        raise NotImplementedError


class Speaker(ABC):
    """Anything that can speak a string out loud."""

    @abstractmethod
    def speak(self, text: str) -> None:
        raise NotImplementedError


class WakeDetector(ABC):
    """Anything that blocks until the wake word is heard."""

    @abstractmethod
    def wait_for_wake(self) -> None:
        raise NotImplementedError
