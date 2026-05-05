"""Logging helpers."""

from __future__ import annotations

import logging
import sys


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Configure and return the package logger."""

    logger = logging.getLogger("jwst_galaxy_analysis")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
        )
        logger.addHandler(handler)

    for handler in logger.handlers:
        handler.setLevel(getattr(logging, level.upper(), logging.INFO))

    return logger
