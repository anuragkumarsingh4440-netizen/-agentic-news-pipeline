"""The confirmation policy is the safety core — test it hard."""

from src.auth.trusting_authenticator import TrustingAuthenticator
from src.core.config import Settings
from src.core.types import Risk
from src.security.policy import ConfirmationPolicy


def test_safe_never_needs_confirmation(monkeypatch):
    monkeypatch.setenv("AURA_MODE", "local")
    p = ConfirmationPolicy(Settings(), TrustingAuthenticator())
    assert p.needs_confirmation(Risk.SAFE) is False


def test_sensitive_and_destructive_need_confirmation(monkeypatch):
    monkeypatch.setenv("AURA_MODE", "local")
    monkeypatch.setenv("AURA_CONFIRM", "1")
    p = ConfirmationPolicy(Settings(), TrustingAuthenticator())
    assert p.needs_confirmation(Risk.SENSITIVE) is True
    assert p.needs_confirmation(Risk.DESTRUCTIVE) is True
