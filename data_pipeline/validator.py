from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .anonymizer import anonymize_text


VALID_RISK_LEVELS = {"baixo", "moderado", "alto"}
VALID_PROTOCOL_CLASSIFICATIONS = {"baixo", "moderado", "alto", "critico"}

REQUIRED_FIELDS = {
    "qa": {"doc_id", "question", "context", "answer", "source", "risk_level"},
    "protocol": {
        "doc_id",
        "condition",
        "symptoms",
        "risk_classification",
        "recommended_actions",
        "requires_referral",
    },
    "violence": {
        "doc_id",
        "text",
        "risk_score",
        "risk_level",
        "requires_intervention",
    },
}


@dataclass
class ValidationIssue:
    record_id: str
    message: str


def contains_sensitive_data(record: dict[str, Any]) -> bool:
    for value in record.values():
        if isinstance(value, str) and anonymize_text(value) != value:
            return True
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and anonymize_text(item) != item:
                    return True
    return False


def infer_record_type(record: dict[str, Any]) -> str:
    if "question" in record and "answer" in record:
        return "qa"
    if "condition" in record and "recommended_actions" in record:
        return "protocol"
    if "risk_score" in record and "requires_intervention" in record:
        return "violence"
    raise ValueError(f"Formato de registro nao reconhecido: {record.keys()}")


def validate_record(record: dict[str, Any]) -> list[ValidationIssue]:
    record_id = str(record.get("doc_id", "sem_id"))
    issues: list[ValidationIssue] = []
    record_type = infer_record_type(record)

    missing = REQUIRED_FIELDS[record_type] - record.keys()
    for field_name in sorted(missing):
        issues.append(ValidationIssue(record_id, f"campo_obrigatorio_ausente:{field_name}"))

    risk_level = str(record.get("risk_level", "")).lower()
    risk_classification = str(record.get("risk_classification", "")).lower()

    if record_type in {"qa", "violence"} and risk_level not in VALID_RISK_LEVELS:
        issues.append(ValidationIssue(record_id, "nivel_risco_invalido"))

    if record_type == "protocol" and risk_classification not in VALID_PROTOCOL_CLASSIFICATIONS:
        issues.append(ValidationIssue(record_id, "classificacao_risco_invalida"))

    if record_type == "violence":
        risk_score = float(record.get("risk_score", 0))
        if not 0 <= risk_score <= 1:
            issues.append(ValidationIssue(record_id, "risk_score_fora_do_intervalo"))

    if contains_sensitive_data(record):
        issues.append(ValidationIssue(record_id, "possivel_dado_sensivel"))

    if record_type == "protocol":
        high_risk = risk_classification in {"alto", "critico"}
        if high_risk and not bool(record.get("requires_referral")):
            issues.append(ValidationIssue(record_id, "risco_alto_sem_encaminhamento"))

    if record_type == "qa":
        answer = str(record.get("answer", "")).lower()
        if "mg" in answer or "dose" in answer:
            issues.append(ValidationIssue(record_id, "conteudo_potencialmente_prescritivo"))

    return issues


def summarize_issues(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    summary: dict[str, list[str]] = {}
    for record in records:
        issues = validate_record(record)
        if issues:
            summary[str(record.get("doc_id", "sem_id"))] = [issue.message for issue in issues]
    return summary
