import os
from file_exists import file_exists
import logging
import csv


BASE_URL = 'https://collectionapi.metmuseum.org/public/'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, 'reports/')


class XMLConverter:
    pass


def convert_row(row):
    """
    :param row: This is a single record from the CSV file generated from the API data
    :return: This function returns the XML object parsed from a single CSV record
    """
    return f"""
    <object>
        <objectID>{row[0]}</objectID>
        <isHighlight>{row[1]}</isHighlight>
        <accessionNumber>{row[2]}</accessionNumber>
        <accessionYear>{row[3]}</accessionYear>
        <isPublicDomain>{row[4]}</isPublicDomain>
        <department>{row[9]}<department>
        <objectName>{row[10]}</objectName>
        <title>{row[11]}</title>
    </object>
    """


def generate_xml(directory, csv_file):
    """
    :param directory: directory name where the XML report is to be generated.
    :param csv_file: name of the csv file from which XML report is to be generated.
    """
    if not file_exists(os.path.join(REPORT_DIR, csv_file)):
        raise FileNotFoundError
    try:
        f = open(directory + csv_file)
    except OSError as ae:
        logging.exception("Something went wrong while accessing the CSV report: {}".format(ae.args[-1]))
    else:
        museum_csv = csv.reader(f)
        data = []
        for row in museum_csv:
            data.append(row)
    finally:
        f.close()

    # write the XML objects in to an XML file
    try:
        with open(REPORT_DIR + 'museum.xml', 'w') as museum:
            museum.write('\n'.join([convert_row(row) for row in data[1:]]))
    except OSError as err:
        logging.exception("Writing to xml file failed due to {}".format(err))
