"""Face-match authenticator (InsightFace/face_recognition).

Compares a live webcam frame against an enrolled embedding stored locally.
The embedding never leaves the machine.
"""

from __future__ import annotations

from src.auth.interfaces import Authenticator


class FaceAuthenticator(Authenticator):
    def __init__(self, enrolled_embedding_path: str) -> None:
        self._path = enrolled_embedding_path

    def verify(self) -> bool:  # pragma: no cover - needs a camera
        # TODO: capture frame -> embedding -> cosine-compare to enrolled.
        raise NotImplementedError("Wire webcam + embedding compare here.")
