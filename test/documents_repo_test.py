import unittest
from unittest.mock import patch, Mock
from documents_repo import ElasticDocumentsRepository
from mock_es_client import MockESClient
from typing import List, Tuple


class DocumentsRepositoryTest(unittest.TestCase):

    @patch('documents_repo.Elasticsearch')
    def test_store_elastic(self, mock_es_client: Mock):
        mock_es_client.return_value = MockESClient()
        repository = ElasticDocumentsRepository(host_address='http://localhost', port=9200, index='test_index')
        document_id = repository.store("this is a test document")
        self.assertTrue(document_id == "7fBSvY4BrhlG6Amh95OS")

    @patch('documents_repo.Elasticsearch')
    def test_retrieve_elastic(self, mock_es_client: Mock):
        mock_es_client.return_value = MockESClient()
        repository = ElasticDocumentsRepository(host_address='http://localhost', port=9200, index='test_index')
        text: str = repository.retrieve("7fBSvY4BrhlG6Amh95OS")
        self.assertTrue(text == "this is a yet another test document")

    @patch('documents_repo.Elasticsearch')
    def test_search_elastic(self, mock_es_client: Mock):
        mock_es_client.return_value = MockESClient()
        repository = ElasticDocumentsRepository(host_address='http://localhost', port=9200, index='test_index')
        matching_documents: List[Tuple[str, float]] = repository.search(text="7fBSvY4BrhlG6Amh95OS", top_k=2)
        self.assertTrue(
            matching_documents == [
                ("bar", 0.7),
                ("foo", 0.6)
            ]
        )
