.. highlight:: shell

=========
New index
=========

You need to fork index_calculator to you own github or do *sync fork* in your repository. Make a **new branch** from where you start with you changes.

Always start with a fresh new environemt and update xclim.

.. code-block:: console

    $ pip install --upgrade xclim



*Tipp 1: run index_calculation in the new environment for an easy index and one file before you start changing, just to check if the base you start from is fine*


*Tipp 2: you like to know where you are and if you are really in your forcked index_calculator $git remote show origin*

The index calculation is based on xclim_. Index calculator only calculated indices, which are available in xclim. If you need an index, which is not included in xclim, please integrate it in xclim not here.

If you like to add a new index, have a look if you can find a similar one, which is available already and copy it and adjust everything to your needs.

Please have a look at xclim for the metadata information.

First, if you need a new index, you need to edit two files:

.. code-block:: console

    $ cd index_calculator/tables
    $ input_vars.json
    $ metadata.json


Secondly you need to edit:

.. code-block:: console

    $ cd index_calculator
    $ _indices.py (edit)


The easiest way is, to copy an exsiting index which is similar to your new one and adjust it to your needs. The naming conventions can de found in xclim_ under indicators (not indices).

At last you need to perform a test:

.. code-block:: console

    $ pip install pytest


Please edit test_indices.py and execute

.. code-block:: console

    $ cd tests
    $ test_indices.py (edit)
    $ pytest (run)
    $ pytest -k GSL (if you only like to test it for GSL)


After you performed your test successfully, you install

.. code-block:: console

    $pip install -e .

the changed index_calculator in your environment. And make a calculation with index_calculation (gitlab) using this environment.




.. _xclim: https://github.com/Ouranosinc/xclim
