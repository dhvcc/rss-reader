CLI RSS reader
--------------

CLI rss reader is a utility which makes it easy to read RSS feed from
command line ## What is RSS? RSS stands for “really simple syndication,”
or, depending on who you ask, “rich site summary.” At its heart, RSS is
just simple text files with basic updated information—news pieces,
articles, that sort of thing. That stripped-down content is usually
plugged into what is called a “feed reader” or an interface that quickly
converts the RSS text files into a stream of the latest updates from
around the web. ## Installation Use the package manager
`pip3 <https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/>`__
to install this RSS reader.

::

    pip3 install rss-reader

**or**

You can `download <[https://pypi.org/project/rss-reader/#files](https://pypi.org/project/rss-reader/#files)>`__
it manually and run ``python3 setup.py install`` in
``.../rss-reader-1.3.0/``

Requirements
------------
Python version 3.6 and later

Usage 
-----

::

    usage: rss-reader [-h] [--version] [--json] [--verbose]
    [--limit LIMIT] source

    Pure Python command-line RSS reader.

    positional arguments:
      source         RSS URL

    optional arguments:
      -h, --help     show this help message and exit
      --version      Print version info
      --json         Print result as JSON in stdout
      --verbose      Outputs verbose status messages
      --limit LIMIT  Limit news topics if this parameter provided

JSON structure
--------------

::

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

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

License
-------

`MIT <https://choosealicense.com/licenses/mit/>`__
