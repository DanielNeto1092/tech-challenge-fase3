from __future__ import annotations

from dataclasses import dataclass

from app.models import KnowledgeDocument, RetrievedContext
from app.retrieval import retrieve_documents
from vectorstore.index import DatasetVectorIndex


@dataclass
class HybridRetriever:
    documents: list[KnowledgeDocument]
    top_k: int = 3

    def __post_init__(self) -> None:
        docs = [document.model_dump() for document in self.documents]
        self._semantic_index = DatasetVectorIndex.from_documents(docs)

    def retrieve(self, question: str) -> list[RetrievedContext]:
        lexical = retrieve_documents(question, self.documents, top_k=self.top_k)
        by_doc_id = {item.document.doc_id: item for item in lexical}
        vector_matches = self._semantic_index.search(question, top_k=self.top_k)
        for hit in vector_matches:
            match = KnowledgeDocument.model_validate(hit.document)
            normalized = max(0.1, float(hit.score))
            if match.doc_id in by_doc_id:
                by_doc_id[match.doc_id].score += normalized
            else:
                by_doc_id[match.doc_id] = RetrievedContext(document=match, score=normalized)

        ranked = sorted(by_doc_id.values(), key=lambda item: item.score, reverse=True)
        return ranked[: self.top_k]
