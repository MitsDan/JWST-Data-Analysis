Installation
============

Clone and install
-----------------

.. code-block:: bash

   git clone https://github.com/your-org/jwst-galaxy-analysis.git
   cd jwst-galaxy-analysis
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -e .

Install development dependencies
--------------------------------

.. code-block:: bash

   python -m pip install -e ".[dev]"

Place data files
----------------

Place the two FITS files in the default data directory:

.. code-block:: text

   data/ceers_cat_v1.0.fits
   data/UNCOVER_DR4_SPS_zspec_catalog.fits

Run the pipeline
----------------

.. code-block:: bash

   jwst-galaxy-analysis --config config/default.toml

or from a source checkout:

.. code-block:: bash

   python scripts/run_analysis.py --config config/default.toml

Run tests
---------

.. code-block:: bash

   pytest

Build documentation
-------------------

.. code-block:: bash

   sphinx-build -b html docs/source docs/build/html
