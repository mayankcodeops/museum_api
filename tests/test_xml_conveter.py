import unittest
from unittest.mock import Mock, patch
import json
import os
from config import config
import logging
import tempfile

from src.reporter.converter import generate_xml

fixture_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/')
test_rep_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_reports/')
logging.basicConfig(filename='testing.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=config['testing'].LOG_LEVEL)


@unittest.skip('Not Implement Test Class: TestXMLGenerator')
class TestXMLGenerator(unittest.TestCase):
    def setUp(self):
        self.xml_converter = generate_xml.XMLConverter()
        # TODO Load the CSV fixture

    def test_convert_row(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
