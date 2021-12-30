import re
import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import requests
import os
import logging


logging.basicConfig(filename='testing.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG)


def parse_url(url):
    url_object = urlparse(url)
    return url_object.path, url_object.params, url_object.query


json_resp = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/1').json()

try:
    f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/museum.json'))
except FileNotFoundError as fnfe:
    logging.exception(f"Could not load JSON mock data for TestHTMLGenerator: {fnfe.args[-1]}")
else:
    json_data = json.load(f)
finally:
    f.close()


class MockServerRequestHandler(BaseHTTPRequestHandler):
    ARTIFACT_PATTERN = re.compile(r'/collection/v1/objects/')

    def do_GET(self):
        if re.search(self.ARTIFACT_PATTERN, self.path):
            self.send_response(requests.codes.ok)
            object_id = self.path.split('/')[-1]
            self.send_header('Accept', '*/*')
            self.send_header('Content-Type', 'application/json; charset=UTF-8')
            self.end_headers()
            response_content = json.dumps(json_data[object_id])
            self.wfile.write(response_content.encode('utf-8'))
            return
        else:
            self.send_response(requests.codes['not_found'])
            self.send_header('Accept', '*/*')
            self.send_header('Content-Type', 'application/json; charset=UTF-8')
            self.end_headers()
            response_content = json.dumps({"message": "Not Found"})
            self.wfile.write(response_content.encode('utf-8'))


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


if __name__ == '__main__':
    start_mock_server(get_free_port())
