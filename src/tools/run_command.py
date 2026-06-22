"""Run a shell command. DESTRUCTIVE — gated + never auto-runs.

An allow-list is the safe default; arbitrary shell from an LLM is how you wipe
a disk. The confirmation policy plus this allow-list are defence in depth.
"""

from __future__ import annotations

import subprocess
from typing import Any, Dict

from src.core.types import Risk, ToolResult
from src.tools.base import Tool

_ALLOWED = {"echo", "ls", "dir", "whoami", "date"}


class RunCommandTool(Tool):
    name = "run_command"
    description = "Run a whitelisted shell command and return its output."
    risk = Risk.DESTRUCTIVE

    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        }

    def run(self, **kwargs: Any) -> ToolResult:
        command = kwargs.get("command", "")
        head = command.strip().split(" ", 1)[0]
        if head not in _ALLOWED:
            return ToolResult(ok=False, summary="Blocked: command not in allow-list.", error=head)
        try:
            out = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            return ToolResult(ok=True, summary=out.stdout.strip()[:500] or "(no output)")
        except Exception as exc:
            return ToolResult(ok=False, summary="Command failed.", error=str(exc))
