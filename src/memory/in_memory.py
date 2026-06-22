"""Simplest possible memory: an in-process ring of recent turns."""

from __future__ import annotations

from collections import deque
from typing import Deque, List

from src.memory.interfaces import ConversationMemory


class InMemoryConversation(ConversationMemory):
    def __init__(self, maxlen: int = 50) -> None:
        self._buf: Deque[dict] = deque(maxlen=maxlen)

    def add(self, role: str, content: str) -> None:
        self._buf.append({"role": role, "content": content})

    def recent(self, n: int = 10) -> List[dict]:
        return list(self._buf)[-n:]
