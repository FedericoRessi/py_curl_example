'''
Created on 15 Aug 2016

@author: fressi
'''

import logging

import bs4
import pycurl
import six
try:
    # Python3
    import urllib.parse as urlparse
except ImportError:
    # Python2
    import urlparse


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

    LOG.info('Get page from url: %s', url)

    html = six.BytesIO()
    curl = pycurl.Curl()
    try:
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, html)
        curl.perform()
        result = to_string(html.getvalue(), encoding=encoding)
        LOG.info('Page downloaded: %s', url)
        return result

    finally:
        curl.close()


def get_page_entries(url, encoding=None):
    "Parses given html."

    new_ulrs = {1: url}
    url_id = 1
    entry_id = 0

    while new_ulrs:
        url = new_ulrs.pop(url_id, None)
        url_id += 1
        if not url:
            continue

        html = get_html(url=url, encoding=encoding)
        soup = bs4.BeautifulSoup(html, 'html.parser')

        for entry in find_posted_entries(soup):
            yield (entry_id,) + entry
            entry_id += 1

        for new_url_id, new_url in find_page_links(soup):
            if new_url_id >= url_id and new_url_id not in new_ulrs:
                LOG.debug('New link found on page: %s -> %s', url, new_url)
                new_ulrs[new_url_id] = urlparse.urljoin(url, new_url)


def find_page_links(soup):
    "Find all pages liks."
    for span in soup.find_all('span'):
        if span.get('class') == ['gensmall']:
            for a in span.find_all('a'):
                url = a.get('href')
                if url:
                    try:
                        url_id = int(a.get_text())
                    except ValueError:
                        continue
                    else:
                        yield url_id, url


def find_posted_entries(table):
    "Find all posted entries."
    for tr in table.find_all('tr'):
        fields = {}
        for td in tr.find_all('td'):
            for span in td.find_all('span'):
                cls = span.get('class')
                if cls:
                    fields[cls[0]] = span.get_text()

        name = fields.get('name')
        if name:
            post_details = fields.get('postdetails', '')
            if post_details:
                post_details = post_details.split('Posted:', 1)[1]
                post_details = post_details.strip()
                post_details = post_details.split('Post subject:', 1)[0]
                post_details = post_details.strip()
            post_body = fields.get('postbody', "")
            LOG.debug('%s: %s', name, post_details)
            yield name, post_details, post_body


class Page(object):
    "Model class returned by parse_html function."

    def __init__(self):
        self.entries = []


def main():
    "My script entry point."

    get_page_entries(REQUIRED_URL, encoding=REQUIRED_ENCODING)
