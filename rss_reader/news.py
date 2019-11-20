"""News parsing module"""
from bs4 import BeautifulSoup
from requests import get
from html import unescape
from json import dumps
from sys import exit


def get_response(source):
    """Function that returns response from source it received"""
    try:
        resp = get(source)
    except Exception as e:
        print('Error requesting a response')
        print(e)
        exit(1)
    return resp


def get_soup(source):
    """Function that returns BeautifulSoup object from response"""
    response = get_response(source)
    try:
        soup = BeautifulSoup(response.content, 'xml')
    except Exception as e:
        print('Error parsing url response')
        print(e)
        exit(1)
    return soup


def get_items(limit, soup):
    """Function that return news dictionary extracted from given BeautifulSoup object"""
    feed_title = unescape(soup.title.text)
    news_dict = {'Feed title': feed_title, 'News': []}
    items = soup.findAll('item')
    limit_counter = 0
    for i in items:
        if limit is not None and limit_counter == limit:
            break
        links = []
        images = []
        desc_soup = BeautifulSoup(i.description.text, 'html.parser')
        for j in desc_soup.findAll('a'):
            links.append(j.get('href'))
        for j in desc_soup.findAll('img'):
            images.append({'Title': j.get('alt'), 'Link': j.get('src')})
        news_dict['News'].append({})
        news_dict['News'][limit_counter]['Title'] = unescape(i.title.text)
        news_dict['News'][limit_counter]['Link'] = unescape(i.link.text)
        if i.pubDate:
            news_dict['News'][limit_counter]['Publishing date'] = unescape(i.pubDate.text)
        if i.category:
            news_dict['News'][limit_counter]['Category'] = unescape(i.category.text)
        news_dict['News'][limit_counter]['Description'] = unescape(desc_soup.text)
        if links:
            news_dict['News'][limit_counter]['Description links'] = links
        if images:
            news_dict['News'][limit_counter]['Description images'] = images
        limit_counter += 1
    return news_dict


def print_regular(news_dict):
    """Function that prints news from given news dictionary"""
    try:
        print()
        print('Feed: {}'.format(news_dict['Feed title']))
        print()
        for news in news_dict['News']:
            print('Title: {}'.format(news['Title']))
            if 'Publishing date' in news:
                print('Publishing date: {}'.format(news['Publishing date']))
            if 'Category' in news:
                print("Category: {}".format(news['Category']))
            print('Link: {}'.format(news['Link']))
            print()
            print(news['Description'])
            print()
            if 'Description links' in news:
                counter2 = 1
                print('Description links: ')
                for j in news['Description links']:
                    print('[{}]: {}'.format(counter2, j))
                    counter2 += 1
            if 'Description images' in news:
                counter2 = 1
                print('Description images: ')
                for j in news['Description images']:
                    print('[{}][{}]: {}'.format(counter2, j['Title'], j['Link']))
                    counter2 += 1
            print('\n')
            return True
    except Exception as e:
        print('Error printing news')
        print(e)
        exit(1)


def print_json(news_dict):
    """Function that prints news from given news dictionary in JSON format"""
    try:
        dump = dumps(news_dict, indent=4, ensure_ascii=False)
        print(dump)
        return True
    except Exception as e:
        print('Error dumping/printing news in JSON')
        print(e)
        exit(1)
