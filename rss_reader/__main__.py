"""Main module"""
import argparse
import rss_reader.news as news
import rss_reader.caching as caching
from rss_reader.config import version
import rss_reader.converting as converting
import logging as log
from sys import exit, stdout
from pathlib import Path
from os import path, mkdir


# before commit
# pip3 install -e ., venv
# pip3 freeze > requirements.txt
# update Readme version
# update config version
# pycodestyle
# readme usage


# tests
# colorize


def get_arguments():
    """This function gets all the args from command line and return args namespace"""
    parser = argparse.ArgumentParser(
        description='Pure Python command-line RSS reader.',
        add_help=True)
    parser.add_argument('source',
                        help='RSS URL',
                        nargs='*',
                        # default=' ',
                        metavar='source',
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
                        help='print cached news from provided date in %%Y%%m%%d format, also affects --to-* arguments'
                             ' (no need to provide source argument)')
    parser.add_argument('--clear-cache',
                        help='clear news cache (no need to provide source argument)',
                        action='store_true')
    parser.add_argument('--to-epub',
                        action='store_true',
                        help='convert news to .epub format and make a new file called news.epub')
    parser.add_argument('--to-fb2',
                        action='store_true',
                        help='convert news to .fb2 format and make a new file called news.fb2')
    parser.add_argument('--to-html',
                        action='store_true',
                        help='convert news to .html format and make a new file called news.html')
    parser.add_argument('--to-pdf',
                        action='store_true',
                        help='convert news to .pdf format and make a new file called news.pdf')

    return parser.parse_args()


def parse_date_argument(args, reader_dir, cache_path):
    """Function that parses date argument prints or converts cached news from given date
    depending on args variable values"""
    cached_news_dict = caching.get_cached_news(args.date, args.limit, cache_path)
    if cached_news_dict is caching.CacheCleanError:
        log.info('Cache is empty')
        return
    elif not cached_news_dict:
        log.info('There are no news from that date')
        return

    if args.json:
        log.info('Printing cached news as JSON')
        log.info('Limit is {}'.format(args.limit))
        if news.print_json(cached_news_dict):
            log.info('Cached news printed successfully')
        else:
            print('Unknown error printing cached news')
            exit(1)
    elif args.to_html:
        log.info('Converting cached news to html')
        if converting.to_html(cached_news_dict, reader_dir):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    elif args.to_pdf:
        log.info('Converting cached news to pdf')
        if converting.to_pdf(cached_news_dict, reader_dir):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    elif args.to_fb2:
        log.info('Converting cached news to fb2')
        if converting.to_fb2(cached_news_dict, reader_dir, 'Cache'):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    elif args.to_epub:
        log.info('Converting cached news to epub')
        if converting.to_epub(cached_news_dict, reader_dir):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    else:
        log.info('Printing cached news')
        log.info('Limit is {}'.format(args.limit))
        if news.print_regular(cached_news_dict):
            log.info('Cached news printed successfully')
        else:
            print('Unknown error printing cached news')
            exit(1)


def parse_source_argument(args, reader_dir, cache_path):
    """Function that parses output arguments and prints or converts news
    depending on args variable value
    Also this function caches read news after printing or converting"""
    log.info('Parsing url')
    soup = news.get_soup(args.source, reader_dir)
    news_dict = news.get_items(args.limit, soup)
    log.info('Parsed successfully')
    if args.json:
        log.info('Printing news as JSON')
        log.info('Limit is {}'.format(args.limit))
        if news.print_json(news_dict):
            log.info('News printed successfully')
        else:
            print('Unknown error printing news')
            exit(1)
    elif args.to_html:
        log.info('Converting news to html')
        if converting.to_html(news_dict, reader_dir):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    elif args.to_pdf:
        log.info('Converting news to pdf')
        if converting.to_pdf(news_dict, reader_dir):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    elif args.to_fb2:
        log.info('Converting news to fb2')
        if converting.to_fb2(news_dict, reader_dir, args.source):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    elif args.to_epub:
        log.info('Converting news to epub')
        if converting.to_epub(news_dict, reader_dir):
            log.info('Converted successfully')
        else:
            print('Unknown error converting to html')
            exit(1)
    else:
        log.info('Printing news')
        log.info('Limit is {}'.format(args.limit))
        if news.print_regular(news_dict):
            log.info('News printed successfully')
        else:
            print('Unknown error printing news')
            exit(1)
    log.info('Caching news')
    ret = caching.cache_news(news_dict, cache_path)
    if ret is caching.CacheCleanError:
        log.info('New cache file was created')
    elif ret:
        log.info('News cached successfully')
    else:
        print('Unknown error caching news')
        exit(1)


def parse_clear_cache_argument(cache_path):
    log.info('Clearing cache')
    ret = caching.clear_cache(cache_path)
    if ret is caching.CacheCleanError:
        log.info('Cache is already clear')
    elif ret:
        log.info('Cache cleared successfully')
    else:
        print('Unknown error clearing cache')
        exit(1)


def main():
    """Main function that is called when running a package"""
    # making a reader directory
    reader_dir = path.join(Path.home(), 'rss_reader')
    cache_path = path.join(reader_dir, 'data.json')
    if not path.isdir(reader_dir):
        try:
            mkdir(reader_dir)
        except Exception as e:
            print('Error making a reader directory at {}'.format(reader_dir))
            print(e)
            exit(1)
    # parsing command line arguments
    args = get_arguments()
    if args.verbose:
        log.basicConfig(stream=stdout, level=log.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log.info('Received arguments successfully')
    log.info('Verbose mode is on')

    if args.date:
        parse_date_argument(args, reader_dir, cache_path)
    elif args.clear_cache:
        parse_clear_cache_argument(cache_path)
    elif len(args.source) is 1:
        args.source = args.source[0]  # assigning str('') value to source argument instead of list ['']
        parse_source_argument(args, reader_dir, cache_path)
    else:
        print('Invalid source')


if __name__ == '__main__':
    main()
