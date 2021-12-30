from .generate_csv import CSVConverter
from .generate_html import HTMLConverter
from .generate_pdf import PDFConverter
from .generate_xml import XMLConverter


class Converter:
    """
    Converter class to wrap other report converter classes
    """
    @staticmethod
    def convert_to_csv(directory, filename, df):
        """
        Converts dataframe to CSV report
        :param directory: directory path for creating CSV report
        :param filename: name of the CSV report to be generated
        :param df: Pandas Dataframe Object
        """
        CSVConverter().convert(directory, filename, df)

    @staticmethod
    def convert_to_html(directory, filename, df):
        """
        Converts dataframe object to an HTML report
        :param directory: directory path for creating HTML report
        :param filename: name of the HTML report to be generated
        :param df: Pandas dataframe object
        """
        HTMLConverter().convert(directory, filename, df)

    @staticmethod
    def convert_to_pdf(directory, pdf_name, html_report):
        """
        Converts HTML reports to PDF format
        :param directory: directory path for creating the PDF report
        :param pdf_name: name of the PDF report to be generated
        :param html_report: name of the HTML report
        """
        PDFConverter().convert(directory, pdf_name, html_report)

    @staticmethod
    def convert_to_xml(directory, csv_file):
        """
        Converts CSV file records to XML report
        :param directory: directory path for the XML report to be generated
        :param csv_file: name of the CSV file to be generated
        """
        XMLConverter().convert(directory, csv_file)



