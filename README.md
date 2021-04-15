# Rss reader

[![Downloads](https://pepy.tech/badge/rss-reader)](https://pepy.tech/project/rss-reader)
[![Downloads](https://pepy.tech/badge/rss-reader/month)](https://pepy.tech/project/rss-reader/month)
[![Downloads](https://pepy.tech/badge/rss-reader/week)](https://pepy.tech/project/rss-reader/week)

[![PyPI version](https://img.shields.io/pypi/v/rss-reader)](https://pypi.org/project/rss-reader)
[![Python versions](https://img.shields.io/pypi/pyversions/rss-reader)](https://pypi.org/project/rss-reader)
[![Wheel status](https://img.shields.io/pypi/wheel/rss-reader)](https://pypi.org/project/rss-reader)
[![License](https://img.shields.io/pypi/l/rss-reader?color=success)](https://github.com/dhvcc/rss-reader/blob/master/LICENSE)
[![GitHub Pages](https://badgen.net/github/status/dhvcc/rss-reader/gh-pages?label=docs)](https://dhvcc.github.io/rss-reader#documentation)

[![Code checks](https://github.com/dhvcc/rss-reader/workflows/Code%20checks/badge.svg)](https://github.com/dhvcc/rss-reader/actions?query=workflow%3A%22Code+checks%22)
[![Pypi publish](https://github.com/dhvcc/rss-reader/workflows/Pypi%20publish/badge.svg)](https://github.com/dhvcc/rss-reader/actions?query=workflow%3A%22Pypi+publish%22)

## What is this?

`rss-reader` is a command line utility that allows you to view RSS feeds

You can also convert RSS feeds to `html`/`pdf`/`epub` for more convenient reading

Command-line arguments, local and global INI configs, environment variables **are supported**

## What is RSS?

RSS stands for “Really Simple Syndication,”
or, depending on who you ask, “Rich Site Summary.” At it's heart, RSS is
just simple text files with basic updated information—news pieces,
articles, that sort of thing. That stripped-down content is usually
plugged into what is called a “feed reader” or an interface that quickly
converts the RSS text files into a stream of the latest updates from
around the web.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Install dependencies with `poetry install` (`pip install poetry`)

`pre-commit` usage is highly recommended. To install hooks run

```bash
poetry run pre-commit install -t=pre-commit -t=pre-push
```

## License

[GPLv3](https://github.com/dhvcc/rss-reader/blob/master/LICENSE)
