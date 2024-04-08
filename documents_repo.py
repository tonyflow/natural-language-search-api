from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
from elasticsearch import Elasticsearch


class DocumentsRepository(ABC):
    """
    Abstract class define the base methods for the documents persistence layer
    """

    @abstractmethod
    def store(self, text: str) -> str:
        """
        Given some string content, store the content in the underlying persistence layer and
        return the ID of the stored content.

        :param text: Document to store
        :return: document id
        """
        pass

    @abstractmethod
    def retrieve(self, document_id: str) -> str:
        """
        Given a text document ID, return the document itself.

        :param document_id: ID of the document
        :return: The text content
        """
        pass

    @abstractmethod
    def search(self, text: str, top_k: int) -> List[Tuple[str, float]]:
        """
        Given a search criteria represented by a text string, search the underlying persistence
        layer for any entries matching - exactly or partially - the given criteria. The repository
        will return the top_k matching results.

        :param text: The string to match
        :param top_k: Number of search results to be returned
        :return: A list of matching documents
        """
        pass


class ESClient:
    def __init__(self, **kwargs):
        self.cluster = Elasticsearch([f'{kwargs['host_address']}:{kwargs['port']}'])
        self.index_name = kwargs['index']

    def get(self):
        pass

    def store(self, document: Dict[str, Any]) -> Dict[str, Any]:
        return self.cluster.index(index=self.index_name, body=document)

    def index(self):
        pass


class ElasticDocumentsRepository(DocumentsRepository):
    """
    Documents repository using ElasticSearch as the persistence layer.
    Requires a host address, a port and an index name to function properly. The index
    does not need to exist beforehand.
    """

    def __init__(self, **kwargs):
        self.cluster = Elasticsearch([f'{kwargs['host_address']}:{kwargs['port']}'])
        self.index_name = kwargs['index']

    # def get_client(self, **kwargs) -> ESClient:
    #     return ESClient(**kwargs)

    def store(self, text: str) -> str:
        document: Dict[str, any] = {
            "text": text
        }
        response = self.cluster.index(index=self.index_name, body=document)

        return response['_id']

    def retrieve(self, document_id: str) -> str:
        response = self.cluster.get(index=self.index_name, id=document_id)
        return response['_source']['text']

    def search(self, text: str, top_k: int) -> List[Tuple[str, float]]:
        """
        The search functionality for this repo uses the _score key/value from
        ElasticSearch _search API to sort the matching documents and return the top_k.
        _score is a way of determining how relevant a match is to the query. For more
        information about how ES scores query results: https://www.elastic.co/guide/en/elasticsearch/guide/2.x/relevance-intro.html#explain
        """
        query = {
            "query": {
                "match": {
                    "text": text
                }
            }
        }

        response = self.cluster.search(index=self.index_name, body=query)
        sorted_results = sorted([(hit['_source']['text'], hit['_score']) for hit in response['hits']['hits']],
                                key=lambda x: -x[1])
        return sorted_results[:top_k]


class MockDocumentsRepository(DocumentsRepository):
    """
    Mock repo for dev and smoke test purposes
    """

    def store(self, text: str) -> str:
        return 'this is a document id'

    def retrieve(self, document_id: str) -> str:
        return 'this is a beautiful text'

    def search(self, text: str, top_k: int) -> List[Tuple[str, float]]:
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
