"""TOML-backed configuration for the JWST analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO
from importlib import resources

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]


@dataclass(frozen=True)
class PathsConfig:
    ceers_catalog: Path = Path("data/ceers_cat_v1.0.fits")
    uncover_catalog: Path = Path("data/UNCOVER_DR4_SPS_zspec_catalog.fits")
    output_dir: Path = Path("outputs")


@dataclass(frozen=True)
class CosmologyConfig:
    H0: float = 70.0
    Om0: float = 0.3
    Tcmb0: float = 2.725


@dataclass(frozen=True)
class CEERSConfig:
    redshift_column: str = "LP_Z_MED"
    z2_name: str = "z2_ceers"
    z2_min: float = 1.9
    z2_max: float = 2.1
    z2_flux_column: str = "F115W_FLUX"
    z2_flux_error_column: str = "F115W_FLUXERR_SE"
    z2_reference_redshift: float = 2.0
    z3_name: str = "z3_ceers"
    z3_min: float = 3.5
    z3_max: float = 3.7
    z3_flux_column: str = "F150W_FLUX"
    z3_flux_error_column: str = "F150W_FLUXERR_SE"
    z3_reference_redshift: float = 3.6
    mass_column: str = "LP_MASS_MED"
    mass_low_column: str = "LP_MASS_MED68_LOW"
    mass_high_column: str = "LP_MASS_MED68_HIGH"
    max_ab_mag_error: float = 10.0
    max_mass_error: float = 3.0


@dataclass(frozen=True)
class UNCOVERConfig:
    redshift_column: str = "z_spec"
    z2_name: str = "z2_uncover"
    z2_min: float = 1.5
    z2_max: float = 2.5
    z3_name: str = "z3_uncover"
    z3_min: float = 3.0
    z3_max: float = 4.0
    mass_column: str = "mstar_50"
    mass_low_column: str = "mstar_16"
    mass_high_column: str = "mstar_84"
    rest_u_column: str = "rest_U_50"
    rest_u_low_column: str = "rest_U_16"
    rest_u_high_column: str = "rest_U_84"


@dataclass(frozen=True)
class PlottingConfig:
    dpi: int = 300
    marker: str = "o"
    ceers_color: str = "#0072B2"
    uncover_color: str = "#D55E00"
    figsize: tuple[float, float] = (8.0, 6.5)
    z2_filename: str = "z2_stellar_mass_vs_u_mag.png"
    z3_filename: str = "z3_stellar_mass_vs_u_mag.png"


@dataclass(frozen=True)
class AnalysisConfig:
    paths: PathsConfig = field(default_factory=PathsConfig)
    cosmology: CosmologyConfig = field(default_factory=CosmologyConfig)
    ceers: CEERSConfig = field(default_factory=CEERSConfig)
    uncover: UNCOVERConfig = field(default_factory=UNCOVERConfig)
    plotting: PlottingConfig = field(default_factory=PlottingConfig)


def _resolve_path(path_value: str | Path, base_dir: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else (base_dir / path).resolve()


def _filter_kwargs(cls: type[Any], values: dict[str, Any]) -> dict[str, Any]:
    allowed = set(cls.__dataclass_fields__)  # type: ignore[attr-defined]
    return {key: value for key, value in values.items() if key in allowed}


def _load_toml(handle: BinaryIO) -> dict[str, Any]:
    return tomllib.load(handle)


def load_config(config_path: str | Path = "config/default.toml") -> AnalysisConfig:
    """Load pipeline configuration from a TOML file.

    Relative data and output paths are resolved relative to the repository root
    when loading ``config/default.toml`` from a source checkout. If that file is
    absent, the packaged ``default_config.toml`` is used and relative paths are
    resolved against the current working directory. This makes both editable
    installs and wheel installs usable.
    """

    requested = Path(config_path).expanduser()
    if requested.exists():
        path = requested.resolve()
        with path.open("rb") as handle:
            data = _load_toml(handle)
        repo_root = path.parent.parent if path.parent.name == "config" else path.parent
    elif str(config_path) == "config/default.toml":
        resource = resources.files("jwst_galaxy_analysis").joinpath("default_config.toml")
        with resource.open("rb") as handle:
            data = _load_toml(handle)
        repo_root = Path.cwd().resolve()
    else:
        raise FileNotFoundError(f"Configuration file does not exist: {requested.resolve()}")
    paths_raw = data.get("paths", {})
    paths = PathsConfig(
        ceers_catalog=_resolve_path(paths_raw.get("ceers_catalog", PathsConfig.ceers_catalog), repo_root),
        uncover_catalog=_resolve_path(
            paths_raw.get("uncover_catalog", PathsConfig.uncover_catalog), repo_root
        ),
        output_dir=_resolve_path(paths_raw.get("output_dir", PathsConfig.output_dir), repo_root),
    )

    plotting_raw = data.get("plotting", {})
    if "figsize" in plotting_raw:
        plotting_raw = dict(plotting_raw)
        plotting_raw["figsize"] = tuple(float(v) for v in plotting_raw["figsize"])

    return AnalysisConfig(
        paths=paths,
        cosmology=CosmologyConfig(**_filter_kwargs(CosmologyConfig, data.get("cosmology", {}))),
        ceers=CEERSConfig(**_filter_kwargs(CEERSConfig, data.get("ceers", {}))),
        uncover=UNCOVERConfig(**_filter_kwargs(UNCOVERConfig, data.get("uncover", {}))),
        plotting=PlottingConfig(**_filter_kwargs(PlottingConfig, plotting_raw)),
    )
