"""CEERS catalog selection and photometric analysis."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from .config import AnalysisConfig, CEERSConfig
from .cosmology import absolute_magnitude, distance_modulus
from .photometry import abmag_error_from_flux, flux_njy_to_abmag, percentile_errors
from .types import GalaxySample
from .validation import as_float_array, finite_mask, range_mask, require_columns


def _extract_ceers_sample(
    catalog: Any,
    cfg: CEERSConfig,
    analysis_cfg: AnalysisConfig,
    *,
    name: str,
    redshift_min: float,
    redshift_max: float,
    flux_column: str,
    flux_error_column: str,
    reference_redshift: float,
    logger: logging.Logger,
) -> GalaxySample:
    required = [
        cfg.redshift_column,
        flux_column,
        flux_error_column,
        cfg.mass_column,
        cfg.mass_low_column,
        cfg.mass_high_column,
    ]
    require_columns(catalog, required, context=f"CEERS {name}")

    zmask = range_mask(catalog[cfg.redshift_column], redshift_min, redshift_max)
    sample = catalog[zmask]
    logger.info("%s redshift mask %.2f < z < %.2f: %d galaxies", name, redshift_min, redshift_max, len(sample))

    flux = as_float_array(sample[flux_column])
    non_nan_flux = np.isfinite(flux)
    nan_flux_indices = np.where(~non_nan_flux)[0]
    if len(nan_flux_indices) > 0:
        logger.debug("%s removed flux-NaN row indices: %s", name, nan_flux_indices.tolist())
    sample = sample[non_nan_flux]
    logger.info("%s after removing NaNs in %s: %d galaxies", name, flux_column, len(sample))

    flux = as_float_array(sample[flux_column])
    flux_err = as_float_array(sample[flux_error_column])
    mass = as_float_array(sample[cfg.mass_column])
    mass_low = as_float_array(sample[cfg.mass_low_column])
    mass_high = as_float_array(sample[cfg.mass_high_column])
    redshift = as_float_array(sample[cfg.redshift_column])

    apparent_mag = flux_njy_to_abmag(flux)
    mag_err = abmag_error_from_flux(flux, flux_err)
    dm = distance_modulus(reference_redshift, analysis_cfg.cosmology)
    abs_mag = absolute_magnitude(apparent_mag, dm)
    mass_err_low, mass_err_high = percentile_errors(mass, mass_low, mass_high)

    quality = (
        finite_mask(mass, mass_err_low, mass_err_high, apparent_mag, mag_err, abs_mag, redshift)
        & (mag_err <= cfg.max_ab_mag_error)
        & (mass_err_low <= cfg.max_mass_error)
        & (mass_err_high <= cfg.max_mass_error)
    )
    removed = int(len(quality) - np.count_nonzero(quality))
    if removed:
        logger.info("%s removed %d rows during CEERS final quality cuts", name, removed)

    logger.info("%s final catalog after quality cuts: %d galaxies", name, int(np.count_nonzero(quality)))
    return GalaxySample(
        name=name,
        stellar_mass=mass[quality],
        stellar_mass_err_low=mass_err_low[quality],
        stellar_mass_err_high=mass_err_high[quality],
        ab_mag=abs_mag[quality],
        ab_mag_err_low=mag_err[quality],
        ab_mag_err_high=mag_err[quality],
        redshift=redshift[quality],
        count_after_redshift=len(sample) + len(nan_flux_indices),
        count_after_nan_filter=len(sample),
        count_final=int(np.count_nonzero(quality)),
    )


def process_ceers(catalog: Any, analysis_cfg: AnalysisConfig, logger: logging.Logger) -> dict[str, GalaxySample]:
    """Process CEERS into z2 and z3 samples."""

    cfg = analysis_cfg.ceers
    z2 = _extract_ceers_sample(
        catalog,
        cfg,
        analysis_cfg,
        name=cfg.z2_name,
        redshift_min=cfg.z2_min,
        redshift_max=cfg.z2_max,
        flux_column=cfg.z2_flux_column,
        flux_error_column=cfg.z2_flux_error_column,
        reference_redshift=cfg.z2_reference_redshift,
        logger=logger,
    )
    z3 = _extract_ceers_sample(
        catalog,
        cfg,
        analysis_cfg,
        name=cfg.z3_name,
        redshift_min=cfg.z3_min,
        redshift_max=cfg.z3_max,
        flux_column=cfg.z3_flux_column,
        flux_error_column=cfg.z3_flux_error_column,
        reference_redshift=cfg.z3_reference_redshift,
        logger=logger,
    )
    return {cfg.z2_name: z2, cfg.z3_name: z3}
