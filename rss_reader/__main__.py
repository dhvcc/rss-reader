from .reader import Reader
import logging

# TODO: Add pretty html/pdf
logger = logging.getLogger("rss-reader")


def main():
    reader = Reader()
    try:
        reader.start()
    except Exception as e:
        logger.exception(e)
        print(f"Rss reader crashed from {type(e).__name__}")
        if not reader.config.verbose:
            print("Consider using --verbose for more info")


if __name__ == '__main__':
    main()
