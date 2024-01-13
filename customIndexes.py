
class Index():

    def __init__(self, esClient, index_name):
        self.esClient = esClient
        self.index_name = index_name    

    def create(self, stopwords, stemmer, useDFR=False):
        index_settings = self._defineBasicIndexSettings(stopwords, stemmer)
        index_settings = self._changeBM25toDFRIndexSettings(index_settings) if useDFR else index_settings
        self.esClient.indices.create(index=self.index_name, body=index_settings) # Define el índice con el analizador SpanishAnalyzer
        self._populateIndexFromReference()

    def _populateIndexFromReference(self):
        # Reindexa los documentos del índice existente al nuevo índice.
        reindex_body = {
            "source": {"index": "reference"},
            "dest": {"index": self.index_name},
        }
        self.esClient.reindex(body=reindex_body)    

    def _defineBasicIndexSettings(self, stopwords, stemmer, similarity=None):
        return {
            "settings": {
                "analysis": {
                "filter": {
                    "spanish_stop": {
                    "type": "stop",
                    "stopwords": stopwords
                    },
                    "spanish_stemmer": {
                    "type": "stemmer",
                    "language": stemmer
                    }
                },
                "analyzer": {
                    "spanish_analyzer": {
                    "type":"spanish",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "spanish_stop",
                        "spanish_stemmer"
                    ]
                    }
                }
                },
            },
            "mappings": {
                "properties": {
                    "doc_id": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "content": {"type": "text", "analyzer": "spanish_analyzer"},
                    "query_id": {"type": "keyword"},
                }
            }
        }

    def _changeBM25toDFRIndexSettings(self, index_settings):
        index_settings["settings"]["similarity"] = {
                                                    "my_similarity": {
                                                    "type": "DFR",
                                                    "basic_model": "g",
                                                    "after_effect": "l",
                                                    "normalization": "h2",
                                                    "normalization.h2.c": "3.0"
                                                    }
                                                }
        return index_settings
    

def createAllCustomIndexes(esClient):

    #Clear state
    esClient.indices.delete(index="base")
    esClient.indices.delete(index="vacias_txt")
    esClient.indices.delete(index="snowball_stm")
    esClient.indices.delete(index="dfr")

    with open("files/vacias.txt", "r", encoding="utf-8") as file:
        stopwords_vaciasTXT = [line.strip() for line in file.readlines()]

    Index(esClient, "base").create(stopwords="_spanish_", stemmer="light_spanish") #"_spanish_" --> Lista procedente de Snowball
                                                                                   #"light_spanish" --> Procedente de la página de recursos de Jacques Savoy
    print("base index created")
    Index(esClient, "vacias_txt").create(stopwords=stopwords_vaciasTXT, stemmer="light_spanish") #"light_spanish" --> Procedente de la página de recursos de Jacques Savoy    
    print("vacias_txt index created")
    Index(esClient, "snowball_stm").create(stopwords="_spanish_", stemmer="spanish") #"_spanish_" --> Lista procedente de Snowball
                                                                                     #"spanish" --> Procedente de Snowball
    print("snowball_stm index created")
    Index(esClient, "dfr").create(stopwords="_spanish_", stemmer="light_spanish", useDFR=True) #"_spanish_" --> Lista procedente de Snowball
                                                                                   #"light_spanish" --> Procedente de la página de recursos de Jacques Savoy
    print("dfr index created")

    