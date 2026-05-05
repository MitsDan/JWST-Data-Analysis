# JWST CEERS + UNCOVER Stellar Mass vs U-band Analysis

This repository provides a reproducible Python pipeline for comparing galaxy
stellar masses and rest-frame/observed U-band AB magnitudes in two JWST legacy
fields:

- **CEERS** using `ceers_cat_v1.0.fits` and LePHARE columns such as `LP_Z_MED`,
  `LP_MASS_MED`, `LP_MASS_MED68_LOW`, and `LP_MASS_MED68_HIGH`.
- **UNCOVER DR4** using `UNCOVER_DR4_SPS_zspec_catalog.fits` and columns such as
  `z_spec`, `mstar_50`, `mstar_16`, `mstar_84`, `rest_U_50`, `rest_U_16`, and
  `rest_U_84`.

The goal is to make the analysis easy to audit, rerun, configure, test, and
extend. The code uses `astropy.table.Table` for FITS catalog input, Astropy
units for nJy-to-AB magnitude conversion, and `astropy.cosmology.FlatLambdaCDM`
for distance modulus calculations.

## Scientific motivation

CEERS and UNCOVER provide deep JWST observations that probe galaxy formation and
evolution across cosmic time. This pipeline extracts two redshift slices near
`z = 2.0` and `z = 3.6`, estimates CEERS rest-frame U-band-like absolute
magnitudes from NIRCam fluxes, and compares them against UNCOVER rest-frame
U-band catalog quantities as a function of stellar mass.

## Relevant public references

- CEERS project page: https://ceers.github.io/
- CEERS MAST HLSP page: https://archive.stsci.edu/hlsp/ceers
- CEERS photometric and physical parameter catalog paper: https://arxiv.org/abs/2510.08743
- CEERS survey paper: https://arxiv.org/abs/2501.04085
- UNCOVER project page: https://jwst-uncover.github.io/
- UNCOVER DR4 data release page: https://jwst-uncover.github.io/DR4.html
- UNCOVER DR4 spectroscopic release on Zenodo: https://zenodo.org/records/13984100
- UNCOVER first spectra release paper: https://arxiv.org/abs/2408.03920
- UNCOVER first-look photometric/SPS catalog context: https://arxiv.org/abs/2301.02671

## What the pipeline does

1. Reads CEERS and UNCOVER FITS catalogs with `astropy.table.Table.read`.
2. Builds CEERS redshift masks from `LP_Z_MED`:
   - `z2_ceers`: `1.9 < z < 2.1`
   - `z3_ceers`: `3.5 < z < 3.7`
3. Removes CEERS rows with NaNs in the relevant flux column:
   - `F115W_FLUX` for `z2_ceers`
   - `F150W_FLUX` for `z3_ceers`
4. Extracts CEERS fluxes, flux errors, median stellar masses, and 16th/84th
   percentile stellar mass values.
5. Converts CEERS nJy fluxes and flux errors to AB magnitudes and AB magnitude
   errors with Astropy unit conversions.
6. Computes FlatLambdaCDM distance moduli at `z = 2.0` and `z = 3.6`, then
   derives CEERS absolute magnitudes.
7. Computes CEERS stellar mass lower and upper errors from percentile columns.
8. Removes CEERS points with AB magnitude error larger than `10.0` mag or either
   stellar-mass percentile error larger than `3.0` dex.
9. Builds UNCOVER redshift masks from `z_spec`:
   - `z2_uncover`: `1.5 < z < 2.5`
   - `z3_uncover`: `3.0 < z < 4.0`
10. Removes UNCOVER rows with NaNs in `mstar_50` or `rest_U_50`, then extracts
    median and percentile stellar masses and rest-frame U-band AB magnitudes.
11. Computes lower and upper error arrays for UNCOVER stellar masses and U-band
    magnitudes.
