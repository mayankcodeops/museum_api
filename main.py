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

    df1 = pd.json_normalize(artifacts).drop(columns=['constituents'])

    meta = list(df1.keys())
    meta.remove('additionalImages')

    df2 = pd.json_normalize(artifacts, record_path=['constituents'], meta=meta,errors='ignore')
    df2 = df2.iloc[:, list(range(6, 61)) + list(range(0, 6))]

    converter = Converter()
    converter.convert_to_csv(config[CONFIG_NAME].REPORT_DIR, 'museum.csv', df2)
    converter.convert_to_html(config[CONFIG_NAME].REPORT_DIR, 'museum.html', df2)
    converter.convert_to_pdf(config[CONFIG_NAME].REPORT_DIR, 'museum.pdf', 'museum.html')
    converter.convert_to_xml(config[CONFIG_NAME].REPORT_DIR, 'museum.csv')
