Installation
============

Clone and install
-----------------

.. code-block:: bash

   git clone https://github.com/MitsDan/JWST-Data-Analysis.git
   cd JWST-Data-Analysis
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

Place the CEERS catalog FITS file here by default (The UNCOVER catalog FITS file is already located in the /data folder):

.. code-block:: text

   data/ceers_cat_v1.0.fits

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
