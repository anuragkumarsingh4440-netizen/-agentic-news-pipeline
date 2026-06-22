"""Open a desktop application by name. SAFE (reversible)."""

from __future__ import annotations

import platform
import shutil
import subprocess
from typing import Any, Dict

from src.core.types import Risk, ToolResult
from src.tools.base import Tool


class OpenAppTool(Tool):
    name = "open_app"
    description = "Launch a desktop application by its name, e.g. 'chrome', 'notepad'."
    risk = Risk.SAFE

    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "App to open"}},
            "required": ["name"],
        }

    def run(self, **kwargs: Any) -> ToolResult:
        name = kwargs.get("name", "")
        system = platform.system()
        try:
            if system == "Darwin":
                subprocess.Popen(["open", "-a", name])
            elif system == "Windows":
                subprocess.Popen(["cmd", "/c", "start", "", name], shell=False)
            else:  # Linux
                exe = shutil.which(name) or name
                subprocess.Popen([exe])
            return ToolResult(ok=True, summary=f"Opened {name}.")
        except Exception as exc:
            return ToolResult(ok=False, summary=f"Could not open {name}.", error=str(exc))
