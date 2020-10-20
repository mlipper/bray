from collections import namedtuple
from pathlib import os, Path
import pytest

from . import FIXTURE_DIR, FIXTURE_ENV, PROJECTS_DIR

@pytest.fixture(scope="module")
def config_json():
    """Returns the path to the config.json file fixture as a str."""
    file_path_str = os.path.join(FIXTURE_DIR, 'config.json')
    assert Path(file_path_str).is_file()
    return file_path_str

@pytest.fixture(scope='module')
def example_config_ini():
    """Returns the path to the config.ini file from the example project as
       a str.
    """
    file_path_str = os.path.join(PROJECTS_DIR, 'example', 'config.ini')
    assert Path(file_path_str).is_file()
    return file_path_str

@pytest.fixture(scope='function')
def mock_env_app_id(monkeypatch):
    """Sets environment variable APP_ID to 'test_config' for the duration of
       the test function.
    """
    expected_value = FIXTURE_ENV['APP_ID']
    monkeypatch.setenv('APP_ID', expected_value)
    return expected_value

@pytest.fixture(scope='function')
def mock_env_app_key(monkeypatch):
    """Sets environment variable APP_KEY to 'S3CRETKEY' for the duration of
       the test function.
    """
    expected_value = FIXTURE_ENV['APP_KEY']
    monkeypatch.setenv('APP_KEY', expected_value)
    return expected_value