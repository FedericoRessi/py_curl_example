'''
Created on 15 Aug 2016

@author: fressi
'''

import logging

import pycurl
import six


LOG = logging.getLogger(__name__)

REQUIRED_URL = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/' + \
               'viewtopic.php?t=12591'
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


def main():
    "My script entry point."

    get_html(REQUIRED_URL, encoding=REQUIRED_ENCODING)
