from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.models import KnowledgeDocument, RetrievedContext
from app.retrieval import retrieve_documents

try:
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document
    from langchain_core.embeddings.fake import DeterministicFakeEmbedding
except ImportError:  # pragma: no cover - fallback path is tested indirectly
    FAISS = None
    Document = None
    DeterministicFakeEmbedding = None


@dataclass
class HybridRetriever:
    documents: list[KnowledgeDocument]
    top_k: int = 3

    def __post_init__(self) -> None:
        self._faiss_store = self._build_faiss_store()

    def _build_faiss_store(self) -> Any:
        if not FAISS or not Document or not DeterministicFakeEmbedding:
            return None

        embeddings = DeterministicFakeEmbedding(size=32)
        docs = [
            Document(
                page_content=document.content,
                metadata={
                    "doc_id": document.doc_id,
                    "title": document.title,
                    "category": document.category,
                    "source": document.source,
                    "keywords": document.keywords,
                    "safety_tags": document.safety_tags,
                },
            )
            for document in self.documents
        ]
        return FAISS.from_documents(docs, embeddings)

    def retrieve(self, question: str) -> list[RetrievedContext]:
        lexical = retrieve_documents(question, self.documents, top_k=self.top_k)
        if not self._faiss_store:
            return lexical

        by_doc_id = {item.document.doc_id: item for item in lexical}
        vector_matches = self._faiss_store.similarity_search_with_score(question, k=self.top_k)
        for doc, score in vector_matches:
            match = KnowledgeDocument(
                doc_id=doc.metadata["doc_id"],
                title=doc.metadata["title"],
                category=doc.metadata["category"],
                content=doc.page_content,
                source=doc.metadata["source"],
                keywords=doc.metadata.get("keywords", []),
                safety_tags=doc.metadata.get("safety_tags", []),
            )
            normalized = max(0.1, 1 / (1 + float(score)))
            if match.doc_id in by_doc_id:
                by_doc_id[match.doc_id].score += normalized
            else:
                by_doc_id[match.doc_id] = RetrievedContext(document=match, score=normalized)

        ranked = sorted(by_doc_id.values(), key=lambda item: item.score, reverse=True)
        return ranked[: self.top_k]
