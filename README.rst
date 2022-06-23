================
index_calculator
================

.. image:: https://github.com/ludwiglierhammer/index_calculator/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/ludwiglierhammer/index_calculator/actions/workflows/ci.yml

.. image:: https://codecov.io/gh/ludwiglierhammer/index_calculator/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/ludwiglierhammer/index_calculator

.. image:: https://readthedocs.org/projects/index_calculator/badge/?version=latest
    :target: https://index-calculator.readthedocs.io/en/latest/?version=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ludwiglierhammer/index_calculator/shield.svg
    :target: https://pyup.io/repos/github/ludwiglierhammer/index_calculator/
    :alt: Updates

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

You can install the package directly from github using pip:

.. code-block:: console

     pip install git+https://github.com/ludwiglierhammer/index_calculator

If you want to contribute, I recommend cloning the repository and installing the package in development mode, e.g.

.. code-block:: console

    git clone https://github.com/ludwiglierhammer/index_calculator.git
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
