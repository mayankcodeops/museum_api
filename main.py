import logging
import os

import pandas as pd
from pandas import DataFrame

from fetch_response import fetch_response
from flatten import flatten


from generate_csv import CSVConverter
from generate_html import HTMLConverter
from generate_pdf import PDFConverter
from generate_xml import XMLConverter

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

    # TODO: Change the class signature, should be:
    # TODO: csv_convertor = CSVConverter()
    # TODO: csv_convertor.generate_csv(REPORT_DIR, 'museum.csv', df)
    # TODO: To make it more generic it should be something like
    # TODO: converter = Converter()
    # TODO: converter.generate_csv(REPORT_DIR, 'museum.csv', df)
    # TODO: converter.generate_html(REPORT_DIR, 'museum.html', df)
    # TODO: converter.generate_pdf(REPORT_DIR, 'museum.pdf', 'museum.html')
    # TODO: converter.generate_xml(REPORT_DIR, 'museum.csv')

    csv_converter: CSVConverter = CSVConverter()
    csv_converter.generate_csv(REPORT_DIR, 'museum.csv', df)

    html_converter: HTMLConverter = HTMLConverter()
    html_converter.generate_html(REPORT_DIR, 'museum.html', df)

    # pdf_converter = PDFConverter(REPORT_DIR, 'museum.pdf', 'museum.html')
    # pdf_converter.generate_pdf()
    #
    # xml_converter = XMLConverter(REPORT_DIR, 'museum.csv')
    # xml_converter.generate_xml()

