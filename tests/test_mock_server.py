import unittest
from unittest.mock import Mock, patch
import requests
import re
import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread

from src.reporter.helpers.fetch_response import fetch_response


def parse_url(url):
    url_object = urlparse(url)
    return url_object.path, url_object.params, url_object.query


json_resp = {"objectID": 1, "isHighlight": "false", "accessionNumber": "1979.486.1", "accessionYear": "1979",
             "isPublicDomain": "false", "primaryImage": "", "primaryImageSmall": "", "additionalImages": [],
             "constituents": [{"constituentID": 164292, "role": "Maker", "name": "James Barton Longacre",
                               "constituentULAN_URL": "http://vocab.getty.edu/page/ulan/500011409",
                               "constituentWikidata_URL": "https://www.wikidata.org/wiki/Q3806459", "gender": ""}],
             "department": "The American Wing", "objectName": "Coin", "title": "One-dollar Liberty Head Coin",
             "culture": "", "period": "", "dynasty": "", "reign": "", "portfolio": "", "artistRole": "Maker",
             "artistPrefix": "", "artistDisplayName": "James Barton Longacre",
             "artistDisplayBio": "American, Delaware County, Pennsylvania 1794–1869 Philadelphia, Pennsylvania",
             "artistSuffix": "", "artistAlphaSort": "Longacre, James Barton", "artistNationality": "American",
             "artistBeginDate": "1794", "artistEndDate": "1869", "artistGender": "",
             "artistWikidata_URL": "https://www.wikidata.org/wiki/Q3806459",
             "artistULAN_URL": "http://vocab.getty.edu/page/ulan/500011409", "objectDate": "1853",
             "objectBeginDate": 1853, "objectEndDate": 1853, "medium": "Gold", "dimensions": "Dimensions unavailable",
             "measurements": "null", "creditLine": "Gift of Heinz L. Stoppelmann, 1979", "geographyType": "", "city": "",
             "state": "", "county": "", "country": "", "region": "", "subregion": "", "locale": "", "locus": "",
             "excavation": "", "river": "", "classification": "", "rightsAndReproduction": "", "linkResource": "",
             "metadataDate": "2021-04-06T04:41:04.967Z", "repository": "Metropolitan Museum of Art, New York, NY",
             "objectURL": "https://www.metmuseum.org/art/collection/search/1", "tags": "null", "objectWikidata_URL": "",
             "isTimelineWork": "false", "GalleryNumber": ""}

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
