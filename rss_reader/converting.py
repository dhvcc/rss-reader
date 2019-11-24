import weasyprint
from yattag import Doc, indent
from os import path
import sys
from rss_reader.news import get_response
import base64
from ebooklib import epub
import mimetypes


def save_news(file, reader_dir, file_format):
    try:
        with open(path.join(reader_dir, 'news.' + file_format), 'w') as f:
            f.write(file)
    except Exception as e:
        print('Error saving a file')
        print(e)
        sys.exit(1)


def save_binary_news(file, reader_dir, file_format):
    try:
        with open(path.join(reader_dir, 'news.' + file_format), 'wb') as f:
            f.write(file)
    except Exception as e:
        print('Error saving a file')
        print(e)
        sys.exit(1)


def get_html(news_dict):
    """Function that converts news to html format
    Return True if converted successfully"""
    try:
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('header'):
                with tag('h2'):
                    text(news_dict['Feed title'])
            with tag('body'):
                with tag('ol'):
                    for news in news_dict['News']:
                        with tag('li'):
                            with tag('h3'):
                                doc.line('a', news['Title'], href=news['Link'])
                            if 'Publishing date' in news:
                                doc.line('h4', news['Publishing date'])
                            if 'Category' in news:
                                doc.line('h4', news['Category'])
                            doc.line('p', news['Description'])
                            doc.nl()
                            with tag('ul'):
                                if 'Description links' in news:
                                    for link in news['Description links']:
                                        with tag('li'):
                                            doc.line('a', link, href=link)
                                if 'Description images' in news:
                                    for image in news['Description images']:
                                        doc.line('p', '')
                                        doc.stag('img', src=image['Link'], klass="photo")
                                        doc.line('p', image['Title'])
        return indent(doc.getvalue())
    except Exception as e:
        print('Error converting to html')
        print(e)
        sys.exit(1)


def get_xhtml(news):
    """Function that converts news to html format
    Return True if converted successfully"""
    try:
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"')
        doc.asis('"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        doc.asis('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">')
        with tag('head'):
            doc.stag('meta', content="text/html; charset=utf-8")
            doc.line('title', news['Title'])
        with tag('body'):
            with tag('ol'):
                with tag('li'):
                    with tag('h3'):
                        doc.line('a', news['Title'], href=news['Link'])
                    if 'Publishing date' in news:
                        doc.line('h4', news['Publishing date'])
                    if 'Category' in news:
                        doc.line('h4', news['Category'])
                    doc.line('p', news['Description'])
                    doc.nl()
                    with tag('ul'):
                        if 'Description links' in news:
                            for link in news['Description links']:
                                with tag('li'):
                                    doc.line('a', link, href=link)
                        if 'Description images' in news:
                            for image in news['Description images']:
                                doc.line('p', '')
                                doc.stag('img', src=image['Link'], klass="photo")
                                doc.line('p', image['Title'])
        doc.asis('</html>')
        return doc.getvalue()
    except Exception as e:
        print('Error getting xhtml')
        print(e)
        sys.exit(1)


def to_html(news_dict, reader_dir):
    """Function that converts news to html format
    Returns True if converted successfully"""
    try:
        html = get_html(news_dict)
        if html:
            save_news(html, reader_dir, 'html')
            return True
        else:
            return False
    except Exception as e:
        print('Error saving a file')
        print(e)
        sys.exit(1)


def get_binary_image(image_link):
    response = get_response(image_link)
    return base64.b64encode(response.content).decode()


def to_pdf(news_dict, reader_dir):
    """Function that converts news to pdf format
    Return True if converted successfully"""
    try:
        pdf_path = path.join(reader_dir, 'news.pdf')
        html_weasy = weasyprint.HTML(string=get_html(news_dict))
        html_weasy.write_pdf(pdf_path)
        return True
    except Exception as e:
        print('Error converting to pdf')
        print(e)
        sys.exit(1)


def to_fb2(news_dict, reader_dir, source):
    try:
        image_counter = 0
        all_images = []
        doc, tag, text = Doc().tagtext()
        doc.asis('<?xml version="1.0" encoding="utf-8"?>')
        doc.asis(
            '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">')
        with tag('description'):
            with tag('title-info'):
                doc.line('genre', 'News')
                doc.line('book-title', news_dict['Feed title'])
                doc.line('author', news_dict['Feed title'])
                doc.line('lang', '')
            with tag('document-info'):
                doc.line('author', news_dict['Feed title'])
                doc.line('date', '')
                doc.line('src-url', source)  # Source
                doc.line('program-used', 'rss-reader 1.4.0')
                doc.line('id', '')
                doc.line('version', '1')
        with tag('body'):
            for news in news_dict['News']:
                images = []
                links = []
                if 'Description images' in news:
                    for image in news['Description images']:
                        images.append({'Title': image['Title'],
                                       'Link': image['Link'],
                                       'Index': str(image_counter)})
                        all_images.append({'Title': image['Title'],
                                           'Link': image['Link'],
                                           'Index': str(image_counter)})
                        image_counter += 1
                if 'Description links' in news:
                    for link in news['Description links']:
                        links.append(link)
                with tag('section'):
                    with tag('title'):
                        doc.line('p', news['Title'])
                    if 'Publishing date' in news:
                        doc.line('p', news['Publishing date'])
                    if 'Category' in news:
                        doc.line('p', news['Category'])
                    doc.stag('empty-line')
                    doc.line('p', news['Description'])
                    doc.stag('empty-line')
                    if images:
                        for image in images:
                            doc.asis('<p><image l:href="#{}"/></p>'.format(image['Index']))
                    doc.stag('empty-line')
                    if links:
                        doc.line('p', 'Links:')
                        for link in links:
                            doc.line('p', link)
        if all_images:
            for image in all_images:
                with tag('binary', ('content-type', mimetypes.guess_type(image['Link'])[0]),
                         id="{}".format(image['Index'])):
                    text(get_binary_image(image['Link']))
        doc.asis('</FictionBook>')
        save_news(doc.getvalue(), reader_dir, 'fb2')
        return True
    except Exception as e:
        print('Error converting to fb2')
        print(e)
        sys.exit(1)


def to_epub(news_dict, reader_dir):
    try:
        book = epub.EpubBook()
        book.set_identifier('id')
        book.set_title(news_dict['Feed title'])
        book.set_language('')

        book.add_author(news_dict['Feed title'])

        counter = 0
        spine = ['nav']
        toc = []
        for news in news_dict['News']:
            c = epub.EpubHtml(title=news['Title'], file_name='{}.xhtml'.format(counter))
            c.content = get_xhtml(news)
            book.add_item(c)
            spine.append(c)
            toc.append(epub.Section(news['Title']))
            toc.append(c)
            counter += 1

        book.toc = tuple(toc)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = spine

        epub.write_epub(path.join(reader_dir, 'news.epub'), book, {})
        return True
    except Exception as e:
        print('Error converting to epub')
        print(e)
        sys.exit(1)
