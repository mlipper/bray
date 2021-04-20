"""
 Module that contains the command line app. Why does this file exist, and why not put this in __main__? You might be tempted to import
 things from __main__ later, but that will cause problems: the code will get executed twice: - When you run `python -mbray` python will
 execute ``__main__.py`` as a script. That means there won't be any
    ``bray.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``bray.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

from bray import etl, logger, service


def get_argument_parser():
    """Create an ArgumentParser customized for use with the Bonobo ETL framework."""
    parser = argparse.ArgumentParser(description="Invoke bray to geocode New York City location data with geoclient.")
    parser.add_argument("--configfile", "-c", action="store_true", default=None, help="Path to bray configuration file.")
    parser.add_argument("--limit", "-l", type=int, default=None, help="If set, limits the number of processed lines.")
    parser.add_argument("--print", "-p", action="store_true", default=False, help="If set, pretty prints before writing to output file.")
    return parser


def main(args=None):
    logger.debug("Arguments to main(): %s.", args)
    registry = service.Registry()
    job = registry.get_job()
    logger.info("Running %s.", job)
    etl.run(job, get_argument_parser())
    logger.info("%s complete.", job)
