from os import mkdir
from os.path import isdir, join
from pathlib import Path

BASE_DIR = join(str(Path.home()), "rss_reader")
if not isdir(BASE_DIR):
    mkdir(BASE_DIR)

OUTPUT_DIR = join(BASE_DIR, "output")
if not isdir(OUTPUT_DIR):
    mkdir(OUTPUT_DIR)

MODULE_DIR = Path(__file__).parent.parent
