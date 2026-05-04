from __future__ import annotations

import json

from app.config import DATASETS_DIR
from app.models import KnowledgeDocument


def load_knowledge_base() -> list[KnowledgeDocument]:
    knowledge_file = DATASETS_DIR / "synthetic_womens_health_knowledge.json"
    with knowledge_file.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return [KnowledgeDocument.model_validate(item) for item in data]

