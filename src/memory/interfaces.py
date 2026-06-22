"""Memory contract — swap JSON for SQLite/vector store without touching callers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class ConversationMemory(ABC):
    @abstractmethod
    def add(self, role: str, content: str) -> None: ...

    @abstractmethod
    def recent(self, n: int = 10) -> List[dict]: ...
