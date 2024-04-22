import xml.etree.ElementTree as ET
from constants import INDEX_REFERENCE_NAME

document_files = ["efe01.xml", "efe02.xml", "efe03.xml", "efe04.xml", "efe05.xml", "efe06.xml", "efe07.xml", "efe08.xml", "efe09.xml", "efe10.xml"]

class LoaderES():
    def __init__(self, esClient, files_folder='files/'):
        self.esClient = esClient
        self.files_folder = files_folder

    def initialUploadToES(self):
        self._index_documents(INDEX_REFERENCE_NAME, document_files=document_files)

    def _index_documents(self, index_name, document_files):
        for document_file in document_files:
            tree = ET.parse(self.files_folder+document_file)
            root = tree.getroot()

            for document in root.findall('.//DOC'):
                doc_id = document.find('DOCNO').text
                category = document.find('CATEGORY').text
                title = document.find('TITLE').text
                text = document.find('TEXT').text

                content = f"{title} {text}"
                self.esClient.index(index=index_name, body={"doc_id": doc_id, "category": category, "content": content})
        
        print(document_file + "already indexed.")