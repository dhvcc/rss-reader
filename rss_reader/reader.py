from os import rmdir

from rss_reader.imports import json
from requests import get

from rss_reader.converter import Converter
from rss_reader.parser import Parser
from rss_reader.parser.models import RSSFeed
from rss_reader.printer import Printer
from rss_reader.argument_parser import args, ArgsModel, arg_parser
from .config import CACHE_DIR


class Reader:
    def __init__(self):
        self.source = args.source
        self.args: ArgsModel = args

        self.rss_response = None
        self.rss = None
        self.rss_raw = None

    def get_parser(self):
        if self.args.date:
            # If --date then get feed from cache
            # And slice if limit is set
            self.rss_raw = json.loads(open(CACHE_DIR, f"{self.args.date}.json").read())
            self.rss = RSSFeed(**self.rss_raw)
            if self.args.limit is not None:
                self.rss.feed = self.rss.feed[:self.args.limit]
        else:
            # TODO: Add file as a source support
            self.rss_response = get(self.source)
        return Parser(self.rss_response.content, self.args.limit if self.args.limit else None)

    @staticmethod
    def clear_cache():
        rmdir(CACHE_DIR)

    def cache_news(self):
        # TODO: enable caching
        ...

    def start(self):
        """Setup and print"""
        if self.args.clear_cache:
            # If --clear-cache then clear and exit
            self.clear_cache()
            return
        elif not self.args.date and not self.args.source:
            # Only --date and --clear-cache should ignore source
            # Therefore, if no source is provided print help and exit
            arg_parser.print_help()
            return
        else:
            # If everything's ok parse the feed
            parser = self.get_parser()
            self.rss: RSSFeed = parser.parse()
            self.rss_raw = parser.raw_data

        self.print()

        if not self.args.dont_cache:
            self.cache_news()

    def print(self):
        """
        Call print and convert
        getattr returns (attribute) method depending on arg value
        """
        printer = Printer(self.rss, self.rss_raw)
        getattr(printer, self.args.output)()

        converter = Converter(self.rss, self.args.convert_dir,
                              self.args.convert_file, self.rss_raw)
        getattr(converter, self.args.convert)()
