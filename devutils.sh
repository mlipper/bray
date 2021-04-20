#!/bin/bash -eux

SOURCE="${BASH_SOURCE[0]}"

while [ -h "$SOURCE" ]; do # resolve until $SOURCE is not a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative
                                               # symlink, need to resolve it
                                               # relative to the path where
                                               # the symlink file was located
done

DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

alias virtenv=pyenv
alias virtpip=pip3
alias virtpy=python3

VIRTENV="$(virtenv version)"
VIRTPIP="$(virtpip --version)"
VIRTPY="$(virtpy --version)"

echo "VIRTENV=${VIRTENV}"
echo "VIRTPIP=${VIRTPIP}"
echo "VIRTPY=${VIRTPY}"

function devinit(){
    echo "[bray] VIRTENV=${VIRTENV}"
    echo "[bray] VIRTPIP=${VIRTPIP}"
    echo "[bray] VIRTPY=${VIRTPY}"
    pushd "${DIR}" >/dev/null
    echo    "[bray] base directory: $(pwd)"
    echo -n "[bray] python version: " && virtpy --version
    echo -n "[bray]    pip version: " && virtpip --version
    echo
    echo pip install --upgrade pip setuptools
    echo pip install tox tox-pyenv
    popd >/dev/null
}

function devclean(){
    pushd "${DIR}"
    echo $(pwd)
    echo rm -rf dist/
    echo rm -rf htmlcov/
    echo rm -f coverage.xml
    echo rm -rf src/*.egg-info
    echo python setup.py clean --all sdist bdist_wheel
    popd
}



unalias virtenv
unalias virtpip
unalias virtpy

