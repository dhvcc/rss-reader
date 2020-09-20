from rss_reader.parser.models import RSSFeed, FeedItem
from rss_reader.imports import json
from jinja2 import Template
from os.path import join
import weasyprint
from ebooklib import epub

from pathlib import Path


class Converter:
    def __init__(self, rss: RSSFeed, convert_dir: str, convert_file: str, rss_raw: dict = None):
        self.rss = rss
        self.rss_raw = rss_raw
        self.convert_dir = convert_dir
        self.convert_file = convert_file

        self.module_dir = Path(__file__).parent

    def none(self):
        pass

    def json(self):
        file_path = join(self.convert_dir,
                         self.convert_file if self.convert_file else "rss_feed.json")
        with open(file_path, "w") as file:
            if self.rss_raw:
                file.write(json.dumps(self.rss_raw, indent=4))
            else:
                # If raw dict rss was not provided then create dict and dump it
                # dumps indent does not work on str
                loaded: dict = json.loads(self.rss.json())
                file.write(json.dumps(loaded, indent=4))

    def html(self):
        file_path = join(self.convert_dir,
                         self.convert_file if self.convert_file else "rss_feed.html")
        template = Template(open(join(self.module_dir, "html_template.jinja2")).read())
        with open(file_path, "w") as file:
            file.write(template.render(rss=self.rss))

    def pdf(self):
        file_path = join(self.convert_dir,
                         self.convert_file if self.convert_file else "rss_feed.pdf")
        template = Template(open(join(self.module_dir, "html_template.jinja2")).read())
        output_html = template.render(rss=self.rss)
        weasyprinted_html = weasyprint.HTML(string=output_html)
        weasyprinted_html.write_pdf(file_path)

    def fb2(self):
        # TODO
        ...

    def get_xhtml(self, feed_item: FeedItem) -> str:
        template = Template(open(join(self.module_dir, "xhtml_template.jinja2")).read())
        return template.render(item=feed_item)

    def epub(self):
        file_path = join(self.convert_dir,
                         self.convert_file if self.convert_file else "rss_feed.epub")
        book = epub.EpubBook()
        book.set_identifier('id')
        book.set_title(self.rss.title)
        # book.set_language('')
        book.add_author(self.rss.title)

        toc = []
        spine = ['nav']

        for num, item in enumerate(self.rss.feed, 1):
            chapter = epub.EpubHtml(title=item.title, file_name=f"{num}.xhtml")
            chapter.content = self.get_xhtml(item)

            book.add_item(chapter)
            spine.append(chapter)
            toc.append(epub.Section(item.title))
            toc.append(chapter)

        book.toc = tuple(toc)
        book.spine = spine

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        epub.write_epub(file_path, book)
