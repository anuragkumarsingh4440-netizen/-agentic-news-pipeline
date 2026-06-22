"""Planner — turns a request into tool calls and reacts to results.

Template Method: handle() runs the fixed loop (ask LLM -> maybe call tool ->
feed result back -> repeat until the LLM stops calling tools). Subclasses /
config decide *which* models and tools, never the control flow.

Reliability is the whole point: every tool returns a ToolResult, so when an
action fails the planner gets structured feedback and can recover instead of
crashing. That recovery loop is where a data-scientist's eval mindset pays off
— log every (request, plan, result) triple and you have a regression dataset.
"""

from __future__ import annotations

from typing import List

from src.core.logging import get_logger
from src.core.types import Utterance
from src.io.interfaces import Speaker
from src.llm.interfaces import LLMProvider
from src.memory.interfaces import ConversationMemory
from src.security.policy import ConfirmationPolicy
from src.tools.registry import ToolRegistry

log = get_logger("aura.agent")

_SYSTEM = (
    "You are AURA, a desktop assistant. Decide which tools to call to satisfy "
    "the user. Prefer the smallest safe set of actions. If a tool result shows "
    "failure, adapt; do not repeat the same failing call."
)


class Planner:
    def __init__(
        self,
        llm: LLMProvider,
        tools: ToolRegistry,
        memory: ConversationMemory,
        policy: ConfirmationPolicy,
        speaker: Speaker,
        max_steps: int = 6,
    ) -> None:
        self._llm = llm
        self._tools = tools
        self._memory = memory
        self._policy = policy
        self._speaker = speaker
        self._max_steps = max_steps

    def handle(self, utt: Utterance, confirm_fn) -> str:
        """Run the loop for one user request. `confirm_fn(text)->bool` asks the
        human to approve a risky action (injected, so it works by voice or CLI)."""
        self._memory.add("user", utt.text)
        messages: List[dict] = [{"role": "system", "content": _SYSTEM}]
        messages += self._memory.recent(10)

        for step in range(self._max_steps):
            resp = self._llm.complete(messages, tools=self._tools.specs())
            calls = resp["tool_calls"]

            if not calls:  # LLM is done; final answer is plain text.
                answer = resp["text"] or "Done."
                self._memory.add("assistant", answer)
                return answer

            for call in calls:
                name = call["function"]["name"]
                import json
                args = json.loads(call["function"].get("arguments") or "{}")
                tool = self._tools.get(name)

                # 1) identity gate, 2) confirmation gate — both before running.
                if not self._policy.is_authorized(tool.risk):
                    return "I couldn't verify it's you, so I won't do that."
                if self._policy.needs_confirmation(tool.risk):
                    if not confirm_fn(f"Confirm {name} ({tool.risk.value})? args={args}"):
                        messages.append({"role": "tool", "name": name,
                                         "content": "User declined this action."})
                        continue

                result = self._tools.run(name, args)
                log.info("tool=%s ok=%s :: %s", name, result.ok, result.summary)
                messages.append({"role": "assistant", "content": f"called {name}"})
                messages.append({"role": "tool", "name": name,
                                 "content": result.summary if result.ok else f"ERROR: {result.error}"})

        return "Stopped after too many steps — please rephrase."
