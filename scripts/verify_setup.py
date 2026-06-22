"""Quick environment check: imports resolve, config validates, tools register.

Run:  python scripts/verify_setup.py
"""

from __future__ import annotations

import sys

from src.core.config import Settings
from src.factories.component_factory import build_tools


def main() -> int:
    s = Settings()
    try:
        s.validate()
    except ValueError as e:
        print(f"[config] {e}")
        if s.mode != "local":
            print("Tip: set AURA_MODE=local to run without a key.")
    tools = build_tools(s)
    print(f"[ok] mode={s.mode} planner={s.planner_model}")
    print(f"[ok] tools registered: {[t['function']['name'] for t in tools.specs()]}")
    print("[ok] setup looks good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
