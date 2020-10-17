import os

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)

FIXTURE_ENV = {
    'APP_ID': 'test_config',
    'APP_KEY': 'S3CRETKEY'
}

PROJECTS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'projects',
)