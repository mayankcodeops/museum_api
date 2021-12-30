import unittest
from unittest.mock import Mock, patch
import json
import os
from config import config
import logging
import tempfile


from src.reporter.helpers.fetch_response import fetch_response
from src.reporter.converter import generate_html
from .test_mock_server import start_mock_server, get_free_port

fixture_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/')
test_rep_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_reports/')
logging.basicConfig(filename='testing.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=config['testing'].LOG_LEVEL)


class TestMTMLGenerator(unittest.TestCase):
    def setUp(self):
        self.endpoint = 'collection/v1/objects/1'
        self.headers = {'Accept': '*/*', 'Content-Type': 'application/json'}
        self.mock_server_port = get_free_port()
        self.mock_url = 'http://localhost:{port}/'.format(port=self.mock_server_port)
        start_mock_server(self.mock_server_port)

        try:
            f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/resp.json'))
        except FileNotFoundError as fnfe:
            logging.exception(f"Could not load JSON mock data for TestHTMLGenerator: {fnfe.args[-1]}")
        else:
            self.json_data = json.load(f)
        finally:
            f.close()
        self.df = self.generate_dataframe()
        self.html_converter = generate_html.HTMLConverter()

    def generate_dataframe(self):
        import pandas as pd
        with patch.dict('src.reporter.helpers.fetch_response.__dict__', {'BASE_URL': self.mock_url}):
            artifacts: list[dict] = list(
                map(lambda objectid: fetch_response(self.endpoint, header=self.headers)
                    .json(),
                    list(range(1, config['testing'].API_RESP_LIMIT + 1))))

        df1 = pd.json_normalize(artifacts).drop(columns=['constituents'])

        meta = list(df1.keys())
        meta.remove('additionalImages')

        df2 = pd.json_normalize(artifacts, record_path=['constituents'], meta=meta, errors='ignore')
        df2 = df2.iloc[:, list(range(6, 61)) + list(range(0, 6))]
        return df2

    def test_convert_to_html_from_df_file_created(self):
        with tempfile.TemporaryDirectory(dir=test_rep_dir) as temp_dir:
            self.html_converter.convert(temp_dir, 'test_html.html', self.df)
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'test_html.html')))

    def test_convert_to_html_from_df_file_match(self):
        with tempfile.TemporaryDirectory(dir=test_rep_dir) as temp_dir:
            self.html_converter.convert(temp_dir, 'test_html.html', self.df)
            with open(os.path.join(fixture_dir, os.path.join(fixture_dir, 'museum.html'))) as file:
                original_html = file.read()
                gen_html_file = open(os.path.join(temp_dir, 'test_html.html'))
                generated_html = gen_html_file.read()
                gen_html_file.close()
                self.assertEqual(original_html, generated_html)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
