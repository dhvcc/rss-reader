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
# update Readme version
# update config version
# readme usage


# tests


def get_arguments(**kwargs):
    """This function gets all the args from command line and return args namespace"""
    parser = argparse.ArgumentParser(
        description='Pure Python command-line RSS reader.',
        add_help=True)
    parser.add_argument('--version',
                        help='print version info',
                        action='version',
                        version='rss-reader {}'.format(version))
    parser.add_argument('--verbose',
                        help='output verbose status messages',
                        action='store_true')
    parser.add_argument('--date',
                        type=str,
                        help='print cached news from provided date in %%Y%%m%%d format')
    parser.add_argument('--clear-cache',
                        help='clear news cache',
                        action='store_true')
    parser.add_argument('--json',
                        help='print the news as JSON in stdout',
                        action='store_true')
    parser.add_argument('source',
                        help='RSS URL',
                        nargs='*',
                        type=str)
    parser.add_argument('--to-html',
                        action='store_true',
                        help='convert news to .html format and make a new file called news.html')
    parser.add_argument('--to-pdf',
                        action='store_true',
                        help='convert news to .pdf format and make a new file called news.pdf')
    parser.add_argument('--to-fb2',
                        action='store_true',
                        help='convert news to .fb2 format and make a new file called news.fb2')
    parser.add_argument('--to-epub',
                        action='store_true',
                        help='convert news to .epub format and make a new file called news.epub')
    parser.add_argument('--limit',
                        help='limit news topics if this parameter is provided',
                        type=int)
    parser.add_argument('--colorize',
                        action='store_true',
                        help='print the result of the utility in colorized mode')

    return parser.parse_args()


def parse_date_argument(args, reader_dir, cache_path, **kwargs):
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
        if news.print_regular(cached_news_dict, args.colorize):
            log.info('Cached news printed successfully')
        else:
            print('Unknown error printing cached news')
            exit(1)


def parse_source_argument(args, reader_dir, cache_path, **kwargs):
    """Function that parses output arguments and prints or converts news
    depending on args variable value
    Also this function caches read news after printing or converting"""
    log.info('Parsing url')
    soup = news.get_soup(args.source)
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
        if news.print_regular(news_dict, args.colorize):
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


def parse_clear_cache_argument(cache_path, **kwargs):
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
    reader_dir = path.join(Path.home(), 'rss_reader')
    cache_path = path.join(reader_dir, 'cache.json')
    # parsing command line arguments
    args = get_arguments()
    if args.verbose:
        log.basicConfig(stream=stdout, level=log.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log.info('Received arguments successfully')
    log.info('Verbose mode is on')
    # making a reader directory
    if not path.isdir(reader_dir):
        try:
            log.info('Making new directory for rss-reader files')
            mkdir(reader_dir)
        except Exception as e:
            print('Error making a reader directory at {}'.format(reader_dir))
            print(e)
            exit(1)
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
