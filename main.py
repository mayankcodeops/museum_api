import csv
import logging
import os

import pandas as pd
import pdfkit
from pandas import DataFrame

import fetch_response
import flatten
import generate_csv
import generate_html
import generate_pdf
import generate_xml


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
        map(lambda objectid: fetch_response('collection/v1/objects/' + str(objectid), headers=headers)
            .json(),
            list(range(1, LIMIT + 1))))
    for artifact in artifacts:
        flatten(artifact)

    df: DataFrame = pd.DataFrame(artifacts)
    generate_csv(REPORT_DIR, 'museum.csv', df)
    generate_html(REPORT_DIR, 'museum.html', df)
    generate_pdf(REPORT_DIR, 'museum.pdf', 'museum.html')
    generate_xml(REPORT_DIR, 'museum.csv')


# # generate csv
# try:
#     df.to_csv(REPORT_DIR + 'museum.csv', mode='w', index=False)
# except OSError as err:
#     print(f'Some error has occurred during CSV generation: {err}', err)
#
# # generate html
# try:
#     df.to_html(REPORT_DIR + 'museum.html')
# except OSError as err:
#     print(f'Some error has occurred during HTML report generation: {err} ', err)
#
# # generate pdf report
# try:
#     pdfkit.from_file(REPORT_DIR + 'museum.html', REPORT_DIR + 'museum.pdf')
# except OSError as err:
#     print(f'Some error has occurred during PDF generation: {err}', err)

