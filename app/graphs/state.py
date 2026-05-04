from __future__ import annotations

from typing import Any, TypedDict


class FlowState(TypedDict, total=False):
    input: dict[str, Any]
    risk_level: str
    urgency: str
    summary: str
    recommended_actions: list[str]
    suggested_exams: list[str]
    escalation: str
    notes: list[str]
    protocol_contexts: list[str]
