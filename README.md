# Rss reader

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

1)You can install this rss-reader using python's standard package-management system 
[pip](<https://pip.pypa.io/en/stable/installing/>)

Just run this command from terminal


    pip3 install rss-reader


2)You can [download](<https://pypi.org/project/rss-reader/#files>)
it manually from PyPI and then run ``python3 setup.py install`` in ``.../rss-reader-*version*/``


# Usage 


    usage: rss-reader [-h] [--version] [--verbose] [--date DATE] [--clear-cache]
                      [--json] [--to-html] [--to-pdf] [--to-fb2] [--to-epub]
                      [--limit LIMIT] [--colorize]
                      [source [source ...]]
    
    Pure Python command-line RSS reader.
    
    positional arguments:
      source         RSS URL
    
    optional arguments:
      -h, --help     show this help message and exit
      --version      print version info
      --verbose      output verbose status messages
      --date DATE    print cached news from provided date in %Y%m%d format
      --clear-cache  clear news cache
      --json         print the news as JSON in stdout
      --to-html      convert news to .html format and make a new file called
                     news.html
      --to-pdf       convert news to .pdf format and make a new file called
                     news.pdf
      --to-fb2       convert news to .fb2 format and make a new file called
                     news.fb2
      --to-epub      convert news to .epub format and make a new file called
                     news.epub
      --limit LIMIT  limit news topics if this parameter is provided
      --colorize     print the result of the utility in colorized mode

# Important

**1)Arguments are prioritized from top to bottom. This means that the utility will first parse the -h/--help argument, then --version, then --verbose, then --date, and so on**

**2)There is no need to enter the source argument if the --date or the --clear-cache arguments were entered. The utility will just ignore it**

**3)The --limit argument DOES affect any kind of news output**

**4)The --date argument DOES affect the --json and the --to-(html/pdf/fb2/epub) arguments**

**5)The --colorize argument DOES NOT affect the --json and the --to-(html/pdf/fb2/epub) arguments**

**6)Data is stored in {HOME}/rss_reader folder**

## JSON structure


    {
        "Feed title": "(Feed title)",
        "News": [
            {
                "Title": "(News title)",
                "Link": "(News link)",
                "Publishing date": "(publishing date)",
                "Category": "(category)",
                "Description": "(description)",
                "Description links": [
                    "(link)",
                    "(link)",
                    ...
                ],
                "Description images": [
                    {
                        "Title": "(image title)",
                        "Link": "(image link)"
                    },
                    {
                        "Title": "(image title)",
                        "Link": "(image link)"
                    },
                    ...
                ]
            },
            {
                "Title": "(News title)",
                "Link": "(News link)",
                "Publishing date": "(publishing date)",
                "Category": "(category)",
                "Description": "(description)",
                "Description links": [
                    "(link)",
                    "(link)",
                    ...
                ],
                "Description images": [
                    {
                        "Title": "(image title)",
                        "Link": "(image link)"
                    },
                    {
                        "Title": "(image title)",
                        "Link": "(image link)"
                    },
                    ...
                ]
            },
            ...
        ]
    }

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

`pre-commit` usage is highly recommended

install hooks via `pre-commit install -t=pre-commit -t=pre-push`

## License

`MIT <https://choosealicense.com/licenses/mit/>`__