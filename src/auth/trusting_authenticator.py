"""Dev authenticator that always trusts the operator.

NEVER ship this in 'cloud'/production with sensitive tools enabled — it exists
so the loop is testable. The factory refuses to select it when confirmation is
disabled in a non-dev mode.
"""

from __future__ import annotations

from src.auth.interfaces import Authenticator


class TrustingAuthenticator(Authenticator):
    def verify(self) -> bool:
        return True
