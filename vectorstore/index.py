from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from langchain_community.vectorstores import FAISS

try:
    from langchain_core.documents import Document
    from langchain_core.runnables import RunnableLambda
except ImportError:  # pragma: no cover - local fallback when LangChain is absent
    @dataclass
    class Document:  # type: ignore[override]
        page_content: str
        metadata: dict[str, Any]

    class RunnableLambda:  # type: ignore[override]
        def __init__(self, func):
            self._func = func

        def invoke(self, payload: dict[str, Any]) -> dict[str, Any]:
            return self._func(payload)

from data_pipeline.formatter import PROFESSIONAL_ALERT, build_rag_documents
from data_pipeline.loader import load_processed_datasets
from vectorstore.embeddings import HashEmbeddingModel

TOKEN_PATTERN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)


@dataclass
class SearchResult:
    document: dict[str, Any]
    score: float


class DatasetVectorIndex:
    def __init__(self, documents: list[dict[str, Any]], model: HashEmbeddingModel, faiss_store: FAISS) -> None:
        self.documents = documents
        self.model = model
        self.faiss_store = faiss_store

    @classmethod
    def from_documents(
        cls,
        documents: list[dict[str, Any]],
        model: HashEmbeddingModel | None = None,
    ) -> "DatasetVectorIndex":
        embedding_model = model or HashEmbeddingModel()
        langchain_docs = [Document(page_content=document["content"], metadata=document) for document in documents]
        faiss_store = FAISS.from_documents(langchain_docs, embedding_model)
        return cls(documents=documents, model=embedding_model, faiss_store=faiss_store)

    @classmethod
    def from_datasets(cls) -> "DatasetVectorIndex":
        documents = build_rag_documents(load_processed_datasets())
        return cls.from_documents(documents)

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_tokens = set(TOKEN_PATTERN.findall(query.lower()))
        raw_hits = self.faiss_store.similarity_search_with_score(query, k=max(top_k * 4, top_k))
        scored = []
        for document, distance in raw_hits:
            payload = dict(document.metadata)
            semantic_score = 1.0 / (1.0 + float(distance))
            score = (0.75 * semantic_score) + (0.25 * _lexical_score(query_tokens, payload))
            scored.append(SearchResult(document=payload, score=score))
        ranked = sorted(scored, key=lambda item: item.score, reverse=True)
        return [item for item in ranked[:top_k] if item.score > 0.02]

    def save(self, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        self.faiss_store.save_local(str(output_dir), index_name="dataset_index")
        metadata_path = output_dir / "index.json"
        metadata_path.write_text(
            json.dumps({"documents": self.documents, "engine": "faiss"}, ensure_ascii=True, indent=2),
            encoding="utf-8",
        )
        return metadata_path

    @classmethod
    def load(cls, input_path: Path, model: HashEmbeddingModel | None = None) -> "DatasetVectorIndex":
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        embedding_model = model or HashEmbeddingModel()
        faiss_store = FAISS.load_local(
            str(input_path.parent),
            embedding_model,
            index_name="dataset_index",
            allow_dangerous_deserialization=True,
        )
        return cls(documents=payload["documents"], model=embedding_model, faiss_store=faiss_store)


def build_langchain_retriever(index: DatasetVectorIndex | None = None, top_k: int = 3):
    semantic_index = index or DatasetVectorIndex.from_datasets()
    return semantic_index.faiss_store.as_retriever(search_kwargs={"k": top_k})


def build_qa_chain(index: DatasetVectorIndex | None = None):
    semantic_index = index or DatasetVectorIndex.from_datasets()
    retriever = build_langchain_retriever(semantic_index)

    def _run(payload: dict[str, Any]) -> dict[str, Any]:
        query = payload["query"]
        hits = semantic_index.search(query, top_k=payload.get("top_k", 3))
        retrieved_docs = retriever.invoke(query)
        context = [
            {
                "doc_id": item.document["doc_id"],
                "title": item.document["title"],
                "source": item.document["source"],
                "score": round(item.score, 4),
            }
            for item in hits
        ]
        if not hits:
            answer = (
                "Nao encontrei contexto suficiente na base sintetica. "
                f"{PROFESSIONAL_ALERT}"
            )
        else:
            snippets = " ".join(document.page_content for document in retrieved_docs[:2])
            answer = f"{snippets} {PROFESSIONAL_ALERT}"
        return {"query": query, "answer": answer, "context": context}

    return RunnableLambda(_run)


def run_rag_pipeline(query: str, index: DatasetVectorIndex | None = None, top_k: int = 3) -> dict[str, Any]:
    return build_qa_chain(index).invoke({"query": query, "top_k": top_k})


def _lexical_score(query_tokens: set[str], document: dict[str, Any]) -> float:
    doc_tokens = set(TOKEN_PATTERN.findall(document["content"].lower()))
    doc_tokens.update(TOKEN_PATTERN.findall(document["title"].lower()))
    for keyword in document.get("keywords", []):
        doc_tokens.update(TOKEN_PATTERN.findall(str(keyword).lower()))
    if not query_tokens or not doc_tokens:
        return 0.0
    return len(query_tokens & doc_tokens) / len(query_tokens)
