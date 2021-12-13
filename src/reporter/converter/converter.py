from .generate_csv import CSVConverter
from .generate_html import HTMLConverter
from .generate_pdf import PDFConverter
from .generate_xml import XMLConverter


class Converter:
    """
    Converter class to wrap other report converter classes
    """
    def convert_to_csv(self, directory, filename, df):
        CSVConverter().convert(directory, filename, df)

    def convert_to_html(self, directory, filename, df):
        HTMLConverter().convert(directory, filename, df)

    def convert_to_pdf(self, directory, pdf_name, html_report):
        PDFConverter().convert(directory, pdf_name, html_report)

    def convert_to_xml(self, directory, csv_file):
        XMLConverter().convert(directory, csv_file)



