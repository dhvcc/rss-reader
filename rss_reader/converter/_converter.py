"""For info read __init__.py docstring"""
import logging
from os.path import join
from pathlib import Path
from typing import Union

import weasyprint
from ebooklib import epub
from jinja2 import Template
from rss_parser.models import FeedItem, RSSFeed

from rss_reader.imports import json

logger = logging.getLogger("rss-reader")


class Converter:
    def __init__(
        self,
        rss: RSSFeed,
        convert_dir: str,
        convert_file: str,
        pretty: Union[None, bool],
        rss_raw: dict = None,
    ):
        self.rss = rss
        self.rss_raw = rss_raw
        self.convert_dir = convert_dir
        self.convert_file = convert_file

        self.pretty: str = "pretty_" if pretty else ""
        self.module_dir = Path(__file__).parent

    def none(self):
        """Empty method which is called if convert argument is 'none'"""
        pass

    def json(self):
        file_path = join(self.convert_dir, self.convert_file or "rss_feed.json")
        with open(file_path, "w") as file:
            if self.rss_raw:
                file.write(json.dumps(self.rss_raw, indent=4))
            else:
                # If raw dict rss was not provided then create dict and dump it
                # dumps indent does not work on str
                loaded: dict = json.loads(self.rss.json())
                file.write(json.dumps(loaded, indent=4))

        logger.info(f"Saved json in {file_path}")

    def get_html(self, **kwargs):
        template = Template(
            open(join(self.module_dir, f"{self.pretty}html_template.jinja2")).read()
        )
        return template.render(**kwargs)

    def html(self):
        file_path = join(self.convert_dir, self.convert_file or "rss_feed.html")
        with open(file_path, "w") as file:
            file.write(self.get_html(rss=self.rss))

        logger.info(f"Saved html in {file_path}")

    def pdf(self):
        file_path = join(self.convert_dir, self.convert_file or "rss_feed.pdf")
        output_html = self.get_html(rss=self.rss)
        weasyprinted_html = weasyprint.HTML(string=output_html)
        weasyprinted_html.write_pdf(file_path)

        logger.info(f"Saved pdf in {file_path}")

    def get_xhtml(self, feed_item: FeedItem, language: str = "") -> str:
        template = Template(open(join(self.module_dir, "xhtml_template.jinja2")).read())
        return template.render(item=feed_item, language=language)

    def epub(self):
        file_path = join(self.convert_dir, self.convert_file or "rss_feed.epub")
        book = epub.EpubBook()
        book.set_identifier("id")
        book.set_title(self.rss.title)
        book.set_language(self.rss.language)
        book.add_author(self.rss.title)

        toc = []
        spine = ["nav"]

        for num, item in enumerate(self.rss.feed, 1):
            chapter = epub.EpubHtml(title=item.title, file_name=f"{num}.xhtml")
            chapter.content = self.get_xhtml(item, self.rss.language)

            book.add_item(chapter)
            spine.append(chapter)
            toc.append(epub.Section(item.title))
            toc.append(chapter)

        book.toc = tuple(toc)
        book.spine = spine

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        epub.write_epub(file_path, book)

        logger.info(f"Saved epub in {file_path}")
