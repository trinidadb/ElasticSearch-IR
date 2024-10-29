import xml.etree.ElementTree as ET
import os

from constants import SEARCH_RESULTS_DIR

class PerformSearch():
    
    def __init__(self, esClient, index_name, writeFile=True):
        self.esClient = esClient
        self.index_name = index_name
        self.results = self.searchDocuments()
        if writeFile:
            os.makedirs(SEARCH_RESULTS_DIR, exist_ok=True)
            self.writeFile(folder=SEARCH_RESULTS_DIR)

    def searchDocuments(self, max_docs=1000):
        print(f"Performing search task for '{self.index_name}' index")

        queries = self._getQueries()
        
        results = []
        for id, query in queries.items():
            body={"query": {"match": {"content": {"query": query}}}}
            searchResults = self.esClient.search(index=self.index_name, body=body, size=max_docs)

            searchResults = searchResults['hits']['hits']

            for rank, searchResult in enumerate(searchResults, start=1):
                format = f"{id} Q0 {searchResult['_source']['doc_id']} {rank} {searchResult['_score']} {self.index_name}"
                results.append(format)

        print(f"Finished search task for '{self.index_name}' index")
        return results    
    
    def writeFile(self, folder):
        with open(folder+self.index_name+'.txt', "w") as file:
            for string in self.results:
                file.write(string + "\n")
        print(f"Text file '{folder+self.index_name}.txt' created successfully.")

    def _getQueries(self):
        tree = ET.parse('files/topics.xml')
        root = tree.getroot()
        formated_queries = {}

        for topic in root.findall('.//top'):
            query_id = topic.find('num').text
            title = topic.find('ES-title').text
            description = topic.find('ES-desc').text

            content = f"{title} {description}"
            formated_queries[query_id] = content

        return formated_queries

