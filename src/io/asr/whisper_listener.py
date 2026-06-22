"""Local ASR via faster-whisper (private, offline, free).

Kept import-light: the heavy model only loads when this class is actually
instantiated, so importing the package (e.g. in tests) stays fast.
"""

from __future__ import annotations

from src.core.types import Utterance
from src.io.interfaces import Listener


class WhisperListener(Listener):
    def __init__(self, model_size: str = "base") -> None:
        # Imported lazily so the dependency is optional until used.
        from faster_whisper import WhisperModel  # noqa: PLC0415

        self._model = WhisperModel(model_size, compute_type="int8")

    def listen(self) -> Utterance:  # pragma: no cover - needs a mic
        # TODO: capture mic audio (sounddevice) -> numpy -> transcribe.
        raise NotImplementedError("Wire mic capture; see scripts/record_demo.py")
