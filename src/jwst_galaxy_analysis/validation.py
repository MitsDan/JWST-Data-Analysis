"""Validation helpers for catalog columns and numerical masks."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np


def table_column_names(table: Any) -> set[str]:
    """Return a set of column names for an Astropy table-like object."""

    if hasattr(table, "colnames"):
        return set(table.colnames)
    if hasattr(table, "columns"):
        return set(table.columns)
    raise TypeError("Expected an Astropy Table-like object with colnames or columns.")


def require_columns(table: Any, columns: Iterable[str], context: str = "catalog") -> None:
    """Raise a clear error if required columns are absent."""

    existing = table_column_names(table)
    missing = sorted(set(columns) - existing)
    if missing:
        raise ValueError(f"Missing required columns in {context}: {', '.join(missing)}")


def as_float_array(values: Any) -> np.ndarray:
    """Convert a table column to a plain float NumPy array."""

    return np.asarray(values, dtype=float)


def finite_mask(*arrays: Any) -> np.ndarray:
    """Return a mask that is finite for every supplied array."""

    if not arrays:
        raise ValueError("At least one array is required to build a finite mask.")
    mask = np.ones_like(as_float_array(arrays[0]), dtype=bool)
    for arr in arrays:
        mask &= np.isfinite(as_float_array(arr))
    return mask


def range_mask(values: Any, lower: float, upper: float) -> np.ndarray:
    """Return finite values satisfying ``lower < value < upper``."""

    arr = as_float_array(values)
    return np.isfinite(arr) & (arr > lower) & (arr < upper)
