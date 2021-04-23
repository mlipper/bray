import logging


from bray import _bray_logging
from bray.config import LOGGING, LOGLEVELS


logger = logging.getLogger(__name__)


def test_default_module_logging():
    conf, levels = _bray_logging
    assert conf is LOGGING
    assert levels is LOGLEVELS


def test_main():
    # TODO test me!
    logger.warning("TODO: test me!!")
    # main([])
