"""Main module"""
import argparse
import rss_reader.parsing as parsing
import logging as log
import sys

v = '1.2.1'


def parse():
    """This function gets all the args from command line and return args namespace"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source',
                        help='RSS URL',
                        type=str)
    parser.add_argument('--version',
                        help='Print version info',
                        action='version',
                        version='RssReader ' + v)
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


def main():
    """Main function that starts everything"""
    args = parse()
    if args.verbose:
        log.basicConfig(stream=sys.stdout, level=log.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log.info('Parsed args successfully')
    log.info('Parsing url ... ')
    soup = parsing.get_soup(args.source)
    log.info('Parsed successfully, printing')
    if args.json:
        parsing.print_json(args.limit, soup)
    else:
        parsing.print_regular(args.limit, soup)


if __name__ == '__main__':
    main()
