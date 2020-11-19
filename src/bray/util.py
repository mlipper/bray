from pathlib import Path


def pathify(string, prepend_working_dir=True, silent_errors=False):
    path = Path(string)
    if path.exists():
        return path
    if path.is_absolute() and silent_errors:
        return path
    absolute_path = Path.cwd() / path
    if absolute_path.exists():
        return absolute_path
    # Given relative path does not exist, even with CWD prepended
    if not silent_errors:
        raise FileNotFoundError(f'Path "{str(path)}" built from string "{string}" does not exist.')
    # Return non-existent relative path
    return path
