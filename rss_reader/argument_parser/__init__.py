from .parser import ArgParser
from .models import ArgsModel

args = None

if not args:
    arg_parser = ArgParser()
    args = arg_parser.get_args()
