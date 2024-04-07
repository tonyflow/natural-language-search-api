from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from elasticsearch import Elasticsearch


class DocumentsRepository(ABC):
    @abstractmethod
    def store(self, text: str) -> str:
        """

        :param text: Document to store
        :return: document id
        """
        pass

    @abstractmethod
    def retrieve(self, document_id: str) -> str:
        pass

    @abstractmethod
    def search(self, text: str) -> List[Tuple[str, float]]:
        pass


class ElasticDocumentsRepository(DocumentsRepository):

    def __init__(self, **kwargs):
        # host_address: str, port: int, index: str
        self.cluster = Elasticsearch([f'{kwargs['host_address']}:{kwargs['port']}'])
        self.index_name = kwargs['index']

    def store(self, text: str) -> str:
        document: Dict[str, any] = {
            "text": text
        }
        response = self.cluster.index(index=self.index_name, body=document)

        return response['_id']

    def retrieve(self, document_id: str) -> str:
        response = self.cluster.get(index=self.index_name, id=document_id)
        return response['_source']['text']

    def search(self, text: str) -> List[Tuple[str, float]]:
        query = {
            "query": {
                "match": {
                    "text": text
                }
            }
        }

        response = self.cluster.search(index=self.index_name, body=query)
        sorted_results = sorted([(hit['_source']['text'], hit['_score']) for hit in response['hits']['hits']])
        return sorted_results


class MockDocumentsRepository(DocumentsRepository):
    def store(self, text: str) -> str:
        return 'this is a document id'

    def retrieve(self, document_id: str) -> str:
        return 'this is a beautiful text'

    def search(self, text: str) -> List[Tuple[str, float]]:
        return [
            ('a beautiful text', 12),
            (' a much more beautiful text', 34)
        ]


class DocumentsRepositoryFactory:

    @staticmethod
    def create(name: str = 'elastic', **kwargs):
        if name == 'elastic':
            return ElasticDocumentsRepository(**kwargs)
        elif name == 'mock':
            return MockDocumentsRepository()
