from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime

from app.config import ACCESS_LOG_FILE, LOGS_DIR
from app.security.crypto import encrypt_text, fingerprint_text


class AccessMonitor:
    def __init__(self) -> None:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def log_access(
        self,
        *,
        endpoint: str,
        specialty: str,
        requester_id: str,
        outcome: str,
        reason: str,
    ) -> None:
        record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "endpoint": endpoint,
            "specialty": specialty,
            "requester_fingerprint": fingerprint_text(requester_id),
            "encrypted_requester": encrypt_text(requester_id),
            "outcome": outcome,
            "reason": reason,
        }
        with ACCESS_LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=True) + "\n")

    def generate_specialty_report(self) -> dict[str, dict[str, int]]:
        report: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        if not ACCESS_LOG_FILE.exists():
            return {}
        for line in ACCESS_LOG_FILE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            specialty = record["specialty"]
            report[specialty]["total_accesses"] += 1
            report[specialty][record["endpoint"]] += 1
            report[specialty][f"outcome::{record['outcome']}"] += 1
        return {key: dict(value) for key, value in report.items()}
