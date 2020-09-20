from .reader import Reader


# TODO: Add pretty html/pdf


def main():
    reader = Reader()
    try:
        reader.start()
    except Exception as e:
        print(f"Rss reader crashed from {type(e).__name__}. "
              "Consider using --verbose for more info")


if __name__ == '__main__':
    main()
