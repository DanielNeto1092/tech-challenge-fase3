from __future__ import annotations

import base64
import hashlib


def encrypt_text(text: str, key: str = "tech-challenge-fase3") -> str:
    payload = f"{key}:{text}".encode("utf-8")
    return base64.urlsafe_b64encode(payload).decode("ascii")


def fingerprint_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

