from file_exists import file_exists
import pdfkit
import logging
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, 'reports/')


class PDFConverter:
    def __int__(self, directory, pdf_name, html_report):
        self.directory = directory
        self.pdf_name = pdf_name
        self.html_report = html_report

    def generate_pdf(self):
        if not file_exists(os.path.join(REPORT_DIR, self.html_report)):
            logging.exception(f'FileNotFoundError: HTML report doesnt exist')
        try:
            pdfkit.from_file(self.directory + self.pdf_name, self.directory + self.html_report)
        except IOError as ae:
            logging.exception(f'{ae.args[-1]}')
            sys.exit(1)
