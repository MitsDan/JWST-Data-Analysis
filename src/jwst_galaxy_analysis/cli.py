"""Command-line interface for the JWST galaxy analysis pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from .logging_utils import configure_logging
from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze CEERS and UNCOVER DR4 catalogs and plot stellar mass vs U-band AB magnitudes."
    )
    parser.add_argument(
        "--config",
        default="config/default.toml",
        type=Path,
        help="Path to a TOML configuration file.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Console logging level.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    logger = configure_logging(args.log_level)
    run_pipeline(args.config, logger=logger)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
