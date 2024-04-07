from pydantic import BaseModel


class StoreRequest(BaseModel):
    text: str


class StoreResponse(BaseModel):
    document_id: str


class RetrieveResponse(BaseModel):
    text: str


class MatchingDocument(BaseModel):
    document: str
    score: float


class SearchResponse(BaseModel):
    matching_documents: list[MatchingDocument]


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
