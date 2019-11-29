"""Main module"""
import argparse
from rss_reader import news
from rss_reader import caching
from rss_reader.config import version
from rss_reader import converting
import logging as log
from sys import exit, stdout
from pathlib import Path
from os import path, mkdir


# before commit
# update Readme version
# update config version
# readme usage


# delete with open on response
# tests

class InvalidSourceError(Exception):
    """Exception that is thrown if the source is invalid"""

    def __init__(self):
        Exception.__init__(self, 'Invalid source')


def get_parser(**kwargs):
    """This function gets all the args from command line and return args namespace"""
    try:
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
        return parser
    except Exception as e:
        raise Exception('Error parsing arguments')


def parse_date_argument(args, reader_dir, cache_path, **kwargs):
    """Function that parses the --date argument prints or converts cached news from given date
    depending on args variable values"""
    try:
        try:
            cached_news_dict = caching.get_cached_news(args.date, args.limit, cache_path)
        except caching.NoNewsError as e:
            raise e
        except caching.CacheCleanError as e:
            raise e

        if args.json:
            log.info('Printing cached news as JSON')
            log.info('Limit is {}'.format(args.limit))
            if news.print_json(cached_news_dict):
                log.info('Cached news printed successfully')
            else:
                raise Exception('Unknown error printing cached news')
        elif args.to_html:
            log.info('Converting cached news to html')
            if converting.to_html(cached_news_dict, reader_dir):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        elif args.to_pdf:
            log.info('Converting cached news to pdf')
            if converting.to_pdf(cached_news_dict, reader_dir):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        elif args.to_fb2:
            log.info('Converting cached news to fb2')
            if converting.to_fb2(cached_news_dict, reader_dir, 'Cache'):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        elif args.to_epub:
            log.info('Converting cached news to epub')
            if converting.to_epub(cached_news_dict, reader_dir):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        else:
            log.info('Printing cached news')
            log.info('Limit is {}'.format(args.limit))
            if news.print_regular(cached_news_dict, args.colorize):
                log.info('Cached news printed successfully')
            else:
                raise Exception('Unknown error printing cached news')
    except Exception as e:
        log.info(e)
        raise Exception('Error printing cached news')


def parse_source_argument(args, reader_dir, cache_path, **kwargs):
    """Function that parses output arguments and prints or converts news
    depending on args variable value
    Also this function caches read news after printing or converting"""
    try:
        log.info('Parsing url')
        try:
            soup = news.get_soup(args.source)
        except news.RSSNotFoundError as e:
            raise e
        news_dict = news.get_items(args.limit, soup)
        log.info('Parsed successfully')
        if args.json:
            log.info('Printing news as JSON')
            log.info('Limit is {}'.format(args.limit))
            if news.print_json(news_dict):
                log.info('News printed successfully')
            else:
                raise Exception('Unknown error printing news')
        elif args.to_html:
            log.info('Converting news to html')
            if converting.to_html(news_dict, reader_dir):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        elif args.to_pdf:
            log.info('Converting news to pdf')
            if converting.to_pdf(news_dict, reader_dir):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        elif args.to_fb2:
            log.info('Converting news to fb2')
            if converting.to_fb2(news_dict, reader_dir, args.source):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        elif args.to_epub:
            log.info('Converting news to epub')
            if converting.to_epub(news_dict, reader_dir):
                log.info('Converted successfully')
            else:
                raise Exception('Unknown error converting to html')
        else:
            log.info('Printing news')
            log.info('Limit is {}'.format(args.limit))
            if news.print_regular(news_dict, args.colorize):
                log.info('News printed successfully')
            else:
                raise Exception('Unknown error printing news')
        log.info('Caching news')
        try:
            ret = caching.cache_news(news_dict, cache_path)
            if ret:
                log.info('News cached successfully')
            else:
                raise Exception('Unknown error caching news')
        except caching.CacheCleanError:
            log.info('New cache file was created')
    except news.RSSNotFoundError as e:
        raise e
    except Exception as e:
        log.info(e)
        raise Exception('Error printing news')


def parse_clear_cache_argument(cache_path, **kwargs):
    """Function that parses the --clear-cache argument"""
    try:
        log.info('Clearing cache')
        try:
            ret = caching.clear_cache(cache_path)
            if ret:
                log.info('Cache cleared successfully')
            else:
                raise Exception('Unknown error clearing cache')
        except caching.CacheCleanError as e:
            raise e
    except Exception as e:
        log.info(e)
        raise Exception('Error clearing cache')


def main():
    """Main function that is called when running a package"""
    try:
        parser = get_parser()
        args = parser.parse_args()
    except Exception as e:
        print(e)
        exit(1)
    try:
        reader_dir = path.join(Path.home(), 'rss_reader')
        cache_path = path.join(reader_dir, 'cache.json')
        if args.verbose:
            log.basicConfig(stream=stdout, level=log.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log.info('Received arguments successfully')
        log.info('Verbose mode is on')
        if not path.isdir(reader_dir):
            try:
                log.info('Making new directory for rss-reader files')
                mkdir(reader_dir)
            except Exception as e:
                print('Error making a reader directory at {}'.format(reader_dir))
                print(e)
                raise e
        if args.date:
            parse_date_argument(args, reader_dir, cache_path)
        elif args.clear_cache:
            parse_clear_cache_argument(cache_path)
        elif len(args.source) is 1:
            args.source = args.source[0]  # assigning str('') value to source argument instead of list ['']
            parse_source_argument(args, reader_dir, cache_path)
        else:
            log.info('Source {} is not valid'.format(args.source))
            raise InvalidSourceError
    except Exception as e:
        print(e)
        if not args.verbose:
            print('Use --verbose for more details')
        parser.print_help()


if __name__ == '__main__':
    main()
