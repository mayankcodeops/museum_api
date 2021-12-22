import unittest
from unittest.mock import Mock, patch
import json
import os
from config import config
import logging
import tempfile

from src.reporter.converter import generate_pdf

fixture_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/')
test_rep_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_reports/')
logging.basicConfig(filename='testing.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=config['testing'].LOG_LEVEL)


class TestMTMLGenerator(unittest.TestCase):
    def setUp(self):
        self.pdf_converter = generate_pdf.PDFConverter()

    @unittest.skip('Not implemented PDF file creation unit test')
    def test_convert_to_pdf_from_html_file_created(self):
        pass

    @unittest.skip('Not implemented PDF file match unit test')
    def test_convert_to_pdf_from_html_file_match(self):
        pass


if __name__ == '__main__':
    unittest.main()
