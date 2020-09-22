"""Cleaner config PR's are welcomed"""
from os import mkdir
from os.path import join, isdir
from pathlib import Path

###############
# Base config #
###############

BASE_DIR = join(str(Path.home()), 'rss_reader')

OUTPUT_DIR = join(BASE_DIR, 'output')
if not isdir(OUTPUT_DIR):
    mkdir(OUTPUT_DIR)

MODULE_DIR = Path(__file__).parent.parent
