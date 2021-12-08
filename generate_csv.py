import csv
import pandas as pd
import pdfkit
import requests
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, 'reports/')
BASE_URL = 'https://collectionapi.metmuseum.org/public/'

LIMIT = 20

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}

objects: list[dict] = []


objects = list(map(lambda objectid: requests.get(BASE_URL + 'collection/v1/objects/' + str(objectid), headers=headers)
                   .json(),
                   list(range(1, LIMIT + 1))))


def flatten(artifact):
    """
    :param artifact: this is the artifact dictionary fetched from the Museum API
    :return: This function returns the flattened JSON from a complex nested JSON recieved from the API response object
    """
    try:
        for constituent in artifact['constituents']:
            for key, value in constituent.items():
                artifact[key] = value
            artifact.pop('constituents')
    except TypeError:
        pass

# TODO: Debug return type here
# objects = list(map(flatten, objects))


for artifact in objects:
    flatten(artifact)

df = pd.DataFrame(objects)

# generate csv
try:
    df.to_csv(REPORT_DIR + 'museum.csv', mode='w', index=False)
except OSError as err:
    print(f'Some error has occurred during CSV generation: {}', err)


# generate html
try:
    df.to_html(REPORT_DIR + 'museum.html')
except OSError as err:
    print(f'Some error has occurred during HTML reoprt generation: {err} ', err)

# generate pdf report
try:
    pdfkit.from_file(REPORT_DIR + 'museum.html', REPORT_DIR + 'museum.pdf')
except OSError as err:
    print(f'Some error has occurred during PDF generation: {err}', err)

# converting csv to xml
try:
    f = open(REPORT_DIR + 'museum.csv')
except OSError as err:
    print(f'Not able to open CSV file: {err}', err)
else:
    museum_csv = csv.reader(f)
    data = []
    for row in museum_csv:
    data.append(row)
finally:
    f.close()


def convert_row(row1):
    """
    :param row1: This is a single record from the CSV file generated from the API data
    :return: This function returns the XML object parsed from a single CSV record
    """
    return """
    <object>
        <objectID>%s</objectID>
        <isHighlight>%s</isHighlight>
        <accessionNumber>%s</accessionNumber>
        <accessionYear>%s</accessionYear>
        <isPublicDomain>%s</isPublicDomain>
        <department>%s<department>
        <objectName>%s</objectName>
        <title>%s</title>
    </object>
    """ % (row1[0], row1[1], row1[2], row1[3], row1[4], row1[9], row1[10], row1[11])


# write the XML objects in to a XML file
with open(REPORT_DIR + 'museum.xml', 'w') as museum:
    museum.write('\n'.join([convert_row(row) for row in data[1:]]))
