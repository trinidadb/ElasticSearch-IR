from constants import INDEX_REFERENCE_NAME

class Index():

    def __init__(self, esClient, index_name):
        self.esClient = esClient
        self.index_name = index_name    

    def create(self, stopwords=None, stemmer=None, useDFR=False):
        index_settings = self._defineBasicIndexSettings(stopwords, stemmer)
        #index_settings = self._changeBM25toDFRIndexSettings(index_settings) if useDFR else index_settings
        self.esClient.indices.create(index=self.index_name, body=index_settings) # Define el índice con el analizador SpanishAnalyzer
        self._populateIndexFromReference()

    def _populateIndexFromReference(self):
        # Reindexa los documentos del índice existente al nuevo índice.
        reindex_body = {
            "source": {"index": INDEX_REFERENCE_NAME},
            "dest": {"index": self.index_name},
        }
        self.esClient.reindex(body=reindex_body)    

    def _defineBasicIndexSettings(self, stopwords, stemmer):
        return {
            "settings": {
                    "analysis": {
                        "filter": {
                            "spanish_stop": {
                                "type": "stop",
                                "stopwords" : stopwords
                            },
                            "spanish_stemmer": {
                                "type": "stemmer",
                                "language" : stemmer
                            }
                        },
                        "analyzer": {
                            "rebuilt_spanish": {
                                "type":"custom",
                                "tokenizer": "standard",
                                "filter": [
                                    "lowercase",
                                    "spanish_stop",
                                    "spanish_stemmer"
                                ]
                            }
                        }  
                    }
                },
                "mappings": {
                "properties": {
                    "doc_id": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "content": {"type": "text", "analyzer": "rebuilt_spanish"}
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
    
    def _defineBasicIndexSettings2(self):
        return {
                "settings": {
                    "analysis": {
                        "filter": {
                            "spanish_stop": {
                                "type": "stop",
                                "stopwords" : "_spanish_"
                            },
                            "spanish_stemmer": {
                                "type": "stemmer",
                                "language" : "light_spanish"
                            }
                        },
                        "analyzer": {
                            "rebuilt_spanish": {
                                "type":"custom",
                                "tokenizer": "standard",
                                "filter": [
                                    "lowercase",
                                    "spanish_stop",
                                    "spanish_stemmer"
                                ]
                            }
                        }  
                    }
                },
                "mappings": {
                "properties": {
                    "doc_id": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "content": {"type": "text", "analyzer": "rebuilt_spanish"}
                }
            }
            }
    

def createCustomIndex(esClient, index_name):

    try:
        esClient.indices.delete(index=index_name)
    except:
        pass

    match index_name:
        case "base":
            stopwords = "_spanish_"   #"_spanish_" --> Lista procedente de Snowball
            stemmer = "light_spanish" #"light_spanish" --> Procedente de la página de recursos de Jacques Savoy
            useDFR = False

        case "vacias_txt":
            with open("files/vacias.txt", "r", encoding="utf-8") as file:
                stopwords_vaciasTXT = [line.strip() for line in file.readlines()]

            stopwords = stopwords_vaciasTXT
            stemmer = "light_spanish"
            useDFR = False

        case "snowball_stm":
            stopwords = "_spanish_"
            stemmer = "spanish"       #"spanish" --> Procedente de Snowball
            useDFR = False

        case "dfr":
            stopwords = "_spanish_"
            stemmer = "light_spanish"
            useDFR = True

    Index(esClient, index_name).create(stopwords=stopwords, stemmer=stemmer, useDFR=useDFR)
    #Index(esClient, index_name).create()
    print(f"{index_name} index created")

    