from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_base import load_knowledge_base
from app.models import KnowledgeDocument
from app.retrieval import retrieve_documents


@dataclass
class ProtocolContextService:
    documents: list[KnowledgeDocument]

    @classmethod
    def build(cls) -> "ProtocolContextService":
        return cls(documents=load_knowledge_base())

    def find_relevant(
        self,
        query: str,
        *,
        specialties: set[str] | None = None,
        categories: set[str] | None = None,
        top_k: int = 2,
    ) -> list[KnowledgeDocument]:
        filtered = self.documents
        if specialties:
            filtered = [document for document in filtered if document.specialty in specialties]
        if categories:
            filtered = [document for document in filtered if document.category in categories]
        matches = retrieve_documents(query, filtered, top_k=top_k)
        return [match.document for match in matches]

    @staticmethod
    def summarize_sources(documents: list[KnowledgeDocument]) -> list[str]:
        return [f"Base sintética consultada: {document.title} ({document.source})" for document in documents]
