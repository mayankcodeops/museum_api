import unittest
from unittest.mock import Mock, patch
import requests
from src.reporter.helpers.fetch_response import fetch_response
from .mock_server import start_mock_server, get_free_port

json_resp = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/1').json()

headers: dict[str, str] = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}


class TestMockServer(unittest.TestCase):
    def setUp(self):
        self.mock_server_port = get_free_port()
        start_mock_server(self.mock_server_port)

    @staticmethod
    def extract_dict_a_from_b(a, b):
        return dict([(k, b[k]) for k in a.keys() if k in b.keys()])

    def test_request_response_is_ok(self):
        mock_url = 'http://localhost:{port}/'.format(port=self.mock_server_port)

        with patch.dict('src.reporter.helpers.fetch_response.__dict__', {'BASE_URL': mock_url}):
            response = fetch_response('collection/v1/objects/1', header=headers)

        self.assertEqual({'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8'},
                         self.extract_dict_a_from_b({'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8'}
                                                    , response.headers))
        self.assertTrue(response.ok)

        self.assertDictEqual(response.json(), json_resp)

    def test_request_response_is_not_ok(self):
        mock_url = 'http://localhost:{port}/'.format(port=self.mock_server_port)

        with patch.dict('src.reporter.helpers.fetch_response.__dict__', {'BASE_URL': mock_url}):
            response = fetch_response('collection/v1/obj/3', header=headers)

        self.assertEqual({'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8'},
                         self.extract_dict_a_from_b({'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8'}
                                                    , response.headers))

        self.assertFalse(response.ok)
        self.assertDictEqual(response.json(), {"message": "Not Found"})

