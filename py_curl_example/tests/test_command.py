'''
Created on 15 Aug 2016

@author: fressi
'''
import unittest


from py_curl_example import command


class TestGetHtm(unittest.TestCase):
    'Test case for get_html function'

    def test_get_required_html(self):
        'Test get_html function with required HTML and encoding'

        html = command.get_html(
            command.REQUIRED_URL, encoding=command.REQUIRED_ENCODING)

        self.assertTrue(html.endswith('</html>\n\n'), html[-30:])


class TestParseHtm(unittest.TestCase):
    'Test case for get_html function'

    def test_parse_required_html(self):
        'Test get_html function with required HTML and encoding'

        html = command.get_html(
            command.REQUIRED_URL, encoding=command.REQUIRED_ENCODING)
        page = command.parse_html(html)

        self.assertEqual('Classic Car Rescue - C5', page.title)
