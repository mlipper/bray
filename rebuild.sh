#!/bin/bash -eux

rm -rf build
rm -rf src/*.egg-info

tox -e check

python setup.py clean --all sdist bdist_wheel
