"""Small, shared value objects passed between layers.

Keeping these dataclasses free of behaviour means every layer can depend on
them without creating a cycle — they are the common vocabulary of the system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class Risk(str, Enum):
    """How dangerous an action is. Drives the confirmation policy."""

    SAFE = "safe"          # read-only / trivially reversible -> auto-run
    SENSITIVE = "sensitive"  # sends/changes something -> confirm
    DESTRUCTIVE = "destructive"  # irreversible / shell / payments -> always confirm


@dataclass
class ToolResult:
    """Uniform result every tool returns, so the planner can re-plan on failure
    instead of crashing or charging blindly ahead."""

    ok: bool
    summary: str
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class Utterance:
    """A transcribed user request plus who/where it came from."""

    text: str
    speaker_verified: bool = False
    confidence: float = 1.0
