Paste crawler
=============

A paste crawler that scrapes the websites, and stores it in a CouchDB
structure.
Use at own risk. Intended as a test for CouchDB, with the eventual integration
of ELK stack for searching.

## Usage
```
$ python crawl.py --help
usage: crawl.py [-h] [--site SITE] [-l sleeptime]

Crawler for pastbin like sites

optional arguments:
  -h, --help            show this help message and exit
  --site SITE           Only run on selected site. Must be present in config.
                        Expects name
  -l sleeptime, --loop sleeptime
                        Run in a loop with specified sleeptime. Should be 5
                        (minutes) or more

```

## Install
Install the needed requirements with pip (Gets the packages from pypi)
```
pip install -r requirements.txt
```

You can get up and running fast with docker, if you don't care much for
security. On a docker host, just run the following:
```
docker run klaemo/couchdb:latest
```
This will create a new container with a CouchDB instance, that has the default
port exposed. This will enable a fast setup for getting up and running fast.

Change the configuration file with the specific IP address, and you are up and
running.
