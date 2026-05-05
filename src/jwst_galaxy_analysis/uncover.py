"""UNCOVER DR4 SPS catalog selection and extraction."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from .config import AnalysisConfig, UNCOVERConfig
from .photometry import percentile_errors
from .types import GalaxySample
from .validation import as_float_array, finite_mask, range_mask, require_columns


def _extract_uncover_sample(
    catalog: Any,
    cfg: UNCOVERConfig,
    *,
    name: str,
    redshift_min: float,
    redshift_max: float,
    logger: logging.Logger,
) -> GalaxySample:
    required = [
        cfg.redshift_column,
        cfg.mass_column,
        cfg.mass_low_column,
        cfg.mass_high_column,
        cfg.rest_u_column,
        cfg.rest_u_low_column,
        cfg.rest_u_high_column,
    ]
    require_columns(catalog, required, context=f"UNCOVER {name}")

    zmask = range_mask(catalog[cfg.redshift_column], redshift_min, redshift_max)
    sample = catalog[zmask]
    logger.info("%s redshift mask %.2f < z < %.2f: %d galaxies", name, redshift_min, redshift_max, len(sample))

    mass = as_float_array(sample[cfg.mass_column])
    rest_u = as_float_array(sample[cfg.rest_u_column])
    base_valid = finite_mask(mass, rest_u)
    bad_indices = np.where(~base_valid)[0]
    if len(bad_indices) > 0:
        logger.debug("%s removed mstar_50/rest_U_50 NaN row indices: %s", name, bad_indices.tolist())
    sample = sample[base_valid]
    logger.info("%s after removing NaNs in %s or %s: %d galaxies", name, cfg.mass_column, cfg.rest_u_column, len(sample))

    mass = as_float_array(sample[cfg.mass_column])
    mass_low = as_float_array(sample[cfg.mass_low_column])
    mass_high = as_float_array(sample[cfg.mass_high_column])
    rest_u = as_float_array(sample[cfg.rest_u_column])
    rest_u_low = as_float_array(sample[cfg.rest_u_low_column])
    rest_u_high = as_float_array(sample[cfg.rest_u_high_column])
    redshift = as_float_array(sample[cfg.redshift_column])

    mass_err_low, mass_err_high = percentile_errors(mass, mass_low, mass_high)
    rest_u_err_low, rest_u_err_high = percentile_errors(rest_u, rest_u_low, rest_u_high)

    final_mask = finite_mask(
        mass,
        mass_err_low,
        mass_err_high,
        rest_u,
        rest_u_err_low,
        rest_u_err_high,
        redshift,
    )
    removed_final = int(len(final_mask) - np.count_nonzero(final_mask))
    if removed_final:
        logger.info("%s removed %d rows with non-finite percentile-derived errors", name, removed_final)

    logger.info("%s final catalog: %d galaxies", name, int(np.count_nonzero(final_mask)))
    return GalaxySample(
        name=name,
        stellar_mass=mass[final_mask],
        stellar_mass_err_low=mass_err_low[final_mask],
        stellar_mass_err_high=mass_err_high[final_mask],
        ab_mag=rest_u[final_mask],
        ab_mag_err_low=rest_u_err_low[final_mask],
        ab_mag_err_high=rest_u_err_high[final_mask],
        redshift=redshift[final_mask],
        count_after_redshift=len(sample) + len(bad_indices),
        count_after_nan_filter=len(sample),
        count_final=int(np.count_nonzero(final_mask)),
    )


def process_uncover(catalog: Any, analysis_cfg: AnalysisConfig, logger: logging.Logger) -> dict[str, GalaxySample]:
    """Process UNCOVER into z2 and z3 samples."""

    cfg = analysis_cfg.uncover
    z2 = _extract_uncover_sample(
        catalog,
        cfg,
        name=cfg.z2_name,
        redshift_min=cfg.z2_min,
        redshift_max=cfg.z2_max,
        logger=logger,
    )
    z3 = _extract_uncover_sample(
        catalog,
        cfg,
        name=cfg.z3_name,
        redshift_min=cfg.z3_min,
        redshift_max=cfg.z3_max,
        logger=logger,
    )
    return {cfg.z2_name: z2, cfg.z3_name: z3}
