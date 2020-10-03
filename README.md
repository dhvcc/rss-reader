# Rss reader

[![Downloads](https://pepy.tech/badge/rss-reader)](https://pepy.tech/project/rss-reader)
[![Downloads](https://pepy.tech/badge/rss-reader/month)](https://pepy.tech/project/rss-reader/month)
[![Downloads](https://pepy.tech/badge/rss-reader/week)](https://pepy.tech/project/rss-reader/week)

[![PyPI version](https://badge.fury.io/py/rss-reader.svg)](https://pypi.org/project/rss-reader/)
[![GitHub license](https://img.shields.io/github/license/dhvcc/rss-reader)](https://github.com/dhvcc/rss-reader/blob/master/LICENSE)

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

# Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

`pre-commit` usage is highly recommended

install hooks via `pre-commit install -t=pre-commit -t=pre-push`

# License

[MIT](https://github.com/dhvcc/rss-reader/blob/master/LICENSE)

# Documentation

1. [Installation](https://github.com/dhvcc/rss-reader#installation)
    1. [From PyPi](https://github.com/dhvcc/rss-reader#from-pypi)
    2. [From GitHub](https://github.com/dhvcc/rss-reader#from-github)
2. [Usage](https://github.com/dhvcc/rss-reader#usage)
    1. [Notes](https://github.com/dhvcc/rss-reader#notes)
    2. [Examples](https://github.com/dhvcc/rss-reader#examples)
3. [Config](https://github.com/dhvcc/rss-reader#config)
    1. [Info](https://github.com/dhvcc/rss-reader#info)
        1. [Config source priority](https://github.com/dhvcc/rss-reader#config-argument-sources-are-prioritized)
        2. [Warning](https://github.com/dhvcc/rss-reader#warning)
    2. [Command-line arguments](https://github.com/dhvcc/rss-reader#command-line-arguments)
    3. [INI configs](https://github.com/dhvcc/rss-reader#ini-configs)
    4. [Environment variables](https://github.com/dhvcc/rss-reader#environment-variables)
        1. [Using environment variables](https://github.com/dhvcc/rss-reader#using-environment-variables)

# Installation

### From PyPi

```bash
pip install rss-reader
```

### From GitHub

```bash
git clone https://github.com/dhvcc/rss-reader.git
cd rss-reader
pip install .
```

### Extras

You can install extra dependencies, such as `speedups` or `dev`

```bash
pip install rss-reader[dev]
# or
pip install .[speedups]
```

# Usage

## Notes

**IMPORTANT** `rss-reader 3.1` no longer supports `fb2` format and caching

You can mute console output with `-o none`. It may be useful if you want to convert only

## Examples

Converting feed to html and muting console output. Feed is limited to 2 items
```bash
rss-reader https://feedforall.com/sample.xml --output none --convert html --limit 2
```

This will generate colorized console output and the feed will be also converted to epub
```bash
rss-reader /path/to/your/file.xml -o colorized -c epub
```

This will generate default console output and the feed will be converted to pdf and saved in /my/dir/filename.pdf
```bash
rss-reader /path/to/your/file.xml -c pdf --convert-dir /my/dir --convert-file filename.pdf
```

# Config

## Info

#### Config argument sources are prioritized

 1. Command-line arguments
 2. Local `.rss-reader` config
 3. Environment variables
 4. Global `{HOME}/.rss-reader` config

#### Warning

`source`, `verbose`, `limit` and `version` arguments can be set only as cli arguments


## Command-line arguments

To view help on cli arguments you can run `rss-reader --help`

## INI configs

Every argument is optional if config and will be grabbed from other source if not present
The syntax for config is the following:

```ini
[rss-reader]
OUTPUT =
CONVERT =
CONVERT_DIR =
CONVERT_FILE =
```

Global config should be located in your home folder and named `.rss-reader`

## Environment variables

Env vars should be prefixed with `RSS_READER_`, for example, `RSS_READER_OUTPUT`

### Using environment variables

[Windows](http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-windows-command-line-and-registry/)

[Linux](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)