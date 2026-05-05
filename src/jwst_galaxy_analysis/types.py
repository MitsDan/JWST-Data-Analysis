"""Shared dataclasses used by the analysis modules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class GalaxySample:
    """Numerical arrays ready for plotting and downstream analysis.

    Attributes
    ----------
    name:
        Human-readable sample name, for example ``z2_ceers``.
    stellar_mass:
        Median stellar mass in log solar mass units.
    stellar_mass_err_low:
        Lower error on stellar mass in dex.
    stellar_mass_err_high:
        Upper error on stellar mass in dex.
    ab_mag:
        AB magnitude used on the y-axis. For CEERS this is the absolute
        magnitude inferred from observed flux plus distance modulus; for
        UNCOVER this is the catalog rest-frame U-band magnitude.
    ab_mag_err_low:
        Lower magnitude uncertainty.
    ab_mag_err_high:
        Upper magnitude uncertainty.
    redshift:
        Optional redshift array from the parent catalog.
    count_after_redshift:
        Number of rows after the redshift mask.
    count_after_nan_filter:
        Number of rows after first NaN filtering step.
    count_final:
        Number of rows after all quality cuts.
    """

    name: str
    stellar_mass: np.ndarray
    stellar_mass_err_low: np.ndarray
    stellar_mass_err_high: np.ndarray
    ab_mag: np.ndarray
    ab_mag_err_low: np.ndarray
    ab_mag_err_high: np.ndarray
    redshift: np.ndarray | None = None
    count_after_redshift: int = 0
    count_after_nan_filter: int = 0
    count_final: int = 0


@dataclass(frozen=True)
class PlotProducts:
    """Paths to generated plot products."""

    z2_plot: Path
    z3_plot: Path
