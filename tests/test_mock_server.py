import unittest
from unittest.mock import Mock, patch
import requests
import re
import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import requests
from src.reporter.helpers.fetch_response import fetch_response


def parse_url(url):
    url_object = urlparse(url)
    return url_object.path, url_object.params, url_object.query


json_resp = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/1').json()

headers: dict[str, str] = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}


class MockServerRequestHandler(BaseHTTPRequestHandler):
    ARTIFACT_PATTERN = re.compile(r'/collection/v1/objects/')

    def do_GET(self):
        if re.search(self.ARTIFACT_PATTERN, self.path):
            self.send_response(requests.codes.ok)

            self.send_header('Accept', '*/*')
            self.send_header('Content-Type', 'application/json; charset=UTF-8')
            self.end_headers()
            response_content = json.dumps(json_resp)
            self.wfile.write(response_content.encode('utf-8'))
            return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()


class TestMockServer(unittest.TestCase):
    def setUp(self):
        self.mock_server_port = get_free_port()
        self.mock_server = HTTPServer(('localhost', self.mock_server_port), MockServerRequestHandler)

        # run mock server in a separate thread
        # mock server daemon thread will shut down when the main process stops
        self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

    @staticmethod
    def extract_dict_a_from_b(a, b):
        return dict([(k, b[k]) for k in a.keys() if k in b.keys()])

    def test_request_response(self):
        mock_url = 'http://localhost:{port}/'.format(port=self.mock_server_port)

        with patch.dict('src.reporter.helpers.fetch_response.__dict__', {'BASE_URL': mock_url}):
            response = fetch_response('collection/v1/objects/1', header=headers)

        self.assertEqual({'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8'},
                         self.extract_dict_a_from_b({'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8'}
                                                    , response.headers))
        self.assertTrue(response.ok)

        self.assertDictEqual(response.json(), json_resp)
