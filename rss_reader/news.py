"""Source parsing and printing module"""
from bs4 import BeautifulSoup
import requests
import html
import json


def get_response(source):
    """Function that returns response from source it received"""
    try:
        resp = requests.get(source)
    except requests.RequestException as e:
        print(e)
        exit(1)
    except UnicodeError as e:
        print(e)
        exit(1)
    return resp


def get_soup(source):
    """Function that returns soup from response"""
    response = get_response(source)
    soup = BeautifulSoup(response.content, 'xml')
    return soup


def format_string(s):
    s = html.unescape(s)
    return s


def get_items(limit, soup):
    feed = format_string(soup.title.text)
    news_dict = {'Feed title': feed, 'News': []}
    items = soup.findAll('item')
    counter = 0
    for i in items:
        if limit is not None and counter == limit:
            break
        links = []
        images = []
        desc_soup = BeautifulSoup(i.description.text, 'html.parser')
        for j in desc_soup.findAll('a'):
            links.append(j.get('href'))
        for j in desc_soup.findAll('img'):
            images.append({'Title': j.get('alt'), 'Link': j.get('src')})
        news_dict['News'].append({})
        news_dict['News'][counter]['Title'] = format_string(i.title.text)
        news_dict['News'][counter]['Link'] = format_string(i.link.text)
        if i.pubDate:
            news_dict['News'][counter]['Publishing date'] = format_string(i.pubDate.text)
        if i.category:
            news_dict['News'][counter]['Category'] = format_string(i.category.text)
        news_dict['News'][counter]['Description'] = format_string(desc_soup.text)
        if links:
            news_dict['News'][counter]['Description links'] = links
        if images:
            news_dict['News'][counter]['Description images'] = images
        counter += 1
    return news_dict


def print_regular(news_dict):
    """Function that prints news"""
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


def print_json(news_dict):
    """The same function as print_regular, but prints in JSON"""
    print(json.dumps(news_dict, indent=4, ensure_ascii=False))
