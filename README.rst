================
index_calculator
================

.. image:: https://github.com/ludwiglierhammer/index_calculator/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/ludwiglierhammer/index_calculator/actions/workflows/ci.yml

.. image:: https://codecov.io/gh/ludwiglierhammer/index_calculator/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ludwiglierhammer/index_calculator

.. image:: https://img.shields.io/pypi/v/index_calculator.svg
    :target: https://pypi.python.org/pypi/index_calculator

.. image:: https://readthedocs.org/projects/index_calculator/badge/?version=latest
    :target: https://index-calculator.readthedocs.io/en/latest/?version=latest
    :alt: Documentation Status

.. image:: https://results.pre-commit.ci/badge/github/ludwiglierhammer/index_calculator/master.svg
   :target: https://results.pre-commit.ci/latest/github/ludwiglierhammer/index_calculator/master
   :alt: pre-commit.ci status

Python index_calculator is an xclim wrapper to calculate climate indices from CMORized netCDF files.


* Free software: MIT license
* Documentation: https://index-calculator.readthedocs.io.


Features
--------

* Calculate climate indices via xclim.
* Write standardized netCDF attributes.
* Write on disk with a project-specific output file name.

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

* numpy

* pandas

* xarray

* xclim


Contact
-------
In cases of any problems, needs or wishes do not hesitate to contact:

ludwig.lierhammer@hereon.de

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
