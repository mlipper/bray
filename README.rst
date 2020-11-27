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

.. |commits-since| image:: https://img.shields.io/github/commits-since/mlipper/bray/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mlipper/bray/compare/v0.2.0...master



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


After not using python heavily for several years, I turned to the
Interwebs to familiarize myself with the modern Python ecosystem.
I found this article:

https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure

Thus, the initial commit of this project was generated using a library
written by the author:

https://github.com/ionelmc/cookiecutter-pylibrary

If I've understood correctly, this is an enhanced cookiecutter template
which differs from the original by using a directory named 'src' source
in root repository directory to contain a project's top-level module.

Following along with the article/library's design, using a "src folder"
requires that bray is packaged and installed so as to be available to
the target python runtime without too many shenanigans running running
tests.

To avoid messing with the system python/site packages and when using
tox, virtual environments are used (pipenv, virtualenv, etc.). Before
the tests (using pytest) will find bray, the following command must be
run (once) from the root directory in each new environment::

    pip install --editable .

To run all the tests run::

    pytest

or::

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
