from elasticsearch import Elasticsearch
from uploadDocsES import LoaderES
from customIndexes import createAllCustomIndexes

ELASTIC_PASSWORD = "ZLELhLuhJsVN3piwvRU350JW"
CLOUD_ID = "rec-info:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRlYmQ1NWZkNjY5Mzk0ZmRjODg1ZjBlZjY0ODMwYzIzMSQ4MzliZjA0M2IxZjY0NmFmOTkyOGI3MGU0ODhiYjJhNw=="

def createESClient():
    client = Elasticsearch(
        cloud_id=CLOUD_ID,
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )
    return client

def main():
    esClient = createESClient()

    loader = LoaderES(esClient)
    if not esClient.indices.exists(index="reference"):
        loader.initialUploadToES() #Es mas eficiente computacionalmente crear un unico indice (solo parseo los XML una vez)
                                   # y despues definir todos los otros en funcion a este, pero usando la API de ES

    createAllCustomIndexes(esClient)

main()
