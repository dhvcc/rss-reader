# Rss reader

It is a command line utility that allows you to view RSS feeds

You can also convert RSS feeds to `html/pretty-html`/`pdf/pretty-pdf`/`epub` for more convenient reading

Command-line arguments, local and global INI configs, environment variables **are supported**

## What is RSS?

RSS stands for “Really Simple Syndication,”
or, depending on who you ask, “Rich Site Summary.” At it's heart, RSS is
just simple text files with basic updated information—news pieces,
articles, that sort of thing. That stripped-down content is usually
plugged into what is called a “feed reader” or an interface that quickly
converts the RSS text files into a stream of the latest updates from
around the web.

# Documentation

1. [Installation](https://dhvcc.github.io/rss-reader#installation)
2. [Usage](https://dhvcc.github.io/rss-reader#usage)
    1. [Notes](https://dhvcc.github.io/rss-reader#notes)
    2. [Examples](https://dhvcc.github.io/rss-reader#examples)
3. [Config](https://dhvcc.github.io/rss-reader#config)
    1. [Info](https://dhvcc.github.io/rss-reader#info)
        1. [Config source priority](https://dhvcc.github.io/rss-reader#config-argument-sources-are-prioritized)
        2. [Warning](https://dhvcc.github.io/rss-reader#warning)
    2. [Command-line arguments](https://dhvcc.github.io/rss-reader#command-line-arguments)
    3. [INI configs](https://dhvcc.github.io/rss-reader#ini-configs)
    4. [Environment variables](https://dhvcc.github.io/rss-reader#environment-variables)
        1. [Using environment variables](https://dhvcc.github.io/rss-reader#using-environment-variables)

# Installation

### Using pip
```bash
pip install rss-reader
```

### Using Git and GitHub
```bash
git clone https://dhvcc.github.io/rss-reader.git
cd rss-reader
pip install .
```

### Extras

You can install extra dependencies, such as `speedups` or `dev`

```
pip install rss-reader[dev]
# or
pip install .[speedups]
```

# Usage

## Notes

**IMPORTANT** `rss-reader 3.1` no longer supports `fb2` format and caching

You can mute console output with `-o none`. It may be useful if you want to convert only

## Examples

**Notice that --pretty is a separate agrument as it affects html and pdf(pdf is generated from html)**

Convert feed to html and mute console output. Feed is limited to 2 items
```bash
rss-reader https://feedforall.com/sample.xml --output none --convert html --limit 2
```

Parse local xml file, generate colorized console output and convert feed to epub
```bash
rss-reader /path/to/your/file.xml -o colorized -c epub
```

Parse local xml file, generate default console output, convert feed to pdf and saved as /my/dir/filename.pdf
```bash
rss-reader /path/to/your/file.xml -c pdf --convert-dir /my/dir --convert-file filename.pdf
```

Mute console output and convert feed to pretty html with bootstrap
```bash
rss-reader /https://feedforall.com/sample.xml -o none -c html --pretty
```

Output colorized feed to console and convert it to pretty pdf (html with bootstrap)
```bash
rss-reader https://feedforall.com/sample.xml -o colorized -c pdf --pretty
```

# Config

## Info

#### Config argument sources are prioritized

 1. Command-line arguments
 2. Local `.rss-reader` config
 3. Environment variables
 4. Global `{HOME}/.rss-reader` config

#### Warning

`source`, `verbose`, `limit`, `pretty` and `version` arguments can be set only as cli arguments


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
