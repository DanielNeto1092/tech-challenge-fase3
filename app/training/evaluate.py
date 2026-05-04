from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
METRICS_FILE = BASE_DIR / "data" / "finetuning_metrics.json"


def main() -> None:
    payload = json.loads(METRICS_FILE.read_text(encoding="utf-8"))
    evaluation = payload["evaluation"]
    print("Resumo de avaliacao")
    for key, value in evaluation.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
