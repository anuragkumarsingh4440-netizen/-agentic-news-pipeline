"""LLM provider abstraction.

We route through litellm so one call site works for Gemini Flash, Gemini Pro
AND a local Ollama model. The agent depends on the LLMProvider interface, not
on litellm — if you ever switch SDKs, only this folder changes (DIP).
"""
