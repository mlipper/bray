from pathlib import os, Path
import pytest

from . import FIXTURE_DIR, FIXTURE_ENV

@pytest.fixture(scope="module")
def config_json():
    """Returns the path to the config.json file fixture as a str."""
    file_path_str = os.path.join(FIXTURE_DIR, 'config.json')
    assert Path(file_path_str).is_file()
    return file_path_str

@pytest.fixture(scope='function')
def mock_app_id_env(monkeypatch):
    """Sets environment variable APP_ID to 'test_config' for the duration of
       the test function.
    """
    monkeypatch.setenv('APP_ID', FIXTURE_ENV['APP_ID'])

@pytest.fixture(scope='function')
def mock_app_key_env(monkeypatch):
    """Sets environment variable APP_KEY to 'S3CRETKEY' for the duration of
       the test function.
    """
    monkeypatch.setenv('APP_KEY', FIXTURE_ENV['APP_KEY'])
