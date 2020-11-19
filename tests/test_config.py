# import pytest
from bray.config import settings


class TestConfig:

    def test_defaults(self):
        assert settings.default.etl_dir == "etl"
        assert settings.default.data_dir == "etl/data"
        assert settings.default.input_file == "input.csv"
        assert settings.default.output_file == "output.csv"
        assert settings.default.job_file == "etl/job.toml"

    def test_geoclient_settings(self):
        assert settings.geoclient is not None
        assert settings.geoclient.app_id is not None
        assert settings.geoclient.app_key is not None
        app_id = settings.geoclient.app_id
        app_key = settings.geoclient.app_key
        assert settings.geoclient.baseuri is not None
        assert settings.geoclient.search is not None
        assert settings.geoclient.search.params is not None
        assert settings.geoclient.search.params == ["input"]
        assert settings.geoclient.search.query is not None
        assert settings.geoclient.search.query.to_dict() == {"app_id": app_id, "app_key": app_key, "returnRejections": "true"}

    def test_example_job(self):
        assert settings.job.name == "bray-example"
        assert settings.job.input.path == "input.csv"
        assert settings.job.input.file_system_id == "fs.in"

    def test_service(self):
        assert settings.service.types == ["db", "fs", "gc"]
