import xml.etree.ElementTree as ET

class PerformSearch():
    
    def __init__(self, esClient, index_name, writeFile=True):
        self.esClient = esClient
        self.index_name = index_name
        self.results = self.searchDocuments()
        if writeFile:
            self.writeFile()

    def searchDocuments(self, max_docs=2):
        print(f"Performing search task for '{self.index_name}' index")

        queries = self._getQueries()
        print(len(queries))
        for query_id in queries:
            body={"query": {"match": {"content": {"query": queries[query_id]}}}}
            searchResults = self.esClient.search(index=self.index_name, body=body, size=max_docs)

            searchResults = searchResults['hits']['hits']

            results = []
            for rank, searchResult in enumerate(searchResults, start=1):
                format = f"{query_id} Q0 {searchResult['_source']['doc_id']} {rank} {searchResult['_score']} {self.index_name}"
                results.append(format)

        print(results)
        print(f"Finished search task for '{self.index_name}' index")
        return results    
    
    def writeFile(self):
        with open(self.index_name+'.txt', "w") as file:
            for string in self.results:
                file.write(string + "\n")
        print(f"Text file '{self.index_name}.txt' created successfully.")

    def _getQueries(self):
        tree = ET.parse('files/topics.xml')
        root = tree.getroot()
        formated_queries = {}

        for topic in root.findall('.//top'):
            query_id = topic.find('num').text
            title = topic.find('ES-title').text
            description = topic.find('ES-desc').text

            # Combina título y descripción en un solo campo (ajusta según tus necesidades)
            content = f"{title} {description}"
            formated_queries[query_id] = content

        return formated_queries

