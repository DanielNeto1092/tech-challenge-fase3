from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .anonymizer import anonymize_record
from .formatter import build_rag_documents
from .preprocess import preprocess_record
from .validator import summarize_issues, validate_record


BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"

DATASET_REGISTRY = {
    "womens_health_qa": DATASETS_DIR / "womens_health_qa" / "records.json",
    "gynecological_protocols": DATASETS_DIR / "gynecological_protocols" / "records.json",
    "obstetric_guidelines": DATASETS_DIR / "obstetric_guidelines" / "records.json",
    "violence_detection": DATASETS_DIR / "violence_detection" / "records.json",
    "contraceptive": DATASETS_DIR / "contraceptive" / "records.json",
    "breast_cancer": DATASETS_DIR / "breast_cancer" / "records.json",
    "menstrual_health": DATASETS_DIR / "menstrual_health" / "records.json",
    "maternal_mental_health": DATASETS_DIR / "maternal_mental_health" / "records.json",
}


def load_json_records(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_all_datasets() -> dict[str, list[dict[str, Any]]]:
    return {dataset_name: load_json_records(path) for dataset_name, path in DATASET_REGISTRY.items()}


def load_processed_datasets(
    *,
    apply_preprocess: bool = True,
    apply_anonymization: bool = True,
    validate: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    processed: dict[str, list[dict[str, Any]]] = {}
    for dataset_name, records in load_all_datasets().items():
        items: list[dict[str, Any]] = []
        for record in records:
            current = dict(record)
            if apply_preprocess:
                current = preprocess_record(current)
            if apply_anonymization:
                current = anonymize_record(current)
            if validate:
                issues = validate_record(current)
                if issues:
                    messages = ", ".join(issue.message for issue in issues)
                    raise ValueError(f"Registro invalido em {dataset_name}/{record.get('doc_id')}: {messages}")
            items.append(current)
        processed[dataset_name] = items
    return processed


def build_validation_manifest() -> dict[str, list[str]]:
    manifest: dict[str, list[str]] = {}
    for dataset_name, records in load_all_datasets().items():
        issues = summarize_issues(records)
        if issues:
            manifest[dataset_name] = [f"{doc_id}:{', '.join(messages)}" for doc_id, messages in issues.items()]
    return manifest


def load_knowledge_documents() -> list[Any]:
    from app.models import KnowledgeDocument

    documents = build_rag_documents(load_processed_datasets())
    return [KnowledgeDocument.model_validate(item) for item in documents]
