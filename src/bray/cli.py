"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mbray` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``bray.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``bray.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
from . import logger
from bray import etl

def main(args=None):
    parser = argparse.ArgumentParser(description='Invoke bray to geocode New York City location data with geoclient.')
    parser.add_argument(
                        'configfile',
                        action='store_true',
                        help='Path to bray configuration file.'
    )
    parser = etl.get_argument_parser(parser)
    args = parser.parse_args(args=args)
    #args = args[1:]
    logger.info('Using arguments %s.', args)
