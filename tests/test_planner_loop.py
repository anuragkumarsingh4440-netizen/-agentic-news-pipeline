"""The planner should call a tool, observe, then answer."""

from src.agent.planner import Planner
from src.auth.trusting_authenticator import TrustingAuthenticator
from src.core.config import Settings
from src.core.types import Utterance
from src.io.tts.console_speaker import ConsoleSpeaker
from src.memory.in_memory import InMemoryConversation
from src.security.policy import ConfirmationPolicy
from src.tools.registry import ToolRegistry
from src.tools.open_app import OpenAppTool
from tests.conftest import FakeLLM


def test_planner_runs_tool_then_finishes(monkeypatch, tool_call):
    monkeypatch.setenv("AURA_MODE", "local")
    s = Settings()
    tools = ToolRegistry()
    tools.register(OpenAppTool())
    llm = FakeLLM([
        {"text": "", "tool_calls": [tool_call("open_app", {"name": "echo"})]},
        {"text": "Opened it.", "tool_calls": []},
    ])
    planner = Planner(llm, tools, InMemoryConversation(),
                      ConfirmationPolicy(s, TrustingAuthenticator()), ConsoleSpeaker())
    out = planner.handle(Utterance("open echo", speaker_verified=True), confirm_fn=lambda _: True)
    assert "Opened" in out
