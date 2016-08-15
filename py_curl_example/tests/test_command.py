'''
Created on 15 Aug 2016

@author: fressi
'''
import os
import tempfile
import unittest

from py_curl_example import command


class TestCommand(unittest.TestCase):
    'Test case for command module'

    def test_get_html(self):
        'Test get_html function with required HTML and encoding'

        html = command.get_html(
            command.REQUIRED_URL, encoding=command.REQUIRED_ENCODING)

        self.assertTrue(html.endswith('</html>\n\n'), html[-30:])

    def test_get_page_entries(self):
        'Test get_html function with required HTML and encoding'

        entries = list(command.get_page_entries(
            command.REQUIRED_URL, encoding=command.REQUIRED_ENCODING))

        self.assertEqual(127, len(entries))

    def test_main(self):
        "Test main function"
        output_fd, output_path = tempfile.mkstemp()
        self.addCleanup(os.remove, output_path)
        os.close(output_fd)

        command.main(file_name=output_path)

        with open(output_path, 'rt', encoding='utf-8') as input_file:
            row0 = input_file.readline()
            self.assertTrue(
                row0.startswith(
                    '0;"Rick";"Mon Sep 24, 2012 4:53 pm";' +
                    '"Tonight, 8pm, might be worth a look...?\\r\\n\\n\\nRJ'),
                repr(row0))
