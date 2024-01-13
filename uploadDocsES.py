import xml.etree.ElementTree as ET

document_files = ["efe01.xml", "efe02.xml", "efe03.xml", "efe04.xml", "efe05.xml", "efe06.xml", "efe07.xml", "efe08.xml", "efe09.xml", "efe10.xml"]
query_file = "topics.xml"
vacias_file = "vacias.txt"

class LoaderES():
    def __init__(self, esClient, files_folder='files/'):
        self.esClient = esClient
        self.files_folder = files_folder
        self.referenceIndexName = "reference"

    def initialUploadToES(self):
        self._index_documents(self.referenceIndexName, document_files=document_files)
        self._index_queries(self.referenceIndexName,query_file=query_file)

    def _index_documents(self, index_name, document_files):
        for document_file in document_files:
            tree = ET.parse(self.files_folder+document_file)
            root = tree.getroot()

            for document in root.findall('.//DOC'):
                doc_id = document.find('DOCNO').text
                category = document.find('CATEGORY').text
                title = document.find('TITLE').text
                text = document.find('TEXT').text

                # Combina título y texto en un solo campo (ajusta según tus necesidades)
                content = f"{title} {text}"

                # Indexa el documento en Elasticsearch
                self.esClient.index(index=index_name, body={"doc_id": doc_id, "category": category, "content": content})
        print(document_file + "already indexed.")

    def _index_queries(self, index_name, query_file):
        tree = ET.parse(self.files_folder+query_file)
        root = tree.getroot()

        for topic in root.findall('.//top'):
            query_id = topic.find('num').text
            title = topic.find('ES-title').text
            description = topic.find('ES-desc').text

            # Combina título y descripción en un solo campo (ajusta según tus necesidades)
            content = f"{title} {description}"

            # Indexa la consulta en Elasticsearch
            self.esClient.index(index=index_name, body={"query_id": query_id, "content": content})

        print(query_file + "already indexed.")    

