import logging
import os

import pandas as pd
from pandas import DataFrame

from fetch_response import fetch_response
from flatten import flatten
# from generate_csv import generate_csv
# from generate_html import generate_html
# from generate_pdf import generate_pdf
# from generate_xml import generate_xml

from generate_csv import CSVConverter

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

    csv_converter: CSVConverter = CSVConverter(REPORT_DIR, 'museum.csv', df)
    csv_converter.generate_csv()
    # generate_html(REPORT_DIR, 'museum.html', df)
    # generate_pdf(REPORT_DIR, 'museum.pdf', 'museum.html')
    # generate_xml(REPORT_DIR, 'museum.csv')
