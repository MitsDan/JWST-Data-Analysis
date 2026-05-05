Project overview
================

This repository analyzes JWST CEERS and UNCOVER DR4 catalogs in two redshift
slices around z = 2.0 and z = 3.6. It is designed for reproducible comparison of
CEERS LePHARE stellar masses and observed NIRCam flux-derived magnitudes against
UNCOVER DR4 SPS stellar masses and rest-frame U-band AB magnitudes.

Primary outputs
---------------

* ``outputs/z2_stellar_mass_vs_u_mag.png``
* ``outputs/z3_stellar_mass_vs_u_mag.png``

Core design goals
-----------------

* Astropy Table FITS IO
* Configurable TOML science cuts and paths
* Explicit validation of required columns
* Isolated modules for CEERS, UNCOVER, photometry, cosmology, and plotting
* Unit-testable numerical helpers
* Console logging for all row-count checkpoints
