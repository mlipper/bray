"""bray: geocoding with NYC geoclient"""
from ._version import __version__

__all__ = [
    '__version__',
    'cli',
    'config',
    'errors',
    'main'
]
__author__ = 'mlipper'

import logging
import sys

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr
)
#logging.getLogger("chardet.charsetprober").disabled = True
logger = logging.getLogger(__name__)
