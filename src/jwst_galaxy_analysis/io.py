"""Catalog input utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def read_fits_table(path: str | Path, **kwargs: Any):
    """Read a FITS catalog with ``astropy.table.Table``.

    Astropy is imported lazily so that package metadata and lightweight unit
    tests can run in minimal environments, while production analysis still uses
    the requested Astropy Table functionality.
    """

    try:
        from astropy.table import Table
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "astropy is required to read FITS catalogs. Install with `pip install astropy`."
        ) from exc

    catalog_path = Path(path).expanduser().resolve()
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catalog not found: {catalog_path}")
    return Table.read(catalog_path, format="fits", **kwargs)
