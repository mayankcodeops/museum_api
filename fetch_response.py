import requests
import logging
import sys

BASE_URL = 'https://collectionapi.metmuseum.org/public/'
REQ_TIMEOUT = 3


def fetch_response(endpoint, header):
    """
    :param: url from which data is to be fetched
    :return: json response from the API
    """
    # check if the url is valid or not
    try:
        resp = requests.get(BASE_URL + endpoint, headers=header, timeout=REQ_TIMEOUT)
    except (requests.ConnectionError, requests.Timeout) as e:
        logging.exception("Connection error or Request Timed Out: {}".format(e.args[-1]))
        sys.exit(1)
    except requests.HTTPError as httperror:
        logging.exception("HTTP Error. Status Code: {}. Error: {}".format(resp.status_code, httperror.args[-1]))
        sys.exit(1)
    else:
        logging.info("Response Status: {}".format(resp.status_code))
        logging.debug(resp.json())
        return resp
