'''
Created on 15 Aug 2016

@author: fressi
'''

import csv
import logging
from urllib.parse import urljoin

import bs4
import pycurl
import six


LOG = logging.getLogger(__name__)

REQUIRED_URL = u'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/' + \
               u'viewtopic.php?t=12591'
REQUIRED_ENCODING = 'iso-8859-1'


def get_html(url, encoding=None):
    "Gets an HTML from ginven url and translating it to a string."

    LOG.info('Get page from url: %s', url)

    html = six.BytesIO()
    curl = pycurl.Curl()
    try:
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, html)
        curl.perform()
        result = str(html.getvalue(), encoding=encoding)
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

        html = get_html(url=url, encoding=encoding)
        soup = bs4.BeautifulSoup(html, 'html.parser')

        for entry in find_posted_entries(soup):
            yield (entry_id,) + entry
            entry_id += 1

        for new_url_id, new_url in find_page_links(soup):
            if new_url_id >= url_id and new_url_id not in new_ulrs:
                LOG.debug('New link found on page: %s -> %s', url, new_url)
                new_ulrs[new_url_id] = urljoin(url, new_url)


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
            post_body = repr(fields.get('postbody', ""))[1:-1]
            LOG.debug('%s: %s', name, post_details)
            yield name, post_details, post_body


def main(file_name='posts.csv'):
    "My script entry point."

    with open(file_name, 'wt', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=';', escapechar='\\', doublequote=True,
            quoting=csv.QUOTE_NONNUMERIC)

        for entry in get_page_entries(url=REQUIRED_URL,
                                      encoding=REQUIRED_ENCODING):
            csv_writer.writerow(entry)
