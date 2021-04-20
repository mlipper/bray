========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/bray/badge/?style=flat
    :target: https://bray.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/mlipper/bray.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/mlipper/bray

.. |codecov| image:: https://codecov.io/gh/mlipper/bray/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/mlipper/bray

.. |commits-since| image:: https://img.shields.io/github/commits-since/mlipper/bray/v0.2.1.svg
    :alt: Commits since latest release
    :target: https://github.com/mlipper/bray/compare/v0.2.1...master



.. end-badges

Simple ETL app for geocoding with NYC Geoclient

* Free software: Apache Software License 2.0

Installation
============

::

    pip install bray

You can also install the in-development version with::

    pip install https://github.com/mlipper/bray/archive/master.zip


Documentation
=============


https://bray.readthedocs.io/


Development
===========

Install tox:

    pip install tox

If you use pyenv, install tox-pyenv:

    pip install tox-pyenv

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
