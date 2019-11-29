"""Converting module which is responsible for everything associated with printing and parsing news"""
from bs4 import BeautifulSoup
from requests import get
from html import unescape
from json import dumps
from colorama import init, Fore, Back, Style


class RSSNotFoundError(Exception):
    def __init__(self):
        Exception.__init__(self, 'RSS not found')


def get_response(source, **kwargs):
    """Function that returns response from source it received"""
    try:
        resp = get(source, timeout=5)
        return resp
    except Exception:
        raise Exception('Error requesting a response')


def get_soup(source, **kwargs):
    """Function that returns BeautifulSoup object from response"""
    try:
        response = get_response(source)
        soup = BeautifulSoup(response.content, 'xml')
        # with open('/home/kwiz/rss_reader/yahoo.xml', 'r') as f:
        # with open('/home/kwiz/rss_reader/tutby.xml', 'r') as f:
        #     soup = BeautifulSoup(f.read(), 'xml')
        if soup.rss is None:
            raise RSSNotFoundError
        return soup
    except RSSNotFoundError as e:
        raise e
    except Exception as e:
        raise Exception('Error getting soup: {}'.format(e))


def get_items(limit, soup, **kwargs):
    """Function that returns news dictionary extracted from given BeautifulSoup object"""
    try:
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
    except Exception as e:
        raise Exception('Error getting items: {}'.format(e))


def print_regular(news_dict, color, **kwargs):
    """Function that prints news from given news dictionary"""
    try:
        print()
        if color:
            print(Style.NORMAL, Back.WHITE, Fore.BLACK, end='\b\b')
        print('Feed: ', news_dict['Feed title'], Style.RESET_ALL)
        print()
        for news in news_dict['News']:
            if color:
                print(Style.NORMAL, Back.WHITE, Fore.BLACK, end='\b\b')
            print('Title: {}'.format(news['Title']), Style.RESET_ALL)
            if color:
                print(Style.BRIGHT, Fore.WHITE, end='\b')
            if 'Publishing date' in news:
                print('Publishing date: {}'.format(news['Publishing date']))
            if 'Category' in news:
                print("Category: {}".format(news['Category']))
            print('Link: {}'.format(news['Link']))
            print(Style.RESET_ALL, end='')
            print()
            if color:
                print(Style.BRIGHT, Fore.YELLOW, end='\b')
            print(news['Description'])
            print(Style.RESET_ALL, end='')
            print()
            if color:
                print(Style.BRIGHT, Fore.WHITE, end='\b')
            if 'Description links' in news:
                desc_links_counter = 1
                print('Description links: ')
                for j in news['Description links']:
                    print('[{}]: {}'.format(desc_links_counter, j))
                    desc_links_counter += 1
            if 'Description images' in news:
                desc_images_counter = 1
                print('Description images: ')
                for j in news['Description images']:
                    print('[{}][{}]: {}'.format(desc_images_counter, j['Title'], j['Link']))
                    desc_images_counter += 1
            print(Style.RESET_ALL, end='')
            print('\n')
        return True
    except Exception as e:
        raise Exception('Error printing news: '.format(e))


def print_json(news_dict, **kwargs):
    """Function that prints news from given news dictionary in JSON format
        Returns True if successful"""
    try:
        dump = dumps(news_dict, indent=4, ensure_ascii=False)
        print(dump)
        return True
    except Exception as e:
        raise Exception('Error dumping/printing news in JSON: {}'.format(e))
