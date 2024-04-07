from fastapi import FastAPI
from model import StoreRequest, StoreResponse, RetrieveResponse, SearchResponse, MatchingDocument, ChatResponse, \
    ChatRequest
from documents_repo import DocumentsRepository, DocumentsRepositoryFactory
from typing import List, Tuple
from llm_client import BERTLLMClient

natural_language_search = FastAPI()

# documents_repo: DocumentsRepository = DocumentsRepositoryFactory.create(name='mock')
documents_repo: DocumentsRepository = DocumentsRepositoryFactory.create(
    name='elastic',
    host_address='http://localhost',
    port=9200,
    index='test_index'
)

bert_llm_client: BERTLLMClient = BERTLLMClient()


@natural_language_search.get("/")
def root():
    return "Welcome to a natural language search API"


# Store
@natural_language_search.post("/store", status_code=200)
def store(store_request: StoreRequest) -> StoreResponse:
    return StoreResponse(document_id=documents_repo.store(store_request.text))


# Retrieve
@natural_language_search.get('/retrieve/{document_id}', status_code=200)
def retrieve(document_id: str) -> RetrieveResponse:
    return RetrieveResponse(text=documents_repo.retrieve(document_id))


# Search
@natural_language_search.get('/search', status_code=200)
def search(text: str) -> SearchResponse:
    matching_documents_with_scores: List[Tuple[str, float]] = documents_repo.search(text)
    converted_matching_documents: List[MatchingDocument] = list(
        map(lambda md: MatchingDocument(
            document=md[0],
            score=md[1]), matching_documents_with_scores))
    return SearchResponse(matching_documents=converted_matching_documents)


@natural_language_search.post('/chat', status_code=200)
def chat(chat_request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=bert_llm_client.ask(chat_request.message))
