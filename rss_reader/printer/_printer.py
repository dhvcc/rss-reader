"""For info read __init__.py docstring"""
from colorama import Back, Fore, Style
from rss_parser.models import RSSFeed

from rss_reader.imports import json


class Printer:
    def __init__(self, rss: RSSFeed, rss_raw: dict = None):
        self.rss = rss
        self.rss_raw = rss_raw

    def none(self):
        """Empty method which is called if output argument is 'none'"""
        pass

    def console(self):
        print(
            f"\nFeed (RSS{self.rss.version or ''} {self.rss.language or ''}): {self.rss.title}"
        )
        print(self.rss.description)
        for item in self.rss.feed:
            print(f"\n\nTitle: {item.title}")
            if item.publish_date:
                print(f"Publication date: {item.publish_date}")
            if item.category:
                print(f"Category: {item.category}")
            if item.link:
                print(f"Link: {item.link}")
            print(f"\n{item.description}\n")
            if item.description_images:
                print("Description images:")
                for num, image in enumerate(item.description_images, 1):
                    print(f"[{num}][{image.alt}]: {image.source}")
            if item.description_links:
                print("Description links:")
                for num, link in enumerate(item.description_links, 1):
                    print(f"[{num}]: {link}")

    def colorized(self):
        # TODO: Wrap printer in a module and add colors.py that contains color scheme tuples
        print()
        print(Style.NORMAL, Back.WHITE, Fore.BLACK, end="\b\b")
        print(
            f"Feed (RSS{self.rss.version or ''} {self.rss.language or ''}): {self.rss.title}",
            Style.RESET_ALL,
        )
        print(Style.NORMAL, Back.WHITE, Fore.BLACK, end="\b\b")
        print(self.rss.description, Style.RESET_ALL)
        for item in self.rss.feed:
            print(2 * "\n")
            print(Style.NORMAL, Back.WHITE, Fore.BLACK, end="\b\b")
            print(f"Title: {item.title}", Style.RESET_ALL)

            if item.publish_date:
                print(Style.BRIGHT, Fore.WHITE, end="\b")
                print(f"Publication date: {item.publish_date}", Style.RESET_ALL)
            if item.category:
                print(Style.BRIGHT, Fore.WHITE, end="\b")
                print(f"Category: {item.category}", Style.RESET_ALL)
            if item.link:
                print(Style.BRIGHT, Fore.WHITE, end="\b")
                print(f"Link: {item.link}", Style.RESET_ALL)

            print(Style.BRIGHT, Fore.YELLOW)
            print(f"{item.description}\n", Style.RESET_ALL)

            if item.description_images:
                print(Style.BRIGHT, Fore.WHITE, end="\b")
                print("Description images:")
                for num, image in enumerate(item.description_images, 1):
                    print(f"[{num}][{image.alt}]: {image.source}")
            if item.description_links:
                print("Description links:")
                for num, link in enumerate(item.description_links, 1):
                    print(f"[{num}]: {link}")
            print(Style.RESET_ALL, end="")

    def json(self):
        if self.rss_raw:
            print(json.dumps(self.rss_raw, indent=4))
        else:
            # If raw dict rss was not provided then create dict and dump it
            # dumps indent does not work on str
            loaded: dict = json.loads(self.rss.json())
            print(json.dumps(loaded, indent=4))
