"""Shared fixtures. A fake LLM lets us test the agent loop with zero network."""

from __future__ import annotations

import json

import pytest

from src.core.config import Settings


class FakeLLM:
    """Scripted provider: returns queued responses in order."""

    def __init__(self, scripted):
        self._scripted = list(scripted)

    def complete(self, messages, tools=None, model=None):
        return self._scripted.pop(0)


@pytest.fixture
def settings(monkeypatch):
    monkeypatch.setenv("AURA_MODE", "local")  # no key required
    return Settings()


@pytest.fixture
def tool_call():
    def _make(name, args):
        return {"function": {"name": name, "arguments": json.dumps(args)}}
    return _make
