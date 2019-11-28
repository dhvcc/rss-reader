"""Converting module which is responsible for everything associated with caching
    (--date DATE)"""
from json import loads, dumps
from sys import exit
from datetime import datetime
from os import remove


def cache_news(news_dict, cache_path, **kwargs):
    """Function that caches news from given dict
        If there's no cache file, creates it and returns CacheCleanError
        Returns True if everything's fine"""
    try:
        f = open(cache_path, 'r+')
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
        f.close()
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
                return CacheCleanError
        except Exception as e:
            print('Error creating cache file')
            print(e)
            exit(1)
    except Exception as e:
        print('Error reading and later creating cache file')
        print(e)
        exit(1)


class CacheCleanError(FileNotFoundError):
    """Exception that is thrown when cache file doesn't exist"""
    pass


def clear_cache(cache_path, **kwargs):
    """Function that deletes cache file
        Returns True if cache file deleted successfully
        Returns CacheCleanError if cache is already clear"""
    try:
        remove(cache_path)
        return True
    except FileNotFoundError:
        return CacheCleanError
    except Exception as e:
        print('Error clearing cache')
        print(e)
        exit(1)


def get_cached_news(date, limit, cache_path, **kwargs):
    """Function that return cached news dictionary from given date
        Returns cached news dictionary if everything's fine
        Returns False if there are news from given date
        Returns CacheCleanError if there's no cache file"""
    try:
        cached_news_dict = {'Feed title': 'Cache from {}'.format(date), 'News': []}
        with open(cache_path, 'r') as f:
            json_dict = loads(f.read())
            if date in json_dict:
                counter = 0
                for news in json_dict[date]:
                    if limit is not None and counter == limit:
                        break
                    cached_news_dict['News'].append(news)
                    counter += 1
                return cached_news_dict
            else:
                return False
    except FileNotFoundError as e:
        return CacheCleanError
    except Exception as e:
        print('Error printing cached news')
        print(e)
        exit(1)
