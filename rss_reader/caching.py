"""Caching module"""
import json
import datetime


def cache_news(news_dict):
    """Function that caches news"""
    try:
        f = open('data.json', 'r+')
        json_dict = json.loads(f.read())
        f.close()
        f = open('data.json', 'w')
        for i in news_dict['News']:
            if 'Publishing date' in i:
                datetime_object = datetime.datetime.strptime(i['Publishing date'], '%a, %d %b %Y %H:%M:%S %z')
                date = str(datetime_object.year) + str(datetime_object.month) + str(datetime_object.day)
                if date not in json_dict:
                    json_dict[date] = []
                    json_dict[date].append(i)
                else:
                    if i not in json_dict[date]:
                        json_dict[date].append(i)
        f.write(json.dumps(json_dict, indent=4, ensure_ascii=False))
        f.close()
        return True
    except FileNotFoundError as e:
        with open('data.json', 'w+') as f:
            json_dict = {}
            for i in news_dict['News']:
                if 'Publishing date' in i:
                    datetime_object = datetime.datetime.strptime(i['Publishing date'], '%a, %d %b %Y %H:%M:%S %z')
                    date = str(datetime_object.year) + str(datetime_object.month) + str(datetime_object.day)
                    if date not in json_dict:
                        json_dict[date] = []
                        json_dict[date].append(i)
                    else:
                        if i not in json_dict[date]:
                            json_dict[date].append(i)
            f.write(json.dumps(dict(json_dict), indent=4, ensure_ascii=False))
        return e
    except EnvironmentError as e:
        return e


def print_cache_regular(date, limit):
    """Function that print cashed news"""
    try:
        with open('data.json', 'r') as f:
            json_dict = json.loads(f.read())
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
    except EnvironmentError as e:
        return e


def print_cache_json(date, limit):
    """Function that print cashed news, but in JSON"""
    try:
        with open('data.json', 'r') as f:
            json_dict = json.loads(f.read())
            if date in json_dict:
                if limit is not None:
                    new_json_dict = {date: [json_dict[date][:limit]]}
                else:
                    new_json_dict = {date: [json_dict[date]]}
                print(json.dumps(new_json_dict, indent=4, ensure_ascii=False))
                return True
            else:
                return False
    except EnvironmentError as e:
        return e
