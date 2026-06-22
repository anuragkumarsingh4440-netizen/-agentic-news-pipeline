"""litellm-backed provider with tiered model routing + offline fallback.

Routing policy (Strategy-ish):
- normal planning  -> flash  (cheap, fast)
- explicit heavy   -> pro    (hard reasoning)
- any cloud error  -> local  (so the agent degrades instead of dying)

This is where 'both Gemini models + local' lives — and the rest of the app is
unaware of which one answered.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.core.config import Settings
from src.core.logging import get_logger
from src.llm.interfaces import LLMProvider

log = get_logger("aura.llm")


class LiteLLMProvider(LLMProvider):
    def __init__(self, settings: Settings) -> None:
        self._s = settings

    def complete(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        from litellm import completion  # lazy import

        chosen = model or self._s.planner_model
        try:
            resp = completion(model=chosen, messages=messages, tools=tools)
        except Exception as exc:  # cloud down / quota / offline
            log.warning("Cloud model '%s' failed (%s); falling back to local.", chosen, exc)
            resp = completion(model=self._s.local_model, messages=messages, tools=tools)

        msg = resp["choices"][0]["message"]
        return {
            "text": msg.get("content") or "",
            "tool_calls": msg.get("tool_calls") or [],
        }
