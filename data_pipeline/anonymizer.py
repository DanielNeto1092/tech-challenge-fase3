from __future__ import annotations

import re
from typing import Any


PHONE_PATTERN = re.compile(r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9?\d{4})-?\d{4}\b")
EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
CPF_PATTERN = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
ID_PATTERN = re.compile(r"\b(?:rg|cartao sus|cns|prontuario)\s*[:#]?\s*\d+\b", re.IGNORECASE)
DATE_PATTERN = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")
ADDRESS_PATTERN = re.compile(r"\b(?:rua|avenida|av\.?|travessa|alameda)\s+[a-z0-9\s]+", re.IGNORECASE)
PATIENT_NAME_PATTERN = re.compile(r"\bPaciente\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)*")
AGE_PATTERN = re.compile(r"\b(\d{1,2})\s+anos\b", re.IGNORECASE)
FULL_NUMBER_PATTERN = re.compile(r"\b\d{5,}\b")

SENSITIVE_KEYS = {
    "nome",
    "name",
    "cpf",
    "email",
    "telefone",
    "phone",
    "endereco",
    "address",
    "prontuario",
    "cartao_sus",
    "cns",
}


def age_bucket(age: int) -> str:
    lower = (age // 5) * 5
    upper = lower + 5
    return f"idade {lower}-{upper}"


def anonymize_text(text: str) -> str:
    text = PATIENT_NAME_PATTERN.sub("Paciente [ANON]", text)
    text = PHONE_PATTERN.sub("[TELEFONE_REMOVIDO]", text)
    text = EMAIL_PATTERN.sub("[EMAIL_REMOVIDO]", text)
    text = CPF_PATTERN.sub("[CPF_REMOVIDO]", text)
    text = ID_PATTERN.sub("[ID_REMOVIDO]", text)
    text = DATE_PATTERN.sub("[DATA_REMOVIDA]", text)
    text = ADDRESS_PATTERN.sub("[ENDERECO_REMOVIDO]", text)
    text = FULL_NUMBER_PATTERN.sub("[NUMERO_REMOVIDO]", text)
    text = AGE_PATTERN.sub(lambda match: age_bucket(int(match.group(1))), text)
    return text


def anonymize_value(value: Any) -> Any:
    if isinstance(value, str):
        return anonymize_text(value)
    if isinstance(value, list):
        return [anonymize_value(item) for item in value]
    if isinstance(value, dict):
        masked: dict[str, Any] = {}
        for key, item in value.items():
            if key.lower() in SENSITIVE_KEYS:
                masked[key] = "[DADO_SENSIVEL_REMOVIDO]"
            else:
                masked[key] = anonymize_value(item)
        return masked
    return value


def anonymize_record(record: dict[str, Any]) -> dict[str, Any]:
    return anonymize_value(record)
