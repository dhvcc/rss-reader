import logging
from pathlib import Path

from requests import exceptions, get
from rss_parser import Parser
from rss_parser.models import RSSFeed

from rss_reader.config import MODULE_DIR, data_config
from rss_reader.converter import Converter
from rss_reader.printer import Printer

logger = logging.getLogger("rss-reader")


class Reader:
    def __init__(self):
        self.config = data_config

        self.source = self.config.source

        self.rss_response = None
        self.rss = None
        self.rss_raw: dict = {}

    def get_parser(self):
        source_path = Path(self.source)
        if source_path.is_file():
            logger.info("Source is a file")
            try:
                with open(self.source) as file:
                    return Parser(file.read(), self.config.limit)
            except Exception as e:
                logger.warning("Source is invalid")
                logger.exception(e)
                raise e
        else:
            logger.info("Source is not a file, should be a link")
            try:
                self.rss_response = get(self.source)
                return Parser(self.rss_response.content, self.config.limit)
            except exceptions.RequestException as e:
                logger.warning("Source is invalid")
                logger.exception(e)
                raise e

    def enable_verbose(self):
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s (%(funcName)s) = %(message)s"
        )

        logger_ = logging.getLogger("rss-reader")
        logger_.setLevel("DEBUG")
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)

        logger_.addHandler(s_handler)

        logger_.info("Enabled verbose mode")
        logger.debug(self.config)
        logger.debug(f"Module dir {MODULE_DIR}")

    def start(self):
        """Setup and print"""
        if self.config.verbose:
            self.enable_verbose()
        else:
            logger.addHandler(logging.NullHandler())
            logger.propagate = False

        parser = self.get_parser()
        self.rss: RSSFeed = parser.parse()
        self.rss_raw = parser.raw_data

        self.print()

    def print(self):
        """
        Call print and convert
        getattr returns (attribute) method depending on arg value
        """
        printer = Printer(self.rss, self.rss_raw)
        logger.info(f"Calling printer.{self.config.output}()")
        getattr(printer, self.config.output)()

        converter = Converter(
            self.rss, self.config.convert_dir, self.config.convert_file, self.rss_raw
        )
        logger.info(f"Calling converter.{self.config.convert}()")
        getattr(converter, self.config.convert)()
