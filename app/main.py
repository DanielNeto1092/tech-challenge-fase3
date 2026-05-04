from __future__ import annotations

from fastapi import FastAPI
from fastapi import HTTPException

from app.assistant import WomensHealthAssistant
from app.models import (
    AssistantRequest,
    AssistantResponse,
    FlowResult,
    ObstetricInput,
    PreventionInput,
    TriageInput,
    ViolenceInput,
)
from app.protocols import ProtocolRepository
from app.graphs.obstetric_graph import run_obstetric_flow
from app.graphs.prevention_graph import run_prevention_flow
from app.graphs.triage_graph import run_triage_flow
from app.graphs.violence_graph import run_violence_flow
from app.security.access_monitor import AccessMonitor


app = FastAPI(
    title="Assistente Virtual Médico - Saúde e Segurança da Mulher",
    version="0.1.0",
    description="Ferramenta acadêmica de apoio clínico com guardrails de segurança.",
)
assistant = WomensHealthAssistant()
protocol_repository = ProtocolRepository()
access_monitor = AccessMonitor()


def _log_endpoint_access(endpoint: str, specialty: str, reason: str) -> None:
    access_monitor.log_access(
        endpoint=endpoint,
        specialty=specialty,
        requester_id="api_system",
        outcome="granted",
        reason=reason,
    )


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/assist", response_model=AssistantResponse)
def assist(request: AssistantRequest) -> AssistantResponse:
    return assistant.answer(request)


@app.post("/assistente/pergunta", response_model=AssistantResponse)
def assistente_pergunta(request: AssistantRequest) -> AssistantResponse:
    return assistant.answer(request)


@app.get("/protocols", response_model=list[dict])
def list_protocols(category: str | None = None) -> list[dict]:
    _log_endpoint_access("/protocols", "protocolos", "consulta_protocolo")
    documents = protocol_repository.list_protocols(category=category)
    return [
        {
            "doc_id": item.doc_id,
            "title": item.title,
            "category": item.category,
            "specialty": item.specialty,
            "document_type": item.document_type,
            "source": item.source,
            "keywords": item.keywords,
            "safety_tags": item.safety_tags,
            "representativity_tags": item.representativity_tags,
        }
        for item in documents
    ]


@app.get("/protocols/{doc_id}", response_model=dict)
def get_protocol(doc_id: str) -> dict:
    _log_endpoint_access("/protocols/{doc_id}", "protocolos", "consulta_documento_especializado")
    document = protocol_repository.get_protocol(doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Protocol not found")
    return document.model_dump()


@app.get("/auditoria/relatorio-especialidade", response_model=dict)
def specialty_access_report() -> dict:
    _log_endpoint_access("/auditoria/relatorio-especialidade", "auditoria", "relatorio_monitoramento")
    return access_monitor.generate_specialty_report()


@app.post("/flows/triage", response_model=FlowResult)
def triage_flow(payload: TriageInput) -> FlowResult:
    _log_endpoint_access("/flows/triage", "ginecologia", "execucao_fluxo")
    return run_triage_flow(payload)


@app.post("/fluxo/triagem-ginecologica", response_model=FlowResult)
def triagem_ginecologica(payload: TriageInput) -> FlowResult:
    _log_endpoint_access("/fluxo/triagem-ginecologica", "ginecologia", "execucao_fluxo")
    return run_triage_flow(payload)


@app.post("/flows/obstetric", response_model=FlowResult)
def obstetric_flow(payload: ObstetricInput) -> FlowResult:
    _log_endpoint_access("/flows/obstetric", "obstetricia", "execucao_fluxo")
    return run_obstetric_flow(payload)


@app.post("/fluxo/obstetrico", response_model=FlowResult)
def fluxo_obstetrico(payload: ObstetricInput) -> FlowResult:
    _log_endpoint_access("/fluxo/obstetrico", "obstetricia", "execucao_fluxo")
    return run_obstetric_flow(payload)


@app.post("/flows/prevention", response_model=FlowResult)
def prevention_flow(payload: PreventionInput) -> FlowResult:
    _log_endpoint_access("/flows/prevention", "prevencao", "execucao_fluxo")
    return run_prevention_flow(payload)


@app.post("/fluxo/prevencao", response_model=FlowResult)
def fluxo_prevencao(payload: PreventionInput) -> FlowResult:
    _log_endpoint_access("/fluxo/prevencao", "prevencao", "execucao_fluxo")
    return run_prevention_flow(payload)


@app.post("/flows/violence", response_model=FlowResult)
def violence_flow(payload: ViolenceInput) -> FlowResult:
    _log_endpoint_access("/flows/violence", "protecao_social", "execucao_fluxo")
    return run_violence_flow(payload)


@app.post("/fluxo/violencia-domestica", response_model=FlowResult)
def fluxo_violencia_domestica(payload: ViolenceInput) -> FlowResult:
    _log_endpoint_access("/fluxo/violencia-domestica", "protecao_social", "execucao_fluxo")
    return run_violence_flow(payload)
