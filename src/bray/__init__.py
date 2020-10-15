__all__ = ['cli', 'config', 'errors', 'main']
__author__ = 'mlipper'
__version__ = '0.1.0'

import logging
import sys

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
#logging.getLogger("chardet.charsetprober").disabled = True
logger = logging.getLogger(__name__)
