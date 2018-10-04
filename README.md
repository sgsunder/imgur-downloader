**Quickly download Imgur albums**

## Installation

`pip3 install imgurdownloader`

## Configuration

You need an Imgur API Key, this can be stored in the environment variable
`IMGUR_API_KEY` for convenience

## Help

From `imgur-downloader --help`:
```
usage: imgur-downloader [-h] [-q] [-d DIRECTORY] [--auth TOKEN]
                           [album [album ...]]

Download Imgur Albums

positional arguments:
  album                 URL to Imgur Album (Multiple Allowed)

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet, --no-progress
                        Do not show a progress bar for downloads
  -d DIRECTORY, --dir DIRECTORY
                        Directory to save albums to (defaults to current
                        working directory)
  --auth TOKEN          Imgur API Client-ID Token
```

## Building

```
python3 setup.py sdist bdist_wheel
twine upload dist/*
```