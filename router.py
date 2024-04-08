from fastapi import FastAPI
from model import StoreRequest, StoreResponse, RetrieveResponse, SearchResponse, MatchingDocument, ChatResponse, \
    ChatRequest, SearchRequest
from documents_repo import DocumentsRepository, DocumentsRepositoryFactory
from typing import List, Tuple
from llm_client import BERTLLMClient
import os

natural_language_search = FastAPI()

es_cluster_address = os.getenv('ES_CLUSTER', default='http://localhost')
documents_repo: DocumentsRepository = DocumentsRepositoryFactory.create(
    name='elastic',
    host_address=es_cluster_address,
    port=9200,
    index='test_index'
)

bert_llm_client: BERTLLMClient = BERTLLMClient()


@natural_language_search.get("/")
def root():
    return "Welcome to a natural language search API"


@natural_language_search.get("/healthcheck", status_code=200)
def healthcheck():
    return 200


@natural_language_search.post("/store", status_code=200)
def store(store_request: StoreRequest) -> StoreResponse:
    return StoreResponse(document_id=documents_repo.store(store_request.text))


@natural_language_search.get('/retrieve/{document_id}', status_code=200)
def retrieve(document_id: str) -> RetrieveResponse:
    return RetrieveResponse(text=documents_repo.retrieve(document_id))


@natural_language_search.post('/search', status_code=200)
def search(search_request: SearchRequest) -> SearchResponse:
    matching_documents_with_scores: List[Tuple[str, float]] = documents_repo.search(search_request.text,
                                                                                    search_request.number_of_results)
    converted_matching_documents: List[MatchingDocument] = list(
        map(lambda md: MatchingDocument(
            document=md[0],
            score=md[1]), matching_documents_with_scores))
    return SearchResponse(matching_documents=converted_matching_documents)


@natural_language_search.post('/ask', status_code=200)
def chat(chat_request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=bert_llm_client.ask(chat_request.message))
