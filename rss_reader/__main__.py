"""Main module"""
import argparse
# import news
import rss_reader.news as news
# import caching
import rss_reader.caching as caching
# from config import version
from rss_reader.config import version
import logging as log
from sys import exit, stdout
from pathlib import Path
from os import path, mkdir


cache_path = ''


def get_arguments():
    """This function gets all the args from command line and return args namespace"""
    parser = argparse.ArgumentParser(
        description='Pure Python command-line RSS reader.')
    parser.add_argument('source',
                        help='RSS URL',
                        type=str)
    parser.add_argument('--version',
                        help='print version info',
                        action='version',
                        version='rss-reader {}'.format(version))
    parser.add_argument('--json',
                        help='print result as JSON in stdout',
                        action='store_true')
    parser.add_argument('--verbose',
                        help='output verbose status messages',
                        action='store_true')
    parser.add_argument('--limit',
                        help='limit news topics if this parameter provided',
                        type=int)
    parser.add_argument('--date',
                        type=str,
                        help='print cached news from provided date')
    parser.add_argument('--clear-cache',
                        help='clear news cache',
                        action='store_true')

    return parser.parse_args()


def print_cached_news_by_date(date, limit, json):
    """Function that prints cached news from given date
    in regular or in JSON formats
    depending on json variable value"""
    if json:
        log.info('Printing cached news as JSON')
        log.info('Limit is {}'.format(limit))
        ret = caching.print_cache_json(date, limit, cache_path)
    else:
        log.info('Printing cached news')
        log.info('Limit is {}'.format(limit))
        ret = caching.print_cache_regular(date, limit, cache_path)
    if ret is caching.CacheClear:
        log.info('Cache is empty')
    elif ret:
        log.info('Cached news printed successfully')
    elif not ret:
        log.info('There are no news from that date')
    else:
        print('Unknown error printing cached news')
        exit(1)


def print_news(news_dict, limit, json):
    """Function that prints news in regular or in JSON formats
    depending on json variable value"""
    if json:
        log.info('Printing news as JSON')
        log.info('Limit is {}'.format(limit))
        ret = news.print_json(news_dict)
    else:
        log.info('Printing news')
        log.info('Limit is {}'.format(limit))
        ret = news.print_regular(news_dict)
    if ret:
        log.info('News printed successfully')
    else:
        print('Unknown error printing news')
        exit(1)
    ret = caching.cache_news(news_dict, cache_path)
    if ret is caching.CacheClear:
        log.info('New cache file was created')
    elif ret:
        log.info('News cached successfully')
    else:
        print('Unknown error caching news')
        exit(1)


def main():
    """Main function that is called when running a package"""
    cache_dir = path.join(Path.home(), 'rss_reader')
    global cache_path
    cache_path = path.join(cache_dir, 'data.json')
    if not path.isdir(cache_dir):
        try:
            mkdir(cache_dir)
        except Exception as e:
            print('Error making a directory for cache at {}'.format(cache_dir))
            print(e)
            exit(1)
    args = get_arguments()
    if args.verbose:
        log.basicConfig(stream=stdout, level=log.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log.info('Received arguments successfully')
    log.info('Parsing url')
    log.info('Parsed successfully')
    soup = news.get_soup(args.source)
    if args.clear_cache:
        log.info('Clearing cache')
        ret = caching.clear_cache(cache_path)
        if ret is caching.CacheClear:
            log.info('Cache is already clear')
        elif ret:
            log.info('Cache cleared successfully')
        else:
            print('Unknown error clearing cache')
            exit(1)
    elif args.date:
        print_cached_news_by_date(args.date, args.limit, args.json)

    else:
        news_dict = news.get_items(args.limit, soup)
        print_news(news_dict, args.limit, args.json)


if __name__ == '__main__':
    main()
