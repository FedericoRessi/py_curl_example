'''
Created on 15 Aug 2016

@author: fressi
'''

import logging

import bs4
import pycurl
import six


LOG = logging.getLogger(__name__)

REQUIRED_URL = u'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/' + \
               u'viewtopic.php?t=12591'
REQUIRED_ENCODING = 'iso-8859-1'


if six.PY2:
    def to_string(obj, encoding=None):
        "Wrap str function ignoring enconding parameter."
        return str(obj)

else:
    to_string = str


def get_html(url, encoding=None):
    "Gets an HTML from ginven url and translating it to a string."

    html = six.BytesIO()
    curl = pycurl.Curl()
    try:
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, html)
        curl.perform()
        return to_string(html.getvalue(), encoding=encoding)

    finally:
        curl.close()


def parse_html(html):
    "Parses given html."
    page = Page()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    page.title = soup.title.string
    return page


class Page(object):
    "Model class returned by parse_html function."

    title = None


def main():
    "My script entry point."

    html = get_html(REQUIRED_URL, encoding=REQUIRED_ENCODING)
    parse_html(html)
