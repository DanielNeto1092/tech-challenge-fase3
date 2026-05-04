from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class KnowledgeDocument(BaseModel):
    doc_id: str
    title: str
    category: str
    content: str
    source: str
    specialty: str = "saude_da_mulher"
    document_type: str = "protocolo"
    keywords: list[str] = Field(default_factory=list)
    safety_tags: list[str] = Field(default_factory=list)
    representativity_tags: list[str] = Field(default_factory=list)


class RetrievedContext(BaseModel):
    document: KnowledgeDocument
    score: float


class AssistantRequest(BaseModel):
    question: str
    patient_context: dict[str, Any] = Field(default_factory=dict)
    requester_id: str = "demo_clinician"
    requester_role: str = "profissional_saude"
    specialty: str = "saude_da_mulher"
    access_reason: str = "apoio_clinico_academico"
    auth_token: str | None = None


class AssistantResponse(BaseModel):
    summary: str
    justification: str
    source: str
    confidence: Literal["low", "medium", "high"]
    limits: str
    data_needs: str
    referral: str
    risk_level: Literal["low", "moderate", "high", "critical"]
    professional_validation_required: bool = True
    safe: bool = True
    red_flags: list[str] = Field(default_factory=list)


class TriageInput(BaseModel):
    sintomas: list[str]
    contexto: str = ""
    idade: int | None = None
    gestante: bool = False


class ViolenceInput(BaseModel):
    sinais_alerta: list[str]
    contexto: str = ""
    risco_imediato: bool = False


class ObstetricInput(BaseModel):
    idade_gestacional_semanas: int
    sintomas: list[str]
    comorbidades: list[str] = Field(default_factory=list)
    contexto: str = ""


class PreventionInput(BaseModel):
    idade: int
    historico: list[str] = Field(default_factory=list)
    exames_realizados: list[str] = Field(default_factory=list)
    contexto: str = ""


class FlowResult(BaseModel):
    flow_name: str
    summary: str
    urgency: Literal["routine", "priority", "urgent", "emergency"]
    recommended_actions: list[str]
    suggested_exams: list[str] = Field(default_factory=list)
    escalation: str
    notes: list[str] = Field(default_factory=list)
    audit_id: str | None = None
