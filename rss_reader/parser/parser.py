from bs4 import BeautifulSoup
from html import unescape

from .models import RSSFeed


class Parser:
    def __init__(self, xml, limit=None):
        self.xml = xml
        self.limit = limit

        self.raw_data = None
        self.rss = None

    @staticmethod
    def get_soup(xml: str) -> BeautifulSoup:
        return BeautifulSoup(xml, 'xml')

    def parse(self) -> RSSFeed:
        main_soup = self.get_soup(self.xml)
        self.raw_data = {
            "title": unescape(main_soup.title.text),
            "link": unescape(main_soup.link.text),
            "feed": []
        }
        items = main_soup.findAll("item")
        if self.limit is not None:
            items = items[:self.limit]
        for item in items:
            description_soup = self.get_soup(item.description.text)
            item_dict = {
                "title": unescape(item.title.text),
                "link": unescape(item.link.text),
                "publish_date": getattr(item.pubDate, "text", ""),
                "category": getattr(item.category, "text", ""),
                "description": description_soup.text,
                "description_links": [anchor.get("href") for anchor in description_soup.findAll('a')],
                "description_images": [
                    {"alt": image.get("alt"), "source": image.get("src")}
                    for image in description_soup.findAll('img')
                ]
            }
            self.raw_data["feed"].append(item_dict)
        # from json import dumps
        # open("rss.json", "w").write(RSSFeed(**self.raw_data).json())
        # open("rss.json", "a").write(dumps(self.raw_data))
        return RSSFeed(**self.raw_data)
