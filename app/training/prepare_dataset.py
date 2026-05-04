from __future__ import annotations

import sys
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from data_pipeline.formatter import build_instruction_corpus, export_json, export_jsonl, split_records
from data_pipeline.loader import build_validation_manifest, load_processed_datasets
from data_pipeline.preprocess import normalize_medical_terms

OUTPUT_DIR = BASE_DIR / "data"


def normalize_text(text: str) -> str:
    return normalize_medical_terms(text)


def build_training_records() -> list[dict]:
    bundle = load_processed_datasets()
    return build_instruction_corpus(bundle)


def validate_training_record(record: dict) -> list[str]:
    errors = []
    if not record.get("instruction"):
        errors.append("instruction_missing")
    if not record.get("input"):
        errors.append("input_missing")
    if not record.get("output"):
        errors.append("output_summary_missing")
    return errors


def summarize_balance(records: list[dict]) -> dict[str, dict[str, int]]:
    category_counter = Counter(record["metadata"]["dataset"] for record in records)
    specialty_counter = Counter(record["metadata"]["specialty"] for record in records)
    representativity_counter = Counter(
        tag
        for record in records
        for tag in record["metadata"].get("representativity_tags", [])
    )
    return {
        "categories": dict(category_counter),
        "specialties": dict(specialty_counter),
        "representativity_tags": dict(representativity_counter),
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
    splits = split_records(records)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for split_name, items in splits.items():
        export_json(OUTPUT_DIR / f"{split_name}.json", items)
        export_jsonl(OUTPUT_DIR / f"{split_name}.jsonl", items)

    manifest = {
        "mode": "academic_simulation",
        "source_dataset": "multi_domain_synthetic_bundle",
        "records_total": len(records),
        "validation_errors": validation_errors,
        "dataset_validation_manifest": build_validation_manifest(),
        "balance_summary": summarize_balance(records),
        "specialist_curation": {
            "status": "simulada",
            "review_required_roles": ["ginecologia", "obstetricia", "psicologia", "assistencia_social"],
        },
    }
    export_json(OUTPUT_DIR / "fine_tuning_manifest.json", manifest)
    print("Dataset preparado em data/train.json, data/validation.json, data/test.json e arquivos JSONL")


if __name__ == "__main__":
    main()
