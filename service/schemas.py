from pydantic import BaseModel
from typing import List, Dict


class IngestReq(BaseModel):
    path: str


class AnswerReq(BaseModel):
    query: str
    user_role: str


class Citation(BaseModel):
    doc_id: str
    section: str
    span: List[int]


class ModelInfo(BaseModel):
    name: str
    version: str
    selector_reason: str


class AnswerCard(BaseModel):
    id: str
    lane: str
    answer: str
    citations: List[Citation] = []
    doc_hashes: List[Dict[str, str]] = []
    model: ModelInfo
    signature: Dict[str, str] = {}
    metrics: Dict[str, float] = {}


class GoldSubmit(BaseModel):
    question: str
    answer: str
    citations: List[Citation] = []
    roles: List[str] = ["Operator"]


