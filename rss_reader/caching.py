"""Converting module which is responsible for everything associated with caching
    (--date DATE)"""
from json import loads, dumps
from datetime import datetime
from os import remove


class CacheCleanError(FileNotFoundError):
    """Exception that is thrown when cache file doesn't exist"""

    def __init__(self):
        FileNotFoundError.__init__(self, 'Cache file does not exist')


class NoNewsError(Exception):
    """Exception that is thrown if there are no news from given date"""

    def __init__(self):
        Exception.__init__(self, 'There are no news from that date')


def cache_news(news_dict, cache_path, **kwargs):
    """Function that caches news from given dict
        If there's no cache file, creates it and raises CacheCleanError
        Returns True if everything's fine"""
    try:
        with open(cache_path, 'r+') as f:
            json_dict = loads(f.read())
            f.seek(0, 0)
            for i in news_dict['News']:
                if 'Publishing date' in i:
                    datetime_object = datetime.strptime(i['Publishing date'], '%a, %d %b %Y %H:%M:%S %z')
                    date = str(datetime_object.year) + str(datetime_object.month) + str(datetime_object.day)
                    if date not in json_dict:
                        json_dict[date] = []
                        json_dict[date].append(i)
                    elif i not in json_dict[date]:
                        json_dict[date].append(i)
            f.write(dumps(json_dict, indent=4, ensure_ascii=False))
        return True
    except FileNotFoundError as e:
        try:
            with open(cache_path, 'w+') as f:
                json_dict = {}
                for i in news_dict['News']:
                    if 'Publishing date' in i:
                        datetime_object = datetime.strptime(i['Publishing date'], '%a, %d %b %Y %H:%M:%S %z')
                        date = str(datetime_object.year) + str(datetime_object.month) + str(datetime_object.day)
                        if date not in json_dict:
                            json_dict[date] = []
                            json_dict[date].append(i)
                        else:
                            if i not in json_dict[date]:
                                json_dict[date].append(i)
                f.write(dumps(dict(json_dict), indent=4, ensure_ascii=False))
            raise CacheCleanError
        except Exception as e:
            raise e
    except CacheCleanError as e:
        raise e
    except Exception as e:
        raise Exception('Error caching news: {}'.format(e))


def clear_cache(cache_path, **kwargs):
    """Function that deletes cache file
        Returns True if cache file deleted successfully
        Raises CacheCleanError if cache is already clear"""
    try:
        remove(cache_path)
        return True
    except FileNotFoundError:
        raise CacheCleanError
    except Exception as e:
        raise Exception('Error clearing cache: {}'.format(e))


def get_cached_news(date, limit, cache_path, **kwargs):
    """Function that return cached news dictionary from given date
        Returns cached news dictionary if everything's fine
        Raises NoNewsError if there are news from given date
        Raises CacheCleanError if there's no cache file"""
    try:
        cached_news_dict = {'Feed title': 'Cache from {}'.format(date), 'News': []}
        with open(cache_path, 'r') as f:
            json_dict = loads(f.read())
            if date in json_dict:
                limit_counter = 0
                for news in json_dict[date]:
                    if limit is not None and limit_counter == limit:
                        break
                    cached_news_dict['News'].append(news)
                    limit_counter += 1
                return cached_news_dict
            else:
                raise NoNewsError
    except FileNotFoundError as e:
        raise CacheCleanError
    except NoNewsError as e:
        raise e
    except Exception as e:
        raise Exception('Error getting cached news: {}'.format(e))
