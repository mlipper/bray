import os.path
from dynaconf import Dynaconf

# TODO Is this acceptable to insure base settings.toml file is found at runtime?
# E.g., when running pytest from the source project root directory
# E.g., when running from .zip, .tgz, .egg files
DEFAULT_DYNACONF_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_DYNACONF_SETTINGS_FILE = os.path.join(DEFAULT_DYNACONF_ROOT_PATH, 'settings.toml')

settings = Dynaconf(
    envvar_prefix="BRAY",
    settings_files=['settings.toml', '.secrets.toml', DEFAULT_DYNACONF_SETTINGS_FILE],
    environments=False,
    load_dotenv=True,
    dotenv_verbose=True,
)
