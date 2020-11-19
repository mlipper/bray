from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / 'data'

FIXTURE_ENV = {
    'APP_ID': 'test_config',
    'APP_KEY': 'S3CRETKEY'
}

ETL_DIR = Path.cwd() / 'etl'

ETL_DATA_DIR = ETL_DIR / 'data'


def getfile(filename):
    return Path(FIXTURE_DIR) / filename
