import argparse


class ArgsModel(argparse.Namespace):
    """Argparse output namespace schema to make linters work"""

    source: str
    version: str
    verbose: bool
    output: str
    convert: str
    convert_dir: str
    convert_file: str
    limit: int
    pretty: bool
