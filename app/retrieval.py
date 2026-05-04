from __future__ import annotations

from app.models import KnowledgeDocument, RetrievedContext


def _score_document(question: str, document: KnowledgeDocument) -> float:
    question_terms = set(question.lower().split())
    keyword_hits = sum(1 for keyword in document.keywords if keyword.lower() in question.lower())
    content_hits = sum(1 for term in question_terms if term in document.content.lower())
    return float(keyword_hits * 2 + content_hits)


def retrieve_documents(question: str, documents: list[KnowledgeDocument], top_k: int = 2) -> list[RetrievedContext]:
    scored = [
        RetrievedContext(document=document, score=_score_document(question, document))
        for document in documents
    ]
    ranked = sorted(scored, key=lambda item: item.score, reverse=True)
    return [item for item in ranked[:top_k] if item.score > 0]

