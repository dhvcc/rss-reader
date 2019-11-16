import argparse
import url_parse
import logging as log
import requests
import sys

v = '1.1.0'


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
        log.basicConfig(level=log.INFO)
    log.info('Parsed args successfully')
    log.info('Parsing url ... ')
    soup = url_parse.get_soup(args.source)
    log.info('Parsed successfully, printing')
    url_parse.print_header(soup)
    url_parse.print_items(args.limit, url_parse.get_items(soup))
    # with open('f.xml', 'wb') as f:
    #    f.write(requests.get(args.source).content)
    # exit()


if __name__ == '__main__':
    main()
