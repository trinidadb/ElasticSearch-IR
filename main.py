from constants import CLOUD_ID, ELASTIC_PASSWORD, INDEX_NAMES, INDEX_REFERENCE_NAME
from elasticsearch import Elasticsearch
from uploadDocsES import LoaderES
from customIndexes import createCustomIndex
from search import PerformSearch

def createESClient():
    client = Elasticsearch(
        cloud_id=CLOUD_ID,
        basic_auth=("elastic", ELASTIC_PASSWORD),
        request_timeout=120
    )
    return client


def main():
    esClient = createESClient()

    loader = LoaderES(esClient)
    if not esClient.indices.exists(index=INDEX_REFERENCE_NAME):
        loader.initialUploadToES() #Es mas eficiente computacionalmente crear un unico indice (solo parseo los XML una vez)
                                   # y despues definir todos los otros en funcion a este, pero usando la API de ES

    for index_name in INDEX_NAMES:
        createCustomIndex(esClient, index_name)
        PerformSearch(esClient, index_name, writeFile=True)

main()
