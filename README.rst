========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/bray/badge/?style=flat
    :target: https://readthedocs.org/projects/bray
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/mlipper/bray.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/mlipper/bray

.. |requires| image:: https://requires.io/github/mlipper/bray/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/mlipper/bray/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/mlipper/bray/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/mlipper/bray

.. |version| image:: https://img.shields.io/pypi/v/bray.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/bray

.. |wheel| image:: https://img.shields.io/pypi/wheel/bray.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/bray

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/bray.svg
    :alt: Supported versions
    :target: https://pypi.org/project/bray

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/bray.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/bray

.. |commits-since| image:: https://img.shields.io/github/commits-since/mlipper/bray/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mlipper/bray/compare/v0.1.0...master



.. end-badges

Simple batch API for geocoding in Python using Geoclient

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
