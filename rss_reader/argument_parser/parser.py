import argparse
from .types import directory
from rss_reader.config import OUTPUT_DIR


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Pure Python command-line RSS reader.",
            add_help=True)
        self.parser.add_argument("source", help="RSS source FILE/URL. Ignored if --date argument is passed", nargs="?",
                                 type=str)
        self.parser.add_argument("--version", help="print version info",
                                 action="version",
                                 version="rss-reader {}".format(globals()["__version__"]))
        self.parser.add_argument("--verbose", help="output verbose status messages",
                                 action="store_true")
        self.parser.add_argument("-d", "--date", help="print cached news from provided date in %%Y%%m%%d format",
                                 type=str)
        self.parser.add_argument("--clear-cache", help="clear news cache",
                                 action="store_true")
        self.parser.add_argument("-o", "--output", help="console output type",
                                 choices=["console", "colorized", "json", "none"],
                                 default="console",
                                 type=str)
        self.parser.add_argument("-c", "--convert", help="convert feed and save as a file",
                                 choices=["json", "html", "pdf", "fb2", "epub"],
                                 default="none",
                                 type=str)
        self.parser.add_argument("--convert-dir", help="convert output dir path instead of {home}/rss_reader/output",
                                 default=OUTPUT_DIR,
                                 type=directory)
        self.parser.add_argument("--convert-file", help="convert output filename",
                                 type=str)
        self.parser.add_argument("--dont-cache", help="don't cache the output",
                                 action="store_true")
        self.parser.add_argument("-l", "--limit", help="limit news topics if this parameter is provided",
                                 type=int)

    def print_help(self):
        """Shortcut for parser.print_help"""
        self.parser.print_help()

    def get_args(self):
        return self.parser.parse_args()
