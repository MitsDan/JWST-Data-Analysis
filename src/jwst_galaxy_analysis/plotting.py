"""Plotting helpers for CEERS and UNCOVER comparisons."""

from __future__ import annotations

from pathlib import Path

from .config import PlottingConfig
from .types import GalaxySample, PlotProducts


def _plot_pair(
    ceers: GalaxySample,
    uncover: GalaxySample,
    *,
    title: str,
    output_path: Path,
    cfg: PlottingConfig,
) -> Path:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "matplotlib is required for plotting. Install with `pip install matplotlib`."
        ) from exc

    fig, ax = plt.subplots(figsize=cfg.figsize)

    ax.errorbar(
        ceers.stellar_mass,
        ceers.ab_mag,
        xerr=[ceers.stellar_mass_err_low, ceers.stellar_mass_err_high],
        yerr=[ceers.ab_mag_err_low, ceers.ab_mag_err_high],
        fmt=cfg.marker,
        markersize=4,
        elinewidth=1,
        capsize=2,
        color=cfg.ceers_color,
        label="JWST CEERS",
        alpha=0.85,
        zorder=3,
    )
    ax.errorbar(
        uncover.stellar_mass,
        uncover.ab_mag,
        xerr=[uncover.stellar_mass_err_low, uncover.stellar_mass_err_high],
        yerr=[uncover.ab_mag_err_low, uncover.ab_mag_err_high],
        fmt=cfg.marker,
        markersize=4,
        elinewidth=1,
        capsize=2,
        color=cfg.uncover_color,
        label="JWST UNCOVER",
        alpha=0.75,
        zorder=2,
    )

    ax.set_xlabel(r"$\log_{10} (Stellar \; Mass \, / \, M_{\odot})$", fontsize=20)
    ax.set_ylabel(r"AB mag", fontsize=20)
    ax.set_title(title, fontsize=20)
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="-", alpha=0.35)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.legend(fontsize=13)
    ax.tick_params(axis="both", which="major", labelsize=13)
    ax.tick_params(axis="both", which="minor", labelsize=11)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=cfg.dpi, bbox_inches="tight", pad_inches=0.5)
    plt.close(fig)
    return output_path


def plot_all(
    *,
    z2_ceers: GalaxySample,
    z2_uncover: GalaxySample,
    z3_ceers: GalaxySample,
    z3_uncover: GalaxySample,
    output_dir: Path,
    cfg: PlottingConfig,
) -> PlotProducts:
    """Generate z2 and z3 comparison plots."""

    z2_path = _plot_pair(
        z2_ceers,
        z2_uncover,
        title=r"Observed U-band mags vs M$_*$ (z = 2.0)",
        output_path=output_dir / cfg.z2_filename,
        cfg=cfg,
    )
    z3_path = _plot_pair(
        z3_ceers,
        z3_uncover,
        title=r"Observed U-band mags vs M$_*$ (z = 3.6)",
        output_path=output_dir / cfg.z3_filename,
        cfg=cfg,
    )
    return PlotProducts(z2_plot=z2_path, z3_plot=z3_path)
