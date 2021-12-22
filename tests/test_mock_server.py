import unittest
import requests

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(requests.codes.ok)
        self.end_headers()
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class TestMockServer(unittest.TestCase):
    def setUp(self):
        self.mock_server_port = get_free_port()
        self.mock_server = HTTPServer(('localhost', self.mock_server_port), MockServerRequestHandler)

        # run mock server in a separate thread
        # mock server daemon thread will shut down when the main process stops
        self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

    def test_request_response(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)

        # send request to the mock API server and store the response.
        response = requests.get(url)

        # confirm that the request-response cycle completed successfully
        self.assertTrue(response.ok)




