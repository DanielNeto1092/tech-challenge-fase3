from __future__ import annotations

import re
import unicodedata
from typing import Any


WHITESPACE_PATTERN = re.compile(r"\s+")
NOISE_PATTERN = re.compile(r"[^\w\s,.;:%/\-\(\)\[\]]+", re.UNICODE)
TOKEN_PATTERN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)
STRUCTURAL_KEYS = {
    "doc_id",
    "source",
    "category",
    "specialty",
    "document_type",
    "risk_level",
    "risk_classification",
    "keywords",
    "representativity_tags",
    "safety_tags",
    "_tokens",
}

MEDICAL_TERM_MAP = {
    "pos parto": "pos-parto",
    "pos-parto": "pos-parto",
    "pre natal": "pre-natal",
    "prenatal": "pre-natal",
    "sangramento uterino anormal": "sangramento uterino anormal",
    "mastalgia": "dor mamaria",
    "violencia de genero": "violencia de genero",
    "violencia domestica": "violencia domestica",
    "papanicolaou": "Papanicolau",
    "citologia oncologica": "Papanicolau",
    "mamografia de rastreio": "mamografia de rastreio",
    "dispareunia": "dor na relacao sexual",
}


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def clean_text(text: str) -> str:
    cleaned = text.replace("\u00a0", " ").replace("\n", " ").strip()
    cleaned = NOISE_PATTERN.sub(" ", cleaned)
    cleaned = WHITESPACE_PATTERN.sub(" ", cleaned)
    return cleaned.strip(" ,;")


def normalize_medical_terms(text: str) -> str:
    normalized = clean_text(text)
    lowered = strip_accents(normalized).lower()
    for raw, target in MEDICAL_TERM_MAP.items():
        lowered = lowered.replace(raw, target)
    return lowered


def standardize_text(text: str) -> str:
    normalized = normalize_medical_terms(text)
    normalized = normalized.replace("  ", " ")
    if not normalized:
        return normalized
    return normalized[0].upper() + normalized[1:]


def tokenize_text(text: str) -> list[str]:
    normalized = strip_accents(normalize_medical_terms(text)).lower()
    return TOKEN_PATTERN.findall(normalized)


def preprocess_value(value: Any) -> Any:
    if isinstance(value, str):
        return standardize_text(value)
    if isinstance(value, list):
        return [preprocess_value(item) for item in value]
    if isinstance(value, dict):
        return {key: preprocess_value(item) for key, item in value.items()}
    return value


def preprocess_record(record: dict[str, Any]) -> dict[str, Any]:
    processed: dict[str, Any] = {}
    for key, value in record.items():
        if key in STRUCTURAL_KEYS:
            processed[key] = value
        else:
            processed[key] = preprocess_value(value)
    processed["_tokens"] = tokenize_text(" ".join(_collect_text_fields(processed)))
    return processed


def _collect_text_fields(record: dict[str, Any]) -> list[str]:
    fields: list[str] = []
    for value in record.values():
        if isinstance(value, str):
            fields.append(value)
        elif isinstance(value, list):
            fields.extend(item for item in value if isinstance(item, str))
    return fields
