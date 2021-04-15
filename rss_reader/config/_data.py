"""Data config module which parses cli args, ini configs and env"""
from configparser import ConfigParser
from os import environ
from os.path import join
from pathlib import Path
from typing import Union

from rss_reader.argument_parser import ArgParser, ArgsModel, types

from ._base import OUTPUT_DIR


class DataConfig:
    def __init__(self):
        self.source: Union[None, str] = None
        self.verbose: Union[None, bool] = None
        self.output: Union[None, str] = None
        self.convert: Union[None, str] = None
        self.convert_dir: Union[None, str] = None
        self.convert_file: Union[None, str] = None
        self.limit: Union[None, int] = None
        self.pretty: Union[None, bool] = None

    def load(
        self,
        arguments_: ArgsModel,
        local_config_: ConfigParser,
        global_config_: ConfigParser,
        environment_,
    ):
        self.load_cli(arguments_)
        self.load_ini(local_config_)
        self.load_environ(environment_)
        self.load_ini(global_config_)

        self.set_defaults()

    def load_cli(self, arguments: ArgsModel):
        self.source = arguments.source
        self.verbose = arguments.verbose
        self.output = arguments.output
        self.convert = arguments.convert
        self.convert_dir = arguments.convert_dir
        self.convert_file = arguments.convert_file
        self.limit = arguments.limit
        self.pretty = arguments.pretty

    def load_ini(self, config: ConfigParser):
        if "rss-reader" not in config.sections():
            return

        if not self.output and config["rss-reader"].get("OUTPUT"):
            self.output = types.output_enum(config["rss-reader"]["OUTPUT"])

        if not self.convert and config["rss-reader"].get("CONVERT"):
            self.convert = types.convert_enum(config["rss-reader"]["CONVERT"])

        if not self.convert_dir and config["rss-reader"].get("CONVERT_DIR"):
            self.convert_dir = types.directory(config["rss-reader"]["CONVERT_DIR"])

        if not self.convert_file and config["rss-reader"].get("CONVERT_FILE"):
            self.convert_file = types.filename(config["rss-reader"]["CONVERT_FILE"])

    def load_environ(self, environment):
        if self.output is None:
            self.output = environment.get("RSS_READER_OUTPUT")

        if self.convert is None:
            self.convert = environment.get("RSS_READER_CONVERT")

        if self.convert_dir is None:
            self.convert_dir = environment.get("RSS_READER_CONVERT_DIR")

        if self.convert_file is None:
            self.convert_file = environment.get("RSS_READER_CONVERT_FILE")

    def set_defaults(self):
        if self.convert_dir is None:
            self.convert_dir = OUTPUT_DIR
        if self.output is None:
            self.output = "console"
        if self.convert is None:
            self.convert = "none"
        if self.pretty is None:
            self.pretty = False

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})>"
        )


# cli
arg_parser = ArgParser()
# local ini
local_config = ConfigParser()
local_config.read(".rss-reader")
# global ini
global_config = ConfigParser()
global_config.read(join(str(Path.home()), ".rss-reader"))

data_config = DataConfig()
data_config.load(
    arguments_=arg_parser.get_args(),
    local_config_=local_config,
    environment_=environ,
    global_config_=global_config,
)
