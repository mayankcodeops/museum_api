import requests

BASE_URL = 'https://collectionapi.metmuseum.org/public/'
LIMIT = 10

headers = {
    'Accept' : '*/*',
    'Content-Type' : 'application/json'
}

def print_object(object_id):
        response_object = requests.get(BASE_URL + 'collection/v1/objects/' + str(object_id),headers=headers)
        print(response_object.text)

for object_id in range(1,LIMIT+1):
    print_object(object_id)