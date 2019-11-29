"""Converting module which is responsible for everything associated with converting
    (--to-html,--to-pdf, etc.)"""
import magic
import weasyprint
from yattag import Doc, indent
from os import path, remove
from rss_reader.news import get_response
import base64
from ebooklib import epub


def save_news(file, reader_dir, file_format, **kwargs):
    """Given file, output directory and file format
        Saves a file called news.{file_format}"""
    try:
        with open(path.join(reader_dir, 'news.' + file_format), 'w') as f:
            f.write(file)
    except Exception as e:
        raise Exception('Error saving news: {}'.format(e))


def get_html(news_dict, **kwargs):
    """Function that converts news to html format from given news dictionary
        Returns html if converted successfully"""
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
        raise Exception('Error getting HTML: {}'.format(e))


def get_xhtml(news, **kwargs):
    """Function that returns given news in xhtml format"""
    try:
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"')
        doc.asis('"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        with tag('html', ('xml:lang', ""), xmlns="http://www.w3.org/1999/xhtml", lang="en"):
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
        return doc.getvalue()
    except Exception as e:
        raise Exception('Error getting XHTML: {}'.format(e))


def get_binary_string_from_link(image_link, **kwargs):
    """Given image link, returns content bytes as a string"""
    try:
        response = get_response(image_link)
        return base64.b64encode(response.content).decode()
    except Exception as e:
        raise Exception('Error getting binary string from link: {}'.format(e))


def get_bytes_from_link(image_link, **kwargs):
    """Given image link, returns content bytes"""
    try:
        response = get_response(image_link)
        return response.content
    except Exception as e:
        raise Exception('Error getting bytes from link: {}'.format(e))


def to_html(news_dict, reader_dir, **kwargs):
    """Function that converts news to html format from given news dictionary
        Returns True if converted successfully"""
    try:
        html = get_html(news_dict)
        save_news(html, reader_dir, 'html')
        print('Saved news.html in {}'.format(reader_dir))
        return True
    except Exception as e:
        raise Exception('Error converting to HTML: {}'.format(e))


def to_pdf(news_dict, reader_dir, **kwargs):
    """Function that converts news to pdf format from given news dictionary
        Returns True if converted successfully"""
    try:
        pdf_path = path.join(reader_dir, 'news.pdf')
        html_weasy = weasyprint.HTML(string=get_html(news_dict))
        html_weasy.write_pdf(pdf_path)
        print('Saved news.pdf in {}'.format(reader_dir))
        return True
    except Exception as e:
        raise Exception('Error converting to PDF: {}'.format(e))


def to_fb2(news_dict, reader_dir, source, **kwargs):
    """Function that converts news to fb2 format from given news dictionary
        Returns True if converted successfully"""
    try:
        image_counter2 = 0
        img = {}
        for news in news_dict['News']:
            if 'Description images' in news:
                mime = magic.Magic(mime=True)
                for image in news['Description images']:
                    try:
                        image_bytes = get_bytes_from_link(image['Link'])
                        image_content = get_binary_string_from_link(image['Link'])
                    except Exception as e:
                        pass
                    else:
                        with open(path.join(reader_dir, 'tmp_image'), 'wb') as f:
                            f.write(image_bytes)
                        img[image_content] = (
                            image_counter2, mime.from_file(path.join(reader_dir, 'tmp_image')))
                        image_counter2 += 1
                try:
                    pass
                    remove(path.join(reader_dir, 'tmp_image'))
                except Exception:
                    pass
        section_counter = 0
        doc, tag, text = Doc().tagtext()
        doc.asis('<?xml version="1.0" encoding="utf-8"?>')
        with tag('FictionBook', ('xmlns:l', "http://www.w3.org/1999/xlink"),
                 xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"):
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
                    if 'Description links' in news:
                        for link in news['Description links']:
                            links.append(link)
                    if 'Description images' in news:
                        for image in news['Description images']:
                            images.append(image)
                    with tag('section', id=section_counter):
                        section_counter += 1
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
                                try:
                                    image_content = get_binary_string_from_link(image['Link'])
                                except Exception:
                                    pass
                                else:
                                    if image_content in img:
                                        doc.stag('image', ('l:href', '#{}'.format(img[image_content][0])))
                        doc.stag('empty-line')
                        if links:
                            doc.line('p', 'Links:')
                            for link in links:
                                doc.line('p', link)
            if img:
                for key, value in img.items():
                    with tag('binary', ('content-type', value[1]), id=value[0]):
                        text(key)
        save_news(doc.getvalue(), reader_dir, 'fb2')
        print('Saved news.fb2 in {}'.format(reader_dir))
        return True
    except Exception as e:
        raise Exception('Error converting to FB2: {}'.format(e))


def to_epub(news_dict, reader_dir, **kwargs):
    """Function that converts news to epub format from given news dictionary
        Returns True if converted successfully"""
    try:
        book = epub.EpubBook()
        book.set_identifier('id')
        book.set_title(news_dict['Feed title'])
        book.set_language('')

        book.add_author(news_dict['Feed title'])
        chapter_file_counter = 1
        spine = ['nav']
        toc = []
        for news in news_dict['News']:
            chapter = epub.EpubHtml(title=news['Title'], file_name='{}.xhtml'.format(chapter_file_counter))
            chapter.content = get_xhtml(news)
            book.add_item(chapter)
            spine.append(chapter)
            toc.append(epub.Section(news['Title']))
            toc.append(chapter)
            chapter_file_counter += 1

        book.toc = tuple(toc)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine = spine

        epub.write_epub(path.join(reader_dir, 'news.epub'), book, {})
        print('Saved news.epub in {}'.format(reader_dir))
        return True
    except Exception as e:
        raise Exception('Error converting to EPUB: {}'.format(e))
