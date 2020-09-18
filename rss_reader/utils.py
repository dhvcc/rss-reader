import argparse
from pathlib import Path


def file_path(path: str) -> str:
    p = Path(path)
    if not p.parent.is_dir():
        raise argparse.ArgumentTypeError(f"directory {str(p.parent)} does not exist")
    else:
        return path
