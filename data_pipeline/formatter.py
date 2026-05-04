from __future__ import annotations

import json
from pathlib import Path
from random import Random
from typing import Any


RNG = Random(42)
PROFESSIONAL_ALERT = (
    "Ferramenta sintetica de apoio. Validacao profissional obrigatoria. "
    "Nao realizar prescricao nem diagnostico definitivo."
)

SPECIALTY_BY_DATASET = {
    "womens_health_qa": "saude_da_mulher",
    "gynecological_protocols": "ginecologia",
    "obstetric_guidelines": "obstetricia",
    "violence_detection": "protecao_social",
    "contraceptive": "planejamento_familiar",
    "breast_cancer": "mastologia_preventiva",
    "menstrual_health": "ginecologia",
    "maternal_mental_health": "saude_mental",
}

DOCUMENT_TYPE_BY_DATASET = {
    "womens_health_qa": "faq",
    "gynecological_protocols": "protocolo",
    "obstetric_guidelines": "protocolo",
    "violence_detection": "protocolo_segurança",
    "contraceptive": "faq",
    "breast_cancer": "protocolo",
    "menstrual_health": "faq",
    "maternal_mental_health": "protocolo",
}

RISK_MAP = {"baixo": "low", "moderado": "moderate", "alto": "high", "critico": "critical"}


def _keywords_from_record(record: dict[str, Any]) -> list[str]:
    if "keywords" in record:
        return list(record["keywords"])
    if "symptoms" in record:
        return list(record["symptoms"])
    return []


def _safety_tags(record: dict[str, Any]) -> list[str]:
    tags = list(record.get("safety_tags", []))
    if record.get("requires_referral") or record.get("requires_intervention"):
        tags.append("requires_professional_referral")
    tags.append("no_prescription")
    return sorted(set(tags))


def to_instruction_record(dataset_name: str, record: dict[str, Any]) -> dict[str, Any]:
    if "question" in record:
        instruction = f"Responda com seguranca a uma pergunta de {dataset_name.replace('_', ' ')}."
        input_text = f"Pergunta: {record['question']}\nContexto: {record['context']}"
        output_text = f"{record['answer']} {PROFESSIONAL_ALERT}"
    elif "condition" in record:
        instruction = f"Organize um protocolo sintetico para {record['condition']}."
        input_text = (
            f"Condicao: {record['condition']}\n"
            f"Sintomas: {', '.join(record['symptoms'])}\n"
            f"Classificacao: {record['risk_classification']}"
        )
        output_text = (
            "Acoes recomendadas: "
            + "; ".join(record["recommended_actions"])
            + f". Encaminhamento obrigatorio: {'sim' if record['requires_referral'] else 'nao'}. "
            + PROFESSIONAL_ALERT
        )
    else:
        instruction = "Analise sinais sinteticos de violencia domestica sem gerar conduta prescritiva."
        input_text = f"Relato: {record['text']}\nRisco: {record['risk_level']}"
        output_text = (
            "Risco identificado: "
            + record["risk_level"]
            + f". Intervencao obrigatoria: {'sim' if record['requires_intervention'] else 'nao'}. "
            + PROFESSIONAL_ALERT
        )

    return {
        "instruction": instruction,
        "input": input_text,
        "output": output_text,
        "metadata": {
            "doc_id": record["doc_id"],
            "dataset": dataset_name,
            "source": record["source"],
            "specialty": record.get("specialty", SPECIALTY_BY_DATASET[dataset_name]),
            "document_type": record.get("document_type", DOCUMENT_TYPE_BY_DATASET[dataset_name]),
            "representativity_tags": list(record.get("representativity_tags", [])),
        },
    }


def to_rag_document(dataset_name: str, record: dict[str, Any]) -> dict[str, Any]:
    specialty = record.get("specialty", SPECIALTY_BY_DATASET[dataset_name])
    document_type = record.get("document_type", DOCUMENT_TYPE_BY_DATASET[dataset_name])

    if "question" in record:
        title = record.get("title", record["question"])
        content = f"{record['context']} {record['answer']} {PROFESSIONAL_ALERT}"
        category = record.get("category", dataset_name)
        risk_level = RISK_MAP[str(record["risk_level"]).lower()]
    elif "condition" in record:
        title = record.get("title", record["condition"])
        content = (
            f"Condicao: {record['condition']}. "
            f"Sintomas principais: {', '.join(record['symptoms'])}. "
            f"Classificacao de risco: {record['risk_classification']}. "
            f"Acoes recomendadas: {'; '.join(record['recommended_actions'])}. "
            f"Encaminhamento obrigatorio: {'sim' if record['requires_referral'] else 'nao'}. "
            f"{PROFESSIONAL_ALERT}"
        )
        category = record.get("category", dataset_name)
        risk_level = RISK_MAP[str(record["risk_classification"]).lower()]
    else:
        title = record.get("title", f"Padrao de risco {record['doc_id']}")
        content = (
            f"Relato sintetico: {record['text']}. "
            f"Score de risco: {record['risk_score']}. "
            f"Nivel: {record['risk_level']}. "
            f"Requer intervencao: {'sim' if record['requires_intervention'] else 'nao'}. "
            f"{PROFESSIONAL_ALERT}"
        )
        category = record.get("category", dataset_name)
        risk_level = RISK_MAP[str(record["risk_level"]).lower()]

    return {
        "doc_id": record["doc_id"],
        "title": title,
        "category": category,
        "content": content,
        "source": record["source"],
        "specialty": specialty,
        "document_type": document_type,
        "keywords": _keywords_from_record(record),
        "safety_tags": _safety_tags(record) + [f"risk::{risk_level}"],
        "representativity_tags": list(record.get("representativity_tags", [])),
    }


def build_instruction_corpus(bundle: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for dataset_name, items in bundle.items():
        for item in items:
            records.append(to_instruction_record(dataset_name, item))
    return records


def build_rag_documents(bundle: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for dataset_name, items in bundle.items():
        for item in items:
            documents.append(to_rag_document(dataset_name, item))
    return documents


def split_records(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    shuffled = records[:]
    RNG.shuffle(shuffled)
    total = len(shuffled)
    train_end = max(1, int(total * 0.7))
    validation_end = max(train_end + 1, int(total * 0.85))
    return {
        "train": shuffled[:train_end],
        "validation": shuffled[train_end:validation_end],
        "test": shuffled[validation_end:],
    }


def export_json(output_path: Path, payload: Any) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def export_jsonl(output_path: Path, payload: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for item in payload:
            handle.write(json.dumps(item, ensure_ascii=True) + "\n")
