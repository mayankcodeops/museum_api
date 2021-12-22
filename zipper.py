import zipfile
import os
from config import config


if __name__ == '__main__':
    compressed_reports = zipfile.ZipFile('reports.zip', 'w')
    compressed_reports.write(os.path.join(config['default'].REPORT_DIR, 'museum.csv'),
                             compress_type=zipfile.ZIP_DEFLATED)
    compressed_reports.write(os.path.join(config['default'].REPORT_DIR, 'museum.html'),
                             compress_type=zipfile.ZIP_DEFLATED)
    compressed_reports.write(os.path.join(config['default'].REPORT_DIR, 'museum.pdf'),
                             compress_type=zipfile.ZIP_DEFLATED)
    compressed_reports.write(os.path.join(config['default'].REPORT_DIR, 'museum.xml'),
                             compress_type=zipfile.ZIP_DEFLATED)
    compressed_reports.close()

