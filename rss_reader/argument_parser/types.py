import argparse
from pathlib import Path
from pathvalidate import validate_filename, ValidationError


def directory(path: str) -> str:
    p = Path(path)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"directory {str(p)} does not exist")
    else:
        return path


def filename(name: str) -> str:
    try:
        validate_filename(name)
    except ValidationError:
        raise argparse.ArgumentTypeError(f"filename {name} is invalid")
    return name


def unsigned_int(number: str):
    if int(number) < 0:
        raise argparse.ArgumentTypeError("limit must be positive")
    else:
        return number
