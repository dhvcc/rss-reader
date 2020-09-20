# Rss reader WIP

[![Downloads](https://pepy.tech/badge/rss-reader)](https://pepy.tech/project/rss-reader)
[![Downloads](https://pepy.tech/badge/rss-reader/month)](https://pepy.tech/project/rss-reader/month)
[![Downloads](https://pepy.tech/badge/rss-reader/week)](https://pepy.tech/project/rss-reader/week)

[![Code checks](https://github.com/dhvcc/rss-reader/workflows/Code%20checks/badge.svg)](https://github.com/dhvcc/rss-reader/actions?query=workflow%3A%22Code+checks%22)
[![Pypi publish](https://github.com/dhvcc/rss-reader/workflows/Pypi%20publish/badge.svg)](https://github.com/dhvcc/rss-reader/actions?query=workflow%3A%22Pypi+publish%22)

## What is this?

rss-reader is a command line utility that allows you to view RSS feeds

## What is RSS?

RSS stands for “Really Simple Syndication,”
or, depending on who you ask, “Rich Site Summary.” At it's heart, RSS is
just simple text files with basic updated information—news pieces,
articles, that sort of thing. That stripped-down content is usually
plugged into what is called a “feed reader” or an interface that quickly
converts the RSS text files into a stream of the latest updates from
around the web.

# Installation

1. Using pip 
```bash
pip install rss-reader
```

2. Using Git and GitHub
```bash
git clone https://github.com/dhvcc/rss-reader.git
cd rss-reader
pip install .
```

## Usage

**Notice** that you can mute console output with `-o none`. It may be useful if you want to convert only

```
usage: rss-reader [-h] [--version] [--verbose] [-d DATE] [--clear-cache] [-o {console,colorized,json,none}] [-c {json,html,pdf,fb2,epub}] [--convert-dir CONVERT_DIR] [--convert-file CONVERT_FILE] [--dont-cache] [-l LIMIT] [source]

Pure Python command-line RSS reader.

positional arguments:
  source                RSS source FILE/URL. Ignored if --date/--clear-cache arguments are passed

optional arguments:
  -h, --help            show this help message and exit
  --version             print version info
  --verbose             output verbose status messages
  -d DATE, --date DATE  print cached news from provided date in %Y%m%d format
  --clear-cache         clear news cache
  -o {console,colorized,json,none}, --output {console,colorized,json,none}
                        console output type
  -c {json,html,pdf,fb2,epub}, --convert {json,html,pdf,fb2,epub}
                        convert feed and save as a file
  --convert-dir CONVERT_DIR
                        convert output dir path instead of {home}/rss_reader/output
  --convert-file CONVERT_FILE
                        convert output filename
  --dont-cache          don't cache the output
  -l LIMIT, --limit LIMIT
                        limit news topics if this parameter is provided
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

`pre-commit` usage is highly recommended

install hooks via `pre-commit install -t=pre-commit -t=pre-push`

## License

`MIT <https://choosealicense.com/licenses/mit/>`__
