import requests
import csv
BASE_URL = 'https://collectionapi.metmuseum.org/public/'
LIMIT = 2

headers = {
    'Accept' : '*/*',
    'Content-Type' : 'application/json'
}

objects = []

def fetch_artifact(object_id):
        response_object = requests.get(BASE_URL + 'collection/v1/objects/' + str(object_id),headers=headers)
        return response_object.json()


for object_id in range(1,LIMIT+1):
    objects.append(fetch_artifact(object_id))

print(objects)
keys =[
    "objectID",
    "isHighlight", 
    "accessionNumber",
    "accessionYear",
    "isPublicDomain",
    "primaryImage",
    "primaryImageSmall",
    "additionalImages",
    "constituents",
    "department",
    "objectName",
    "title",
    "culture",
    "period",
    "dynasty",
    "reign",
    "portfolio",
    "artistRole",
    "artistPrefix",
    "artistDisplayName",
    "artistDisplayBio",
    "artistSuffix",
    "artistAlphaSort",
    "artistNationality",
    "artistBeginDate",
    "artistEndDate",
    "artistGender",
    "artistWikidata_URL",
    "artistULAN_URL",
    "objectDate",
    "objectBeginDate",
    "objectEndDate",
    "medium",
    "dimensions",
    "dimensionsParsed",
    "measurements",
    "creditLine",
    "geographyType",
    "city",
    "state",
    "county",
    "country",
    "region",
    "subregion",
    "locale",
    "locus",
    "excavation",
    "river",
    "classification",
    "rightsAndReproduction",
    "linkResource",
    "metadataDate",
    "repository",
    "objectURL",
    "tags",
    "objectWikidata_URL",
    "isTimelineWork",
    "GalleryNumber",
]

with open("museum_data.csv", "w") as museum_data:
    writer = csv.DictWriter(museum_data, fieldnames=keys)
    writer.writeheader()
    writer.writerows(objects)