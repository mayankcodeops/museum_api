import logging
import zipfile
import os
from config import config

CONFIG_NAME = os.environ.get('CONFIG_NAME', 'default')

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG)


def zip_reports(compressed_file, *args):
    try:
        with zipfile.ZipFile(compressed_file, 'w') as zipped_report:
            for file in args:
                file_path = os.path.join(config[CONFIG_NAME].REPORT_DIR, file)
                if os.path.isfile(file_path):
                    zipped_report.write(file_path,
                                        compress_type=zipfile.ZIP_DEFLATED)
    except OSError as error:
        logging.exception(f"OSError while writing reports import a zip: {error.args[-1]}")


if __name__ == '__main__':
    zip_reports('reports.zip', 'museum.csv', 'museum.html', 'museum.pdf', 'museum.xml')

