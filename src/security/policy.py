"""Confirmation policy — the line between 'assistant' and 'liability'.

Rule: SAFE auto-runs; SENSITIVE and DESTRUCTIVE require explicit confirmation
when settings.require_confirmation is on. Identity (Authenticator) is checked
before any non-SAFE action regardless. This is intentionally boring and
centralised so the dangerous decision lives in exactly one auditable place.
"""

from __future__ import annotations

from src.auth.interfaces import Authenticator
from src.core.config import Settings
from src.core.types import Risk


class ConfirmationPolicy:
    def __init__(self, settings: Settings, authenticator: Authenticator) -> None:
        self._s = settings
        self._auth = authenticator

    def needs_confirmation(self, risk: Risk) -> bool:
        if risk == Risk.SAFE:
            return False
        return self._s.require_confirmation

    def is_authorized(self, risk: Risk) -> bool:
        """Non-SAFE actions require a verified operator."""
        if risk == Risk.SAFE:
            return True
        return self._auth.verify()
