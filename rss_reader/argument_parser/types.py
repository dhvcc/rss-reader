"""Custom types for argparse"""
import argparse
from pathlib import Path

from pathvalidate import ValidationError, validate_filename


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


def unsigned_int(number: str) -> int:
    num = int(number)
    if num < 0:
        raise argparse.ArgumentTypeError("limit must be positive")
    return num


def output_enum(output: str) -> str:
    enum = ("console", "colorized", "json", "none")
    if output not in enum:
        raise argparse.ArgumentTypeError(f"output not in {enum}")
    return output


def convert_enum(convert: str) -> str:
    enum = ("json", "html", "pdf", "epub")
    if convert not in enum:
        raise argparse.ArgumentTypeError(f"convert not in {enum}")
    return convert
