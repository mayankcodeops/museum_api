import logging
import os.path
import unittest
import json
from unittest.mock import Mock, patch

from config import config
from src.reporter.helpers.fetch_response import fetch_response
from .test_mock_server import start_mock_server, get_free_port

logging.basicConfig(filename='testing.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=config['testing'].LOG_LEVEL)


class APIIntegrationContract(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = config['testing'].BASE_URL
        self.endpoint = 'collection/v1/objects/1'
        self.headers = {'Accept': '*/*', 'Content-Type': 'application/json'}

    def test_integration_contract(self):
        actual_resp = fetch_response(self.endpoint, header=self.headers)
        actual_keys = actual_resp.json().keys()
        logging.debug(f'Response Status: {actual_resp.status_code}')
        logging.debug(f'Actual API resp keys: {actual_keys}')
        # call mocked requests.get
        try:
            f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/resp.json'))
        except FileNotFoundError as fnfe:
            logging.exception(f"Could not load JSON mock data for API Integration Test: {fnfe.args[-1]}")
        else:
            json_data = json.load(f)
            with patch('src.reporter.helpers.fetch_response.requests.get') as mock_get:
                mock_get.return_value.ok = True
                mock_get.return_value.json.return_value = json_data

                mocked_resp = fetch_response(self.endpoint, header=self.headers)
                mocked_keys = mocked_resp.json().keys()
                logging.debug(f'Mocked JSON keys: {mocked_keys}')

            # Compare the actual resp json_keys and mocked resp json_keys for same data-structure
            self.assertEqual(actual_keys, mocked_keys)
        finally:
            f.close()


class TestFetchResponse(unittest.TestCase):
    def setUp(self):
        self.endpoint = 'collection/v1/objects/1'
        self.headers = {'Accept': '*/*', 'Content-Type': 'application/json'}
        self.mock_server_port = get_free_port()
        self.mock_url = 'http://localhost:{port}/'.format(port=self.mock_server_port)
        start_mock_server(self.mock_server_port)

    def test_fetch_response_response_is_ok(self):
        with patch.dict('src.reporter.helpers.fetch_response.__dict__', {'BASE_URL': self.mock_url}):
            response = fetch_response(self.endpoint, header=self.headers)
            self.assertTrue(response.ok)

    @unittest.skip('Skip NOT OK response, not yet handled in mock server')
    def test_fetch_response_response_is_not_ok(self):
        # TODO replace the endpoint with wrong path value
        with patch.dict('src.reporter.helpers.fetch_response.__dict__', {'BASE_URL': self.mock_url}):
            response = fetch_response(self.endpoint, header=self.headers)
            self.assertFalse(response.ok)

    def test_getting_json_fetch_response(self):
        try:
            f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/resp.json'), encoding='utf-8')
        except FileNotFoundError as fnfe:
            logging.exception(f"Could not load JSON mock data for fetch_response: {fnfe.args[-1]}")
        else:
            json_data = json.load(f)
        finally:
            f.close()
        with patch.dict('src.reporter.helpers.fetch_response.__dict__', {'BASE_URL': self.mock_url}):
            response = fetch_response(self.endpoint, header=self.headers)

        self.assertEqual(response.json(), json_data)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
