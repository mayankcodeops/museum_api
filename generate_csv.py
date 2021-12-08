import csv
import pandas as pd
import pdfkit
import requests
from requests import Response

BASE_URL = 'https://collectionapi.metmuseum.org/public/'
LIMIT = 20

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}

objects: list[dict] = []


def fetch_artifact(objectid):
    """
    :param objectid: objectid for the fetched artifact from the Museum API
    :return: This function returns the artifact fetched from the Museum API for the particular objectid
    """
    response_object: Response = requests.get(BASE_URL + 'collection/v1/objects/' + str(objectid), headers=headers)
    return response_object.json()


for objectid in range(1, LIMIT + 1):
    objects.append(fetch_artifact(objectid))


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


for artifact in objects:
    flatten(artifact)

df = pd.DataFrame(objects)

# generate csv
df.to_csv('museum.csv', mode='w', index=False)
# generate html
df.to_html('museum.html')
# generate pdf report
pdfkit.from_file('museum.html', 'museum.pdf')

# converting csv to xml
f = open('museum.csv')
museum_csv = csv.reader(f)
data = []

for row in museum_csv:
    data.append(row)

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
with open('museum.xml', 'w') as museum:
    museum.write('\n'.join([convert_row(row) for row in data[1:]]))
