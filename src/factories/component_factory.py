"""Build I/O, auth, llm, and tools from Settings."""

from __future__ import annotations

from src.auth.interfaces import Authenticator
from src.auth.trusting_authenticator import TrustingAuthenticator
from src.core.config import Settings
from src.io.asr.console_listener import ConsoleListener
from src.io.interfaces import Listener, Speaker, WakeDetector
from src.io.tts.console_speaker import ConsoleSpeaker
from src.io.wake.always_on import AlwaysOn
from src.llm.interfaces import LLMProvider
from src.llm.litellm_provider import LiteLLMProvider
from src.tools.open_app import OpenAppTool
from src.tools.registry import ToolRegistry
from src.tools.run_command import RunCommandTool
from src.tools.send_email import SendEmailTool


def build_listener(s: Settings) -> Listener:
    if s.asr_provider == "whisper_local":
        # Lazy: only import the heavy class if actually selected.
        from src.io.asr.whisper_listener import WhisperListener
        try:
            return WhisperListener()
        except Exception:
            return ConsoleListener()  # graceful dev fallback
    return ConsoleListener()


def build_speaker(s: Settings) -> Speaker:
    return ConsoleSpeaker()


def build_wake(s: Settings) -> WakeDetector:
    return AlwaysOn()


def build_authenticator(s: Settings) -> Authenticator:
    # In a hardened build you'd return FaceAuthenticator and refuse to start
    # without an enrolled face. Dev uses the trusting one.
    return TrustingAuthenticator()


def build_llm(s: Settings) -> LLMProvider:
    return LiteLLMProvider(s)


def build_tools(s: Settings) -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(OpenAppTool())
    reg.register(SendEmailTool())
    reg.register(RunCommandTool())
    return reg
