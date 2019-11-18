"""Main module"""
import argparse
import rss_reader.news as news
# import news
import rss_reader.caching as caching
# import caching
import logging as log
import sys

v = '1.3.0'


def parse():
    """This function gets all the args from command line and return args namespace"""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source',
                        help='RSS URL',
                        type=str)
    parser.add_argument('--version',
                        help='Print version info',
                        action='version',
                        version='rss-reader {}'.format(v))
    parser.add_argument('--json',
                        help='Print result as JSON in stdout',
                        action='store_true')
    parser.add_argument('--verbose',
                        help='Outputs verbose status messages',
                        action='store_true')
    parser.add_argument('--limit',
                        help='Limit news topics if this parameter provided',
                        type=int)
    parser.add_argument('--date',
                        type=str,
                        help='Prints cached news from provided date')
    return parser.parse_args()


def main():
    """Main function that starts everything"""
    args = parse()
    if args.verbose:
        log.basicConfig(stream=sys.stdout, level=log.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log.info('Parsed args successfully')
    log.info('Parsing url')
    soup = news.get_soup(args.source)
    log.info('Parsed successfully')
    if args.date:
        if args.json:
            log.info('Printing cached news as JSON')
            log.info('Limit is {}'.format(args.limit))
            ret = caching.print_cache_json(args.date, args.limit)
        else:
            log.info('Printing cached news')
            log.info('Limit is {}'.format(args.limit))
            ret = caching.print_cache_regular(args.date, args.limit)
        if ret is not None and type(ret) is EnvironmentError:
            log.info('Error during printing cache')
            log.info(ret)
        elif ret is True:
            log.info('Cached news printed successfully')
        else:
            log.info('No cached news from that date')

    else:
        news_dict = news.get_items(args.limit, soup)
        if args.json:
            log.info('Printing news as JSON ... ')
            log.info('Limit is {}'.format(args.limit))
            news.print_json(news_dict)
        else:
            log.info('Printing news ... ')
            log.info('Limit is {}'.format(args.limit))
            news.print_regular(news_dict)
        ret = caching.cache_news(news_dict)
        if ret is not None and type(ret) is FileNotFoundError:
            log.info(ret)
            log.info('New data file was created')
        elif ret is not None:
            log.info('Error during caching')
            log.info(ret)
        elif ret is True:
            log.info('News cached successfully')
        else:
            log.info('Unknown error')


if __name__ == '__main__':
    main()
