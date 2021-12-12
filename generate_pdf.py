from file_exists import file_exists
import pdfkit
import logging
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, 'reports/')


class PDFConverter:
    """
        A class for generating PDF reports from HTML file

        Attributes
        ----------

        Methods
        -------
        generate_pdf(directory, pdf_name, html_report)
            Generates PDF report from HTML file
        """

    @staticmethod
    def generate_pdf(directory, pdf_name, html_report):
        if not file_exists(os.path.join(REPORT_DIR, html_report)):
            logging.exception(f'FileNotFoundError: HTML report doesnt exist')
        try:
            pdfkit.from_file(directory + pdf_name, directory + html_report)
        except IOError as ae:
            logging.exception(f'{ae.args[-1]}')
            sys.exit(1)

