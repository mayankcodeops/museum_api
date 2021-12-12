import logging
import os

import pandas as pd
from pandas import DataFrame

from fetch_response import fetch_response
from flatten import flatten


from converter import Converter

LIMIT = 20


headers: dict[str, str] = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG)

BASE_URL = 'https://collectionapi.metmuseum.org/public/'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, 'reports/')


if __name__ == '__main__':
    artifacts: list[dict] = list(
        map(lambda objectid: fetch_response('collection/v1/objects/' + str(objectid), header=headers)
            .json(),
            list(range(1, LIMIT + 1))))
    for artifact in artifacts:
        flatten(artifact)

    df: DataFrame = pd.DataFrame(artifacts)

    converter = Converter()
    converter.convert_to_csv(REPORT_DIR, 'museum.csv', df)
    converter.convert_to_html(REPORT_DIR, 'museum.html', df)
    converter.convert_to_pdf(REPORT_DIR, 'museum.pdf', 'museum.html')
    converter.convert_to_xml(REPORT_DIR, 'museum.csv')


