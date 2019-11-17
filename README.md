## CLI RSS reader
CLI rss reader is a utility which makes it easy to read RSS feed from command line
## What is RSS?
RSS stands for “really simple syndication,” or, depending on who you ask, “rich site summary.” At its heart, RSS is just simple text files with basic updated information—news pieces, articles, that sort of thing. That stripped-down content is usually plugged into what is called a “feed reader” or an interface that quickly converts the RSS text files into a stream of the latest updates from around the web.
## Installation
Use the package manager [pip3](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) to install this RSS reader.

```
pip3 install rss-reader
```
## Usage
    usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source
    
    Pure Python command-line RSS reader.
    
    positional arguments:
      source         RSS URL
    
    optional arguments:
      -h, --help     show this help message and exit
      --version      Print version info
      --json         Print result as JSON in stdout
      --verbose      Outputs verbose status messages
      --limit LIMIT  Limit news topics if this parameter provided
 
## JSON structure
     {
         "(Feed title)": [
             {
                 "Title": "(news title)",
                 "Link": "(news link)",
                 "Publishing date": "(news publishing date)",
                 "Description": "(news description)",
                 "Description links": [
                     "(news description link)",
                     "(news description link)",
                     ...
                 ],
                 "Description images": [
                     {
                         "Title": "(news description image's title)",
                         "Link": "(news description image's link)"
                     },
                     {
                         "Title": "(news description image's title)",
                         "Link": "(news description image's link)"
                     },
                     ...
                     
                 ]
             },
             {
                 "Title": "(news title)",
                 "Link": "(news link)",
                 "Publishing date": "(news publishing date)",
                 "Description": "(news description)",
                 "Description links": [
                     "(news description links)"
                 ],
                 "Description images": [
                     {
                         "Title": "(news description image's title)",
                         "Link": "(news description image's link)"
                     }
                 ]
             },
             ...
         ]
     }
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
## License
[MIT](https://choosealicense.com/licenses/mit/)