12. Produces two PNG errorbar plots:
    - `outputs/z2_stellar_mass_vs_u_mag.png`
    - `outputs/z3_stellar_mass_vs_u_mag.png`

## Repository structure

```text
jwst_galaxy_analysis_repo/
├── config/
│   └── default.toml
├── data/
│   └── .gitkeep
├── docs/
│   ├── Makefile
│   ├── make.bat
│   └── source/
│       ├── conf.py
│       ├── core.rst
│       ├── index.rst
│       ├── installation.rst
│       └── readme.rst
├── outputs/
│   └── .gitkeep
├── scripts/
│   └── run_analysis.py
├── src/
│   └── jwst_galaxy_analysis/
│       ├── __init__.py
│       ├── ceers.py
│       ├── cli.py
│       ├── config.py
│       ├── cosmology.py
│       ├── io.py
│       ├── logging_utils.py
│       ├── photometry.py
│       ├── pipeline.py
│       ├── plotting.py
│       ├── types.py
│       ├── uncover.py
│       └── validation.py
├── tests/
│   ├── test_config.py
│   ├── test_errors.py
│   └── test_validation.py
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Script and module overview

- `scripts/run_analysis.py`: thin script wrapper for running the complete pipeline.
- `jwst_galaxy_analysis.cli`: command-line interface and argument parsing.
- `jwst_galaxy_analysis.pipeline`: high-level orchestration of read, process, plot.
- `jwst_galaxy_analysis.config`: typed dataclass configuration and TOML loading.
- `jwst_galaxy_analysis.io`: FITS catalog input via `astropy.table.Table`.
- `jwst_galaxy_analysis.validation`: column and numerical validation helpers.
- `jwst_galaxy_analysis.photometry`: nJy-to-AB magnitude conversion and error propagation.
- `jwst_galaxy_analysis.cosmology`: FlatLambdaCDM construction and distance moduli.
- `jwst_galaxy_analysis.ceers`: CEERS redshift slicing, NaN filtering, magnitude and mass arrays.
- `jwst_galaxy_analysis.uncover`: UNCOVER redshift slicing, NaN filtering, rest-U and mass arrays.
- `jwst_galaxy_analysis.plotting`: color-blind-friendly Matplotlib errorbar plots.

## Installation

```bash
git clone https://github.com/your-org/jwst-galaxy-analysis.git
cd jwst-galaxy-analysis
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

For tests and documentation:

```bash
python -m pip install -e ".[dev]"
pytest
sphinx-build -b html docs/source docs/build/html
```

## Data placement

Place the FITS catalogs here by default:

```text
data/ceers_cat_v1.0.fits
data/UNCOVER_DR4_SPS_zspec_catalog.fits
```

You can override paths in `config/default.toml` or pass a different config file:

```bash
jwst-galaxy-analysis --config config/default.toml
```

or:

```bash
python scripts/run_analysis.py --config config/default.toml
```

## Configuration

All science cuts, file paths, cosmology values, plot styling, and output filenames
live in `config/default.toml`. This avoids hard-coding assumptions in the source
code and makes future re-runs traceable.

## Logging

The pipeline writes structured console logs showing:

- how many rows were loaded,
- how many galaxies pass each redshift mask,
- how many rows are removed because of missing flux/mass/magnitude values,
- how many final galaxies remain after quality cuts,
- where output plots are saved.

Use `--log-level DEBUG` for more detailed diagnostics.

## Tests

The repository includes lightweight unit tests for:

- TOML config loading and overrides,
- mass and magnitude percentile error propagation,
- required-column validation.

Run:

```bash
pytest
```

## Documentation

Sphinx source files are in `docs/source`. Build HTML docs with:

```bash
sphinx-build -b html docs/source docs/build/html
```

or from `docs/`:

```bash
make html
```

## License

This repository is released under the MIT License. Commercial use, modification,
distribution, and private use are permitted subject to the terms in `LICENSE`.
