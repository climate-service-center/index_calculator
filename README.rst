============================================================================================
Calculate climate indicators with standardized project-specific attributes: index_calculator
============================================================================================

+----------------------------+-----------------------------------------------------+
| Versions                   | |pypi|                                              |
+----------------------------+-----------------------------------------------------+
| Documentation and Support  | |docs| |versions|                                   |
+----------------------------+-----------------------------------------------------+
| Open Source                | |license| |zenodo|                                  |
+----------------------------+-----------------------------------------------------+
| Coding Standards           | |black| |pre-commit|                                |
+----------------------------+-----------------------------------------------------+
| Development Status         | |status| |build| |coveralls|                        |
+----------------------------+-----------------------------------------------------+

Python index_calculator is an xclim wrapper to calculate climate indicators from CMORized netCDF files.

Documentation
-------------
The official documentation is at https://index_calculator.readthedocs.io/

Features
--------
* Calculate climate indices via xclim_.
* Write standardized netCDF attributes.
* Write on disk with a project-specific output file name.

Available projects
------------------
You can calculate climate indicators using index_calculator with the projects listed in the table below.

+--------------------+--------------+
| CMIP               | CMIP5, CMIP6 |
+--------------------+--------------+
| CORDEX             | CORDEX       |
+--------------------+--------------+
| Observational data | E-OBS, HYRAS |
+--------------------+--------------+
| Reanalysis data    | ERA5         |
+--------------------+--------------+

Installation
------------

You can install the package directly with pip:

.. code-block:: console

     pip install index_calculator

If you want to contribute, I recommend cloning the repository and installing the package in development mode, e.g.

.. code-block:: console

    git clone https://github.com/ludwiglierhammer/index_calculator
    cd index_calculator
    pip install -e .

This will install the package but you can still edit it and you don't need the package in your :code:`PYTHONPATH`


Requirements
------------

* python3.6 or higher

* xclim

* numpy

* pandas

* xarray

* cf_xarray

* cftime


Contact
-------
In cases of any problems, needs or wishes do not hesitate to contact:

ludwig.lierhammer@hereon.de

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _xclim: https://xclim.readthedocs.io/en/latest/

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. |pypi| image:: https://img.shields.io/pypi/v/index_calculator.svg
        :target: https://pypi.python.org/pypi/index_calculator
        :alt: Python Package Index Build

.. |docs| image:: https://readthedocs.org/projects/index_calculator/badge/?version=latest
        :target: https://index-calculator.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. |versions| image:: https://img.shields.io/pypi/pyversions/index_calculator.svg
        :target: https://pypi.python.org/pypi/index_calculator
        :alt: Supported Python Versions

.. |license| image:: https://img.shields.io/github/license/ludwiglierhammer/index_calculator.svg
        :target: https://github.com/ludwiglierhammer/index_calculator/blob/master/LICENSE
        :alt: License

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black
        :alt: Python Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ludwiglierhammer/index_calculator/master.svg
   :target: https://results.pre-commit.ci/latest/github/ludwiglierhammer/index_calculator/master
   :alt: pre-commit.ci status

.. |status| image:: https://www.repostatus.org/badges/latest/active.svg
        :target: https://www.repostatus.org/#active
        :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.

.. |build| image:: https://github.com/ludwiglierhammer/index_calculator/actions/workflows/ci.yml/badge.svg
        :target: https://github.com/ludwiglierhammer/index_calculator/actions/workflows/ci.yml
        :alt: Build Status

.. |coveralls| image:: https://codecov.io/gh/ludwiglierhammer/index_calculator/branch/master/graph/badge.svg
	:target: https://codecov.io/gh/ludwiglierhammer/index_calculator
	:alt: Coveralls

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7762679.svg
        :target: https://doi.org/10.5281/zenodo.7762679
 	:alt:   DOI
