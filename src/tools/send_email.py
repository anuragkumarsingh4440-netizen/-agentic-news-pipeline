"""Send an email. SENSITIVE — always passes through the confirmation policy.

Uses the Gmail API in production (not SMTP screen-scraping). Here the body is
stubbed so the skeleton runs; wire google-api-python-client to go live.
"""

from __future__ import annotations

from typing import Any, Dict

from src.core.types import Risk, ToolResult
from src.tools.base import Tool


class SendEmailTool(Tool):
    name = "send_email"
    description = "Send an email to a recipient with a subject and body."
    risk = Risk.SENSITIVE

    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["to", "subject", "body"],
        }

    def run(self, **kwargs: Any) -> ToolResult:
        to = kwargs.get("to", "")
        # TODO: call Gmail API here.
        return ToolResult(ok=True, summary=f"(stub) Email queued to {to}.", data=kwargs)
