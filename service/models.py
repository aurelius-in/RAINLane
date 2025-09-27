from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.types import JSON
from sqlalchemy.sql import func

from service.db import Base


class Document(Base):
    __tablename__ = "documents"
    doc_hash = Column(String(128), primary_key=True)
    path = Column(String(1024), nullable=False)
    meta = Column(JSON, nullable=True)


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_hash = Column(String(128), nullable=False, index=True)
    section_id = Column(String(64), nullable=False)
    title = Column(String(512), nullable=True)
    text = Column(Text, nullable=False)


class Answer(Base):
    __tablename__ = "answers"
    id = Column(String(64), primary_key=True)
    lane = Column(String(32), nullable=False)
    answer = Column(Text, nullable=False)
    citations = Column(JSON, nullable=True)
    doc_hashes = Column(JSON, nullable=True)
    model = Column(JSON, nullable=True)
    signature = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


