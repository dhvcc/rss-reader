import argparse
from pathlib import Path


def directory(path: str) -> str:
    p = Path(path)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"directory {str(p)} does not exist")
    else:
        return path
