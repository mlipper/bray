
import os, os.path
import pytest
from bray import logger
from bray.cli import main
from bray.config import settings

def test_default_config():
    assert settings.geoclient is not None
    assert settings.geoclient.app_id is not None
    assert settings.geoclient.app_key is not None
    app_id = settings.geoclient.app_id
    app_key = settings.geoclient.app_key
    assert settings.geoclient.baseuri is not None
    assert settings.geoclient.search is not None
    assert settings.geoclient.search.params is not None
    assert settings.geoclient.search.params == ['input']
    assert settings.geoclient.search.query is not None
    assert settings.geoclient.search.query.to_dict() == {'app_id': app_id, 'app_key': app_key, 'returnRejections': 'true'}

def test_main():
    main([])
