"""Authenticator contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Authenticator(ABC):
    @abstractmethod
    def verify(self) -> bool:
        """Return True only if the enrolled operator is present."""
        raise NotImplementedError
