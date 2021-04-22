import sys

from pathlib import Path

from dynaconf import Dynaconf


# How to run the dynaconf CLI list command
#
# Assumptions:
#   Python's sys.path contains '<bray project root>/src'
#   Your shell's CWD is <bray project root>
#
# Command line:
#   $ cd path/to/<bray project root>
#   $ dynaconf -i bray.config.settings list --all
#   # If that fails, try:
#   $ ENV_FOR_DYNACONF=DEFAULT dynaconf -i bray.config.settings list --all
#
# TODO Is this acceptable to insure base settings.toml file is found at runtime?
# E.g., when running pytest from the source project root directory
# E.g., when running from .zip, .tgz, .egg files
# TODO Decide if using importlib.resources.path is better.
# See https://docs.python.org/3/library/importlib.html#importlib.resources.path
DEFAULT_DYNACONF_ROOT_PATH = Path(__file__).parent
DEFAULT_DYNACONF_SETTINGS_FILE = Path(DEFAULT_DYNACONF_ROOT_PATH) / 'settings.toml'
DEFAULT_ETL_DIR = Path.cwd() / 'etl'
DEFAULT_DATA_DIR = Path(DEFAULT_ETL_DIR) / 'data'
DEFAULT_JOB_SETTINGS_FILE = Path(DEFAULT_ETL_DIR) / 'job.toml'
# TODO: allow override of default log levels from cli
LOGLEVELS = {
    "console": "INFO",
    "file": "INFO"
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)-16s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': LOGLEVELS["console"],
            'stream': sys.stdout
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': LOGLEVELS["file"],
            'filename': 'bray.log',
            'mode': 'w',
            'encoding': 'utf-8',
            'maxBytes': 2000000,
            'backupCount': 3
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG'
    },
}


settings = Dynaconf(
    root_path=DEFAULT_DYNACONF_ROOT_PATH,
    envvar_prefix="BRAY",
    settings_files=['settings.toml', '.secrets.toml'],
    silent_errors=False,
    # settings_files=['settings.toml', '.secrets.toml', DEFAULT_DYNACONF_SETTINGS_FILE],
    includes=[str(DEFAULT_JOB_SETTINGS_FILE)],
    # environments=False,
    load_dotenv=True,
    dotenv_verbose=True,
)
