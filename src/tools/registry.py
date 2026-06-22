"""Registry of available tools (Open/Closed friendly).

Register concrete tools at startup; the planner asks the registry for specs
and for execution. Nothing here knows what any specific tool does.
"""

from __future__ import annotations

from typing import Dict, List

from src.core.types import ToolResult
from src.tools.base import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Duplicate tool name: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]

    def specs(self) -> List[dict]:
        return [t.to_spec() for t in self._tools.values()]

    def run(self, tool_name: str, args: dict) -> ToolResult:
        # args passed as a dict (not **kwargs) so a tool's own 'name' argument
        # can never collide with the registry's parameter.
        return self.get(tool_name).run(**args)
