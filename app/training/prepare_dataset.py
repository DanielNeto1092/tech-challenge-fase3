from __future__ import annotations

import json
from pathlib import Path
from random import Random
from collections import Counter

from app.security.anonymizer import anonymize_payload


BASE_DIR = Path(__file__).resolve().parent.parent.parent
SOURCE_FILE = BASE_DIR / "datasets" / "synthetic_womens_health_knowledge.json"
OUTPUT_DIR = BASE_DIR / "data"
RNG = Random(42)


def normalize_text(text: str) -> str:
    replacements = {
        "visão": "visao",
        "pós-parto": "pos-parto",
        "ginecológico": "ginecologico",
    }
    normalized = text.lower()
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def build_training_records() -> list[dict]:
    docs = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    records = []
    for item in docs:
        records.append(
            {
                "instruction": f"Explique com segurança o tema: {item['title']}",
                "input": anonymize_payload(item["content"]),
                "output": {
                    "summary": item["content"],
                    "source": item["source"],
                    "category": item["category"],
                    "specialty": item.get("specialty", "saude_da_mulher"),
                },
                "metadata": {
                    "doc_id": item["doc_id"],
                    "document_type": item.get("document_type", "protocolo"),
                    "representativity_tags": item.get("representativity_tags", []),
                },
            }
        )
    return records


def validate_training_record(record: dict) -> list[str]:
    errors = []
    if not record.get("instruction"):
        errors.append("instruction_missing")
    if not record.get("input"):
        errors.append("input_missing")
    if not record.get("output", {}).get("summary"):
        errors.append("output_summary_missing")
    return errors


def summarize_balance(records: list[dict]) -> dict[str, dict[str, int]]:
    category_counter = Counter(record["output"]["category"] for record in records)
    specialty_counter = Counter(record["output"]["specialty"] for record in records)
    representativity_counter = Counter(
        tag
        for record in records
        for tag in record.get("metadata", {}).get("representativity_tags", [])
    )
    return {
        "categories": dict(category_counter),
        "specialties": dict(specialty_counter),
        "representativity_tags": dict(representativity_counter),
    }


def export_jsonl(split_name: str, items: list[dict]) -> None:
    output_file = OUTPUT_DIR / f"{split_name}.jsonl"
    with output_file.open("w", encoding="utf-8") as file:
        for item in items:
            file.write(json.dumps(item, ensure_ascii=True) + "\n")


def split_dataset(records: list[dict]) -> dict[str, list[dict]]:
    shuffled = records[:]
    RNG.shuffle(shuffled)
    total = len(shuffled)
    train_end = max(1, int(total * 0.6))
    val_end = max(train_end + 1, int(total * 0.8))
    return {
        "train": shuffled[:train_end],
        "validation": shuffled[train_end:val_end],
        "test": shuffled[val_end:],
    }


def main() -> None:
    records = build_training_records()
    for record in records:
        record["input"] = normalize_text(record["input"])
    validation_errors = {
        record["metadata"]["doc_id"]: validate_training_record(record)
        for record in records
        if validate_training_record(record)
    }
    splits = split_dataset(records)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for split_name, items in splits.items():
        output_file = OUTPUT_DIR / f"{split_name}.json"
        output_file.write_text(json.dumps(items, ensure_ascii=True, indent=2), encoding="utf-8")
        export_jsonl(split_name, items)

    manifest = {
        "mode": "academic_simulation",
        "source_dataset": str(SOURCE_FILE.name),
        "records_total": len(records),
        "validation_errors": validation_errors,
        "balance_summary": summarize_balance(records),
        "specialist_curation": {
            "status": "simulada",
            "review_required_roles": ["ginecologia", "obstetricia", "psicologia", "assistencia_social"],
        },
    }
    (OUTPUT_DIR / "fine_tuning_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )
    print("Dataset preparado em data/train.json, data/validation.json, data/test.json e arquivos JSONL")


if __name__ == "__main__":
    main()
