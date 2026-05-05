"""Top-level pipeline orchestration."""

from __future__ import annotations

import logging
from pathlib import Path

from .ceers import process_ceers
from .config import AnalysisConfig, load_config
from .io import read_fits_table
from .plotting import plot_all
from .types import GalaxySample, PlotProducts
from .uncover import process_uncover


def run_pipeline(
    config: AnalysisConfig | str | Path = "config/default.toml",
    *,
    logger: logging.Logger | None = None,
) -> tuple[dict[str, GalaxySample], PlotProducts]:
    """Run the full CEERS + UNCOVER analysis pipeline.

    Parameters
    ----------
    config:
        Either an ``AnalysisConfig`` instance or a path to a TOML config file.
    logger:
        Optional logger. If omitted, a package logger is used.
    """

    analysis_cfg = load_config(config) if not isinstance(config, AnalysisConfig) else config
    logger = logger or logging.getLogger("jwst_galaxy_analysis")

    logger.info("Reading CEERS catalog: %s", analysis_cfg.paths.ceers_catalog)
    ceers_table = read_fits_table(analysis_cfg.paths.ceers_catalog)
    logger.info("Loaded CEERS rows: %d", len(ceers_table))

    logger.info("Reading UNCOVER catalog: %s", analysis_cfg.paths.uncover_catalog)
    uncover_table = read_fits_table(analysis_cfg.paths.uncover_catalog)
    logger.info("Loaded UNCOVER rows: %d", len(uncover_table))

    ceers_samples = process_ceers(ceers_table, analysis_cfg, logger)
    uncover_samples = process_uncover(uncover_table, analysis_cfg, logger)
    samples = {**ceers_samples, **uncover_samples}

    products = plot_all(
        z2_ceers=ceers_samples[analysis_cfg.ceers.z2_name],
        z2_uncover=uncover_samples[analysis_cfg.uncover.z2_name],
        z3_ceers=ceers_samples[analysis_cfg.ceers.z3_name],
        z3_uncover=uncover_samples[analysis_cfg.uncover.z3_name],
        output_dir=analysis_cfg.paths.output_dir,
        cfg=analysis_cfg.plotting,
    )
    logger.info("Saved z2 plot: %s", products.z2_plot)
    logger.info("Saved z3 plot: %s", products.z3_plot)

    return samples, products
