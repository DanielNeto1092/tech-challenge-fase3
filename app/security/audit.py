from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import uuid4

from app.config import AUDIT_LOG_FILE, LOGS_DIR
from app.security.anonymizer import anonymize_payload
from app.security.crypto import encrypt_text


class AuditLogger:
    def __init__(self) -> None:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type: str, payload: dict) -> str:
        audit_id = str(uuid4())
        record = {
            "audit_id": audit_id,
            "event_type": event_type,
            "timestamp": datetime.now(UTC).isoformat(),
            "payload": anonymize_payload(payload),
            "encrypted_payload": encrypt_text(json.dumps(anonymize_payload(payload), ensure_ascii=True)),
        }
        with AUDIT_LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=True) + "\n")
        return audit_id
