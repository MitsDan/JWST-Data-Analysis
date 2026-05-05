"""Photometric transformations and uncertainty propagation."""

from __future__ import annotations

import numpy as np


def flux_njy_to_abmag(flux_njy: np.ndarray) -> np.ndarray:
    """Convert flux density in nanoJansky to AB magnitude with Astropy units.

    Non-positive or non-finite flux values are returned as NaN because AB
    magnitudes are undefined for those inputs.
    """

    flux = np.asarray(flux_njy, dtype=float)
    mag = np.full(flux.shape, np.nan, dtype=float)
    valid = np.isfinite(flux) & (flux > 0)
    if not np.any(valid):
        return mag

    try:
        from astropy import units as u
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "astropy is required for unit-based nJy-to-ABmag conversion. "
            "Install with `pip install astropy`."
        ) from exc

    mag[valid] = (flux[valid] * u.nJy).to(u.ABmag).value
    return mag


def abmag_error_from_flux(flux_njy: np.ndarray, flux_err_njy: np.ndarray) -> np.ndarray:
    """Propagate flux errors to AB magnitude errors.

    Uses dm = (2.5 / ln 10) * sigma_f / f for positive finite fluxes.
    """

    flux = np.asarray(flux_njy, dtype=float)
    flux_err = np.asarray(flux_err_njy, dtype=float)
    err = np.full(flux.shape, np.nan, dtype=float)
    valid = np.isfinite(flux) & np.isfinite(flux_err) & (flux > 0) & (flux_err >= 0)
    err[valid] = (2.5 / np.log(10.0)) * (flux_err[valid] / flux[valid])
    return err


def percentile_errors(median: np.ndarray, low: np.ndarray, high: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return lower and upper errors from median, 16th, and 84th percentiles."""

    median_arr = np.asarray(median, dtype=float)
    low_arr = np.asarray(low, dtype=float)
    high_arr = np.asarray(high, dtype=float)
    return median_arr - low_arr, high_arr - median_arr
