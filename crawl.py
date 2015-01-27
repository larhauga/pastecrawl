#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import random
import couchdb
import argparse
import requests
import subprocess
from models import Paste
from datetime import datetime
from BeautifulSoup import BeautifulSoup
import config

previous = []
couch = couchdb.Server(config.server)
try:
    db = couch.create(config.dbname)
except couchdb.http.PreconditionFailed as error:
    db = couch[config.dbname]


def get_archive(site):
    links = []
    r = requests.get(site['archive'], headers=config.header)

    if 'pastebin' in site['archive']:
        if "We have blocked your IP from accessing" in r.text:
            sys.exit("IP address has been banned")
        soup = BeautifulSoup(r.text)
        main = soup.find('table', { "class": "maintable" })
        for row in main.findAll('tr'):
            col = row.findAll('td')
            try:
                links.append(col[0].find('a').get('href')[1:])
            except:
                pass
    else:
        raise NotImplementedError('Parsing for this site not implemented: %s' % site['archive'])

    return links

def download(site, links):
    for link in links:
        if not link in previous:
            r = requests.get(site['raw'] % link, headers=config.header)
            paste = Paste(_id=link, content=r.text,
                    filetype=test_filetype(r.text), site=site['archive'])
            try:
                paste.store(db)
                print "Stored new object %s" % link
            except couchdb.http.ResourceConflict as error:
                print "Object %s allready stored: %s" % (link, error)
            time.sleep(random.uniform(0.2,2))

def test_filetype(content):
    with open('tempfile', 'w') as f:
        f.write(content.encode('utf-8'))

    output = subprocess.check_output('file tempfile'.split())
    subprocess.call('rm tempfile'.split())
    return output.strip().split(':')[1].strip()

def iterate(only_site=None):
    if only_site:
        s = filter(lambda x: only_site in x['archive'], config.sites)
        if s:
            print "Gathering values from site %s" % s['archive']
            download(s, get_archive(s))
        else:
            sys.exit('Site not configured')
    else:
        for site in config.sites:
            download(site, get_archive(site))

def main():
    parser = argparse.ArgumentParser(description="Crawler for pastbin like sites")
    parser.add_argument('--site',
            help="Only run on selected site. Must be present in config. Expects name")
    parser.add_argument('-l', '--loop', metavar='sleeptime', type=int,
            help="Run in a loop with specified sleeptime. Should be 5 (minutes) or more")

    args = parser.parse_args()
    try:
        if args.loop:
            while True:
                iterate(only_site=args.site)
                sleep(args.loop*60)
        else:
            iterate(only_site=args.site)
    except KeyboardInterrupt:
        print "Exiting..."

if __name__ == '__main__':
    main()
