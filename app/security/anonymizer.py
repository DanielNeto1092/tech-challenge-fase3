from __future__ import annotations

import re
from typing import Any


PHONE_PATTERN = re.compile(r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9?\d{4})-?\d{4}\b")
EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
CPF_PATTERN = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")


def mask_sensitive_text(text: str) -> str:
    text = PHONE_PATTERN.sub("[TELEFONE_REMOVIDO]", text)
    text = EMAIL_PATTERN.sub("[EMAIL_REMOVIDO]", text)
    text = CPF_PATTERN.sub("[CPF_REMOVIDO]", text)
    return text


def anonymize_payload(payload: Any) -> Any:
    if isinstance(payload, str):
        return mask_sensitive_text(payload)
    if isinstance(payload, list):
        return [anonymize_payload(item) for item in payload]
    if isinstance(payload, dict):
        sanitized: dict[str, Any] = {}
        for key, value in payload.items():
            lowered = key.lower()
            if lowered in {"nome", "name", "cpf", "email", "telefone", "phone", "address", "endereco"}:
                sanitized[key] = "[DADO_SENSIVEL_REMOVIDO]"
            else:
                sanitized[key] = anonymize_payload(value)
        return sanitized
    return payload
