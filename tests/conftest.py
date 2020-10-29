import pytest

from . import FIXTURE_ENV, PROJECTS_DIR

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