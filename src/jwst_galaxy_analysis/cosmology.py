"""Cosmological helpers based on Astropy."""

from __future__ import annotations

import numpy as np

from .config import CosmologyConfig


def make_flat_lambdacdm(config: CosmologyConfig):
    """Construct an ``astropy.cosmology.FlatLambdaCDM`` instance."""

    try:
        from astropy.cosmology import FlatLambdaCDM
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "astropy is required for FlatLambdaCDM calculations. Install with `pip install astropy`."
        ) from exc

    return FlatLambdaCDM(H0=config.H0, Om0=config.Om0, Tcmb0=config.Tcmb0)


def distance_modulus(redshift: float, config: CosmologyConfig) -> float:
    """Return distance modulus at ``redshift`` for the configured cosmology."""

    cosmology = make_flat_lambdacdm(config)
    return float(cosmology.distmod(redshift).value)


def absolute_magnitude(apparent_ab_mag: np.ndarray, dist_mod: float) -> np.ndarray:
    """Compute absolute magnitude from apparent AB magnitude and distance modulus."""

    return np.asarray(apparent_ab_mag, dtype=float) - dist_mod
