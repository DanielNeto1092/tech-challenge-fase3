from __future__ import annotations

from app.knowledge_base import load_knowledge_base
from app.models import KnowledgeDocument


class ProtocolRepository:
    def __init__(self) -> None:
        self.documents = load_knowledge_base()

    def list_protocols(self, category: str | None = None) -> list[KnowledgeDocument]:
        if not category:
            return self.documents
        return [document for document in self.documents if document.category == category]

    def get_protocol(self, doc_id: str) -> KnowledgeDocument | None:
        for document in self.documents:
            if document.doc_id == doc_id:
                return document
        return None
