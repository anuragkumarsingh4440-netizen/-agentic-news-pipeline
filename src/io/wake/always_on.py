"""A no-op wake detector that returns immediately.

Used in console/hybrid dev so you are not forced to say a wake word every turn.
Swap for an openWakeWord/Porcupine detector in production.
"""

from __future__ import annotations

from src.io.interfaces import WakeDetector


class AlwaysOn(WakeDetector):
    def wait_for_wake(self) -> None:
        return None
