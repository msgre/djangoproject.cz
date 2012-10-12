# -*- coding: utf-8 -*-
# vim: set et si ts=4 sw=4 enc=utf-8: 

"""
Sada pomocnych parsovacich trid, kterymi taham cerstve udaje do 
stranky s komunitou.
"""

import os
import re
import time
import urllib
import sys
from datetime import datetime
from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select
from czech import slugify
from django.template.defaultfilters import striptags, urlizetrunc

PROJECT_PATH = os.path.join(os.path.dirname(__file__), '..')

# konfigurace sablonovaciho systemu
from django.conf import settings
settings.configure(
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    TEMPLATE_DIRS=(os.path.abspath(os.path.join(PROJECT_PATH, 'templates/fetcher')), )
)
from django.template.loader import render_to_string
from django.template.loader import get_template


class NotImplemented(Exception):
    pass

class Fetcher(object):
    """
    Obecna trida, ktera resi stahnuti stranky a jeji zpracovani.
    """
    def __init__(self, url):
        self.url = url
        self.text, self.soup, self.data = None, None, None

    def fetch(self):
        f = urllib.urlopen(self.url)
        self.text = f.read()
        self.soup = Soup(self.text)
        f.close()
            
    def parse(self):
        raise NotImplemented

    def render(self):
        # jmeno sablony je odvozeno ze jmena sablony
        template_name = self.__class__.__name__.replace('Fetcher', '').lower()
        template_name = template_name + '.html'
        return render_to_string(
            template_name,
            {'data': self.data}
        )

    def process(self):
        self.fetch()
        if self.soup:
            self.parse()
            return self.render()
        # try:
        #     self.fetch()
        #     if self.soup:
        #         self.parse()
        #         return self.render()
        # except:
        #     return ''


class DjangopeopleFetcher(Fetcher):
    """
    Zpracuje stranku z webu http://djangopeople.net/cz/
    a vytahne z ni seznam, kde kazda polozka je tuple 
    (jmeno, url).
    """
    def parse(self):
        if not self.soup:
            return
        book = {}
        for a in select(self.soup, 'ul.detailsList li h3 a'):
            link = self.url.replace('/cz/', '') + a['href']
            xa = str(select(a, 'span.given-name')[0].string)
            xb = str(select(a, 'span.family-name')[0].string)
            name = u"%s %s" % (
                # select(a, 'span.given-name')[0].string.capitalize(),
                # select(a, 'span.family-name')[0].string.capitalize()
                xa.decode('utf-8'),
                xb.decode('utf-8')
            )
            key = name.split(u' ')
            key.reverse()
            key = slugify(u" ".join(key))
            book[key] = (name, link)
        keys = sorted(book.keys())
        self.data = [book[k] for k in keys]


class IrcFetcher(Fetcher):
    """
    Zpracuje stranku z webu http://botland.oebfare.com/logger/django-cs/
    a vytahne z ni seznam, kde kazda polozka je tuple (nick, message).
    """
    def parse(self):
        if not self.soup:
            return
        out = []
        for tr in select(self.soup, '#content table tr'):
            td = select(tr, 'td')
            if len(td) != 3:
                continue
            name = select(td[1], 'strong')[0].string
            msg = urlizetrunc(striptags(select(td[2], 'div')[0].renderContents()), 30)
            out.append((name, msg))
        self.data = out[:]


class DjangositesFetcher(Fetcher):
    """
    Zpracuje RSS z URL http://www.djangosites.org/rss/tag_full/czech
    a vytahne z ni seznam, kde kazda polozka je tuple 
    (jmeno webu, odkaz na web, odkaz na obrazek).
    Prvni polozka je nejnovejsi prirustek.
    """
    URL_FROM_DESCRIPTION = re.compile(r'\((http:[^\)]+)\)')

    def parse(self):
        if not self.soup:
            return
        sites = {}
        for item in select(self.soup, 'item'):
            name = select(item, 'title')[0].string.strip()
            description = select(item, 'description')[0].string
            m = self.URL_FROM_DESCRIPTION.search(description)
            if m:
                link = m.group(1)
            else:
                link = select(item, 'guid')[0].string.strip()
            img = select(item, 'enclosure')[0]['url']
            date = select(item, 'pubdate')[0].string.strip()
            try:
                d = time.strptime(date, '%a, %d %b %Y %H:%M:%S +1100')
            except ValueError:
                d = time.strptime(date, '%a, %d %b %Y %H:%M:%S +1000')
            _date = datetime(*d[:6])
            sites[_date] = (name, link, img)
        keys = sorted(sites.keys(), reverse=True)
        self.data = [sites[k] for k in keys]


URLS = {
    'djangopeople': ('http://djangopeople.net/cz/', DjangopeopleFetcher),
    'djangosites':  ('http://www.djangosites.org/rss/tag_full/czech', DjangositesFetcher),
    'irc':          ('http://botland.oebfare.com/logger/django-cs/', IrcFetcher)
}

if len(sys.argv) > 1 and sys.argv[1] in URLS:
    k = sys.argv[1]
    fetcher = URLS[k][1](URLS[k][0])
    sys.stdout.write(fetcher.process().encode('utf-8'))
