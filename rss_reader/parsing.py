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
    return resp


def get_soup(source):
    """Function that returns soup from response"""
    response = get_response(source)
    soup = BeautifulSoup(response.content, 'xml')
    return soup


def get_items(soup):
    """This function extracts all items from the soup"""
    return soup.findAll('item')


def print_regular(limit, soup):
    """Function that prints news(items) {limit} number of times"""
    counter = 0
    items = soup.findAll('item')
    print()
    print('Feed: {}'.format(html.unescape(soup.title.text)))
    print()
    for i in items:
        if limit is not None and counter == limit:
            break
        links = []
        images = []
        desc_soup = BeautifulSoup(i.description.text, 'html.parser')
        for j in desc_soup.findAll('a'):
            links.append(j.get('href'))
        for j in desc_soup.findAll('img'):
            images.append([j.get('src'), j.get('alt')])
        print('Title: ' + html.unescape(i.title.text))
        if i.pubDate:
            print('Publishing date: {}'.format(html.unescape(i.pubDate.text)))
        if i.category:
            print("Category: {}".format(html.unescape(i.category.text)))
        print('Link: ' + html.unescape(i.link.text))
        print()
        print(desc_soup.text)
        print()
        if links:
            counter2 = 1
            print('Description links: ')
            for j in links:
                print('[{}]: {}'.format(counter2, j))
                counter2 += 1
        if images:
            counter2 = 1
            print('Description images: ')
            for j in images:
                print('[{}][{}]: {}'.format(counter2, j[1], j[0]))
                counter2 += 1
        counter += 1
        print('\n')


def print_json(limit, soup):
    """The same function ans print_regular, but it prints in JSON(--json) """
    feed = html.unescape(soup.title.text)
    dict_json = {feed: []}
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
        dict_json[feed].append({})
        dict_json[feed][counter]['Title'] = html.unescape(i.title.text)
        dict_json[feed][counter]['Link'] = html.unescape(i.link.text)
        if i.pubDate:
            dict_json[feed][counter]['Publishing date'] = html.unescape(i.pubDate.text)
        if i.category:
            dict_json[feed][counter]['Category'] = html.unescape(i.category.text)
        dict_json[feed][counter]['Description'] = html.unescape(desc_soup.text)
        if links:
            dict_json[feed][counter]['Description links'] = links
        if images:
            dict_json[feed][counter]['Description images'] = images
        counter += 1
    print(json.dumps(dict_json, indent=4, ensure_ascii=False))
