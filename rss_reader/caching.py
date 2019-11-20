"""Caching module"""
from json import loads, dumps
from sys import exit
from datetime import datetime
from os import remove


def cache_news(news_dict, cache_path):
    """Function that caches news from given dict
    If there's no cache file, creates it and returns FileNotFoundError
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
    pass


def clear_cache(cache_path):
    """Function that deletes cache file
    Returns True if cache file deleted successfully
    Returns CacheClear if cache is already clear"""
    try:
        remove(cache_path)
        return True
    except FileNotFoundError:
        return CacheCleanError
    except Exception as e:
        print('Error clearing cache')
        print(e)
        exit(1)


def print_cache_regular(date, limit, cache_path):
    """Function that prints cached news from given date
    Returns True if everything's fine
    Returns False if there are news from given date
    Returns FileNotFoundError if there's no cache file"""
    try:
        with open(cache_path, 'r') as f:
            json_dict = loads(f.read())
            if date in json_dict:
                print('\n')
                counter = 0
                for i in json_dict[date]:
                    if limit is not None and counter == limit:
                        break
                    counter += 1
                    print('Title: {}'.format(i['Title']))
                    if 'Publishing date' in i:
                        print('Publishing date: {}'.format(i['Publishing date']))
                    if 'Category' in i:
                        print("Category: {}".format(i['Category']))
                    print('Link: {}'.format(i['Link']))
                    print()
                    print(i['Description'])
                    print()
                    if 'Description links' in i:
                        counter2 = 1
                        print('Description links: ')
                        for j in i['Description links']:
                            print('[{}]: {}'.format(counter2, j))
                            counter2 += 1
                    if 'Description images' in i:
                        counter2 = 1
                        print('Description images: ')
                        for j in i['Description images']:
                            print('[{}][{}]: {}'.format(counter2, j['Title'], j['Link']))
                            counter2 += 1
                    print('\n')
                return True
            else:
                return False
    except FileNotFoundError as e:
        return CacheCleanError
    except Exception as e:
        print('Error printing cached news')
        print(e)
        exit(1)


def print_cache_json(date, limit, cache_path):
    """Function that prints cached news from given date in JSON format
    Returns True if everything's fine
    Returns False if there are news from given date
    Returns FileNotFoundError if there's no cache file"""
    try:
        with open(cache_path, 'r') as f:
            json_dict = loads(f.read())
            if date in json_dict:
                if limit is not None:
                    new_json_dict = {date: [json_dict[date][:limit]]}
                else:
                    new_json_dict = {date: [json_dict[date]]}
                print(dumps(new_json_dict, indent=4, ensure_ascii=False))
                return True
            else:
                return False
    except FileNotFoundError as e:
        return CacheCleanError
    except Exception as e:
        print('Error printing cached news in JSON')
        print(e)
        exit(1)
