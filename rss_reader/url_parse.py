from bs4 import BeautifulSoup
import requests
import html


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
    # with open('f.xml', 'r') as f:
    #     soup = BeautifulSoup(f, 'xml')
    return soup


def get_items(soup):
    """This function extracts all items from the soup"""
    return soup.findAll('item')


def print_header(soup):
    """Function that prints header(Feed: ) from the soup"""
    print()
    print('Feed: ', soup.title.text)
    print()


def print_items(limit, items):
    """Function that prints news(items) {limit} number of times"""
    count = 0
    for i in items:
        if limit is not None and count == limit:
            break
        links = []
        images = []
        desc_soup = BeautifulSoup(i.description.text, 'html.parser')
        for j in desc_soup.findAll('a'):
            links.append(j.get('href'))
        for j in desc_soup.findAll('img'):
            images.append([j.get('src'), j.get('alt')])
        print('Title: ' + html.unescape(i.title.text))
        print("Date: " + html.unescape(i.pubDate.text))
        print('Link: ' + html.unescape(i.link.text))
        print()
        count2 = len(links)
        for j in images:
            print('[image {}: {}][{}]'.format(count2 + 1, j[1], count2 + 1), end='')
            count2 += 1
        print(desc_soup.text)
        print('\n')
        print('Links:   ')
        count2 = 1
        for j in links:
            print('[{}]: '.format(count2), j, ' (link)')
            count2 += 1
        for j in images:
            print('[{}]: '.format(count2), j[0], ' (image)')
            count2 += 1
        count += 1
        print('\n')
