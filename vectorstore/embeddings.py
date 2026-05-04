from __future__ import annotations

import hashlib
import math
import re

from langchain_core.embeddings import Embeddings


TOKEN_PATTERN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)


class HashEmbeddingModel(Embeddings):
    """Deterministic local embedding model for offline dataset indexing."""

    def __init__(self, dimensions: int = 96) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = TOKEN_PATTERN.findall(text.lower())
        if not tokens:
            return vector

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            weight = 1.0 + (digest[5] / 255.0)
            vector[index] += sign * weight

        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.embed_many(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.embed(text)


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
