from file_exists import file_exists
import pdfkit
import logging
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, 'reports/')


def generate_pdf(directory, pdf_name, html_report):
    """
    :param directory: directory name where the PDF report is to be generated
    :param pdf_name: name of the PDF report to be generated.
    :param html_report: html report from which PDF report is to be generated
    """
    if not file_exists(os.path.join(REPORT_DIR, html_report)):
        raise FileNotFoundError("HTML Report file doesn't exists. Please try creating the report to generate PDF.")
    try:
        pdfkit.from_file(directory + pdf_name, directory + html_report)
    except IOError as ae:
        logging.exception(f'{ae.args[-1]}')
        sys.exit(1)
