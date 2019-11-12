import argparse


def parse():
    """This function gets all the args from command line and return args namespace"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source',
                        help='RSS URL',
                        type=str)
    parser.add_argument('--version',
                        help='Print version info',
                        action='version',
                        version='RssReader 1.1.0')
    parser.add_argument('--json',
                        help='Print result as JSON in stdout',
                        action='store_true')
    parser.add_argument('--verbose',
                        help='Outputs verbose status messages',
                        action='store_true')
    parser.add_argument('--limit',
                        help='Limit news topics if this parameter provided',
                        type=int)
    return parser.parse_args()


args = parse()
if args.verbose:
    print("Parsed args succesfully")
    print("Requesting rss from url ... ")

print(args)
