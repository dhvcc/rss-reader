import argparse
from .types import directory, unsigned_int, filename
from rss_reader.config import OUTPUT_DIR, MODULE_DIR
from os.path import join

pkg_info = {}

with open(join(MODULE_DIR, "__version__.py")) as f:
    """Executing init to set __version__ value"""
    exec(f.read(), pkg_info)


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Pure Python command-line RSS reader.",
            add_help=True)
        self.parser.add_argument("source", help="RSS source URL or a file path",
                                 type=str)
        self.parser.add_argument("--version", help="print version info",
                                 action="version",
                                 version=f"rss-reader {pkg_info['__version__']}")
        self.parser.add_argument("--verbose", help="output verbose status messages",
                                 action="store_true")
        self.parser.add_argument("-o", "--output", help="console output type",
                                 choices=["console", "colorized", "json", "none"],
                                 type=str)
        self.parser.add_argument("-c", "--convert", help="convert feed and save as a file",
                                 choices=["json", "html", "pdf", "epub"],
                                 type=str)
        self.parser.add_argument("--convert-dir", help=f"convert output dir path instead of {OUTPUT_DIR}",
                                 type=directory)
        self.parser.add_argument("--convert-file", help="convert output filename",
                                 type=filename)
        self.parser.add_argument("-l", "--limit", help="limit news topics if this parameter is provided",
                                 type=unsigned_int)

    def print_help(self):
        """Shortcut for parser.print_help"""
        self.parser.print_help()

    def get_args(self):
        return self.parser.parse_args()
