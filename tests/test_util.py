import pytest

from pathlib import Path
from contextlib import nullcontext as does_not_raise
from bray.util import pathify

test_data = [
    ("etl", {"prepend_working_dir": True, "silent_errors": False}, Path("etl"), does_not_raise()),
    ("fake", {"prepend_working_dir": True, "silent_errors": False}, None, pytest.raises(FileNotFoundError)),
    ("fake2", {"prepend_working_dir": True, "silent_errors": True}, Path("fake2"), does_not_raise()),
]


@pytest.mark.parametrize("path_string,kwargs,expected,exception_context", test_data)
def test_pathify(path_string, kwargs, expected, exception_context):
    with(exception_context):
        actual = pathify(path_string, **kwargs)
        assert actual == expected
