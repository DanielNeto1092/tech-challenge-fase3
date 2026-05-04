from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
METRICS_FILE = DATA_DIR / "finetuning_metrics.json"


def load_split(name: str) -> list[dict]:
    file_path = DATA_DIR / f"{name}.json"
    return json.loads(file_path.read_text(encoding="utf-8"))


def simulate_training_epoch(train_records: list[dict], epoch: int) -> dict:
    coverage = min(0.70 + epoch * 0.08, 0.95)
    safety = min(0.82 + epoch * 0.04, 0.98)
    consistency = min(0.74 + epoch * 0.05, 0.97)
    return {
        "epoch": epoch,
        "train_examples": len(train_records),
        "retrieval_grounding_score": round(coverage, 3),
        "safety_compliance_score": round(safety, 3),
        "format_consistency_score": round(consistency, 3),
    }


def main() -> None:
    train = load_split("train")
    validation = load_split("validation")
    test = load_split("test")
    history = [simulate_training_epoch(train, epoch) for epoch in range(1, 4)]
    summary = {
        "mode": "simulation",
        "train_size": len(train),
        "validation_size": len(validation),
        "test_size": len(test),
        "history": history,
        "evaluation": {
            "validation_grounding": 0.88,
            "validation_safety": 0.94,
            "test_grounding": 0.85,
            "test_safety": 0.93,
        },
        "notes": [
            "Simulacao academica para demonstrar pipeline de fine-tuning com dados sinteticos.",
            "Em ambiente real, substituir por treinamento supervisionado de modelo open-source pequeno com GPUs.",
        ],
    }
    METRICS_FILE.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"Metricas simuladas gravadas em {METRICS_FILE}")


if __name__ == "__main__":
    main()
