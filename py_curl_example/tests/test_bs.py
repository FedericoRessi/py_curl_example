'''
Created on 15 Aug 2016

@author: fressi
'''

import os
import unittest

import bs4


HTML_DOC = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters;
and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


TESTS_DIR = os.path.dirname(__file__)
REQUIRED_WEB_PAGE = os.path.join(TESTS_DIR, 'required_page.html')


class TestBeautifulSoup(unittest.TestCase):
    "Test case for bs4 library"

    def test_parse_page(self):
        "Test parsing a know web page."
        soup = bs4.BeautifulSoup(HTML_DOC, 'html.parser')

        self.assertEqual('title', soup.title.name)
        self.assertEqual("The Dormouse's story", soup.title.string)
        self.assertEqual('head', soup.title.parent.name)

    def test_parse_required_page(self):
        "Test parsing required web page."

        with open(REQUIRED_WEB_PAGE, encoding='iso-8859-1') as html_file:
            html = html_file.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')

        self.assertEqual('title', soup.title.name)
        self.assertEqual("Classic Car Rescue - C5", soup.title.string)
        self.assertEqual('meta', soup.title.parent.name)
