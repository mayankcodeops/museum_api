import logging
import os

import pandas as pd
from pandas import DataFrame

from src.reporter.helpers.fetch_response import fetch_response
from src.reporter.helpers.flatten import flatten
from src.reporter.converter.converter import Converter

from config import config

CONFIG_NAME = os.environ.get('CONFIG_NAME', 'default')

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=config[CONFIG_NAME].LOG_LEVEL)


headers: dict[str, str] = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}


if __name__ == '__main__':
    artifacts: list[dict] = list(
        map(lambda objectid: fetch_response('collection/v1/objects/' + str(objectid), header=headers)
            .json(),
            list(range(1, config[CONFIG_NAME].API_RESP_LIMIT + 1))))
    for artifact in artifacts:
        flatten(artifact)

    df: DataFrame = pd.DataFrame(artifacts)

    converter = Converter()
    converter.convert_to_csv(config[CONFIG_NAME].REPORT_DIR, 'museum.csv', df)
    converter.convert_to_html(config[CONFIG_NAME].REPORT_DIR, 'museum.html', df)
    converter.convert_to_pdf(config[CONFIG_NAME].REPORT_DIR, 'museum.pdf', 'museum.html')
    converter.convert_to_xml(config[CONFIG_NAME].REPORT_DIR, 'museum.csv')
