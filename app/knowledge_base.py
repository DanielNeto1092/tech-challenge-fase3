from __future__ import annotations

from app.models import KnowledgeDocument


def load_knowledge_base() -> list[KnowledgeDocument]:
    from data_pipeline.loader import load_knowledge_documents

    return load_knowledge_documents()
