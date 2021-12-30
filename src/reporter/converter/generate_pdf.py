from ..helpers.file_exists import file_exists
import pdfkit
import logging
import sys
import os


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
    def convert(directory, pdf_name, html_report):
        if not file_exists(os.path.join(directory, html_report)):
            logging.exception(f'FileNotFoundError: HTML report doesnt exist')
        try:
            pdfkit.from_file(os.path.join(directory, html_report), os.path.join(directory, pdf_name),
                             options={'page-size': 'B0', 'dpi': 400, 'encoding': "UTF-8",
})
        except IOError as ae:
            logging.exception(f'{ae.args[-1]}')
            sys.exit(1)

