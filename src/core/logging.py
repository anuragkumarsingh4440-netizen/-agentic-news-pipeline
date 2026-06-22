"""Structured, secret-safe logging.

One configured logger for the whole app (SRP). A redaction filter strips
anything that looks like an API key before it can reach a file or console —
security must not depend on every call site remembering to be careful.
"""

from __future__ import annotations

import logging
import re
import sys

_SECRET_PATTERN = re.compile(r"(AIza[0-9A-Za-z\-_]{10,}|sk-[0-9A-Za-z\-_]{10,})")


class _RedactFilter(logging.Filter):
    """Replace anything resembling a key with ***REDACTED*** in every record."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _SECRET_PATTERN.sub("***REDACTED***", record.msg)
        return True


def get_logger(name: str = "aura") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # configure once
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"))
    handler.addFilter(_RedactFilter())
    logger.addHandler(handler)
    return logger
