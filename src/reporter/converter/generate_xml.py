import os
from ..helpers.file_exists import file_exists
import logging
import csv


class XMLConverter:
    """
        A class for generating XML reports from CSV file

        Attributes
        ----------

        Methods
        -------
        convert_row(row)
            Takes a row of CSV data and converts it into an XML object
        generate_xml(directory, csv_file)
            Generates XML report from CSV data
        """
    @staticmethod
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
            <department>{row[7]}<department>
            <objectName>{row[8]}</objectName>
            <title>{row[9]}</title>
            <artistRole>{row[15]}</artistRole>
            <artistDisplayName>{row[17]}</artistDisplayName>
            <artistDisplayBio>{row[18]}</artistDisplayBio>
        </object>
        """

    @staticmethod
    def convert(directory, csv_file):
        if not file_exists(os.path.join(directory, csv_file)):
            raise FileNotFoundError
        try:
            f = open(os.path.join(directory, csv_file))
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
            with open(directory + 'museum.xml', 'w') as museum:
                museum.write('\n'.join([__class__.convert_row(row) for row in data[1:]]))
        except OSError as err:
            logging.exception("Writing to xml file failed due to {}".format(err))
