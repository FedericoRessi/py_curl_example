'''
Created on 15 Aug 2016

@author: fressi
'''
import unittest

import pycurl
import six


REQUIRED_URL = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/' + \
               'viewtopic.php?t=12591'


class TestPyCurl(unittest.TestCase):
    "Test case for PyCurl library"

    def test_connect_some_web_site(self):
        "Test with connecting to pycurl with a know web page."
        buf = six.BytesIO()
        curl = pycurl.Curl()
        self.addCleanup(curl.close)
        curl.setopt(curl.URL, 'http://pycurl.io/')
        curl.setopt(curl.WRITEDATA, buf)

        curl.perform()
        body = buf.getvalue()

        self.assertTrue(body)

    def test_connect_required_web_site(self):
        "Test with connecting to pycurl with required web page."
        buf = six.BytesIO()
        curl = pycurl.Curl()
        self.addCleanup(curl.close)
        curl.setopt(curl.URL, REQUIRED_URL)
        curl.setopt(curl.WRITEDATA, buf)

        curl.perform()
        body = buf.getvalue()

        self.assertTrue(body)
