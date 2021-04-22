"""bray: geocoding with NYC geoclient"""
from ._version import __version__


__all__ = [
    '__version__',
    'cli',
    'config',
    'errors',
    'etl',
    'geoclient',
    'service',
    'util'
]
__author__ = 'mlipper'

import logging
import logging.config
import logging.handlers

from bray.config import LOGGING, LOGLEVELS


def configure_logging(conf=LOGGING, levels=LOGLEVELS):
    handlers = conf['handlers']
    for name, props in handlers.items():
        if name in levels.keys():
            print(f"name={name}")
            print(f"props={props}")
            props['level'] = levels[name]
    logging.config.dictConfig(conf)
    # Return conf, levels for easier testing
    return conf, levels


def _init():
    conf, __ = configure_logging()
    logger = logging.getLogger(__name__)
    logger.debug("%s logger configured by %s using:", __name__, "logging.config.dictConfig")
    logger.debug(conf)


_init()
