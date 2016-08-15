'''
Created on 15 Aug 2016

@author: fressi
'''
import unittest


from py_curl_example import command


class TestGetHtm(unittest.TestCase):
    'Test case for get_html function'

    def test_get_html(self):
        'Test get_html function with required HTML and encoding'

        html = command.get_html(
            command.REQUIRED_URL, encoding=command.REQUIRED_ENCODING)

        self.assertTrue(html.endswith('</html>\n\n'), html[-30:])


class TestParseHtm(unittest.TestCase):
    'Test case for get_html function'

    def test_get_entries(self):
        'Test get_html function with required HTML and encoding'

        entries = list(command.get_page_entries(
            command.REQUIRED_URL, encoding=command.REQUIRED_ENCODING))

        self.assertEqual(127, len(entries))
