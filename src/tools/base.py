"""Tool interface + the JSON schema the LLM sees.

Template Method-ish: the planner calls .run(**args); each concrete tool
implements the body and returns a uniform ToolResult so failures are data,
not exceptions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from src.core.types import Risk, ToolResult


class Tool(ABC):
    name: str
    description: str
    risk: Risk = Risk.SAFE

    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON-schema of accepted args (fed to the LLM tool spec)."""
        raise NotImplementedError

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError

    def to_spec(self) -> Dict[str, Any]:
        """Render the OpenAI/Gemini-style function spec for tool calling."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters(),
            },
        }
