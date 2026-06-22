"""AURA — Autonomous User Response Agent.

A local-first, voice + face driven desktop agent built on SOLID principles.
The package is organised so every external dependency (speech, vision, LLM,
OS control) sits behind an interface, and the orchestrator depends only on
those interfaces — never on a concrete library. That is what makes it both
testable and swappable (local <-> cloud) without touching the core loop.
"""

__version__ = "0.1.0"
