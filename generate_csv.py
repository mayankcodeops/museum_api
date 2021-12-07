import csv

import pandas as pd
import pdfkit
import requests

BASE_URL = 'https://collectionapi.metmuseum.org/public/'
LIMIT = 20

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}

objects = []


def fetch_artifact(objectID):
    response_object = requests.get(BASE_URL + 'collection/v1/objects/' + str(objectID), headers=headers)
    return response_object.json()


for objectID in range(1, LIMIT + 1):
    objects.append(fetch_artifact(objectID))


def flatten(artifact):
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


# print(data[1:])
def convert_row(row):
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
    """ % (row[0], row[1], row[2], row[3], row[4], row[9], row[10], row[11])


with open('museum.xml', 'w') as museum:
    museum.write('\n'.join([convert_row(row) for row in data[1:]]))
