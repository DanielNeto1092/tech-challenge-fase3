from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.domain.models import FlowResult, ViolenceInput
from app.graphs.state import FlowState
from app.security.audit import AuditLogger
from app.security.risk import classify_risk
from app.services.protocol_context_service import ProtocolContextService


def _evaluate_risk(state: FlowState) -> FlowState:
    payload = ViolenceInput.model_validate(state["input"])
    texts = payload.sinais_alerta + [payload.contexto]
    if payload.risco_imediato:
        texts.append("risco imediato")
    risk = classify_risk(texts)
    service = ProtocolContextService.build()
    protocols = service.find_relevant(
        " ".join(texts),
        specialties={"protecao_social"},
        categories={"violencia_domestica"},
    )
    return {
        **state,
        "risk_level": risk,
        "protocol_contexts": service.summarize_sources(protocols),
    }


def _build_safety_protocol(state: FlowState) -> FlowState:
    emergency = state["risk_level"] == "critical"
    return {
        **state,
        "urgency": "emergency" if emergency else "urgent",
        "recommended_actions": [
            "Validar o relato sem culpabilizar a paciente.",
            "Priorizar comunicação segura e discreta.",
            "Evitar registros que aumentem risco de exposição indevida.",
        ],
        "notes": [
            "Manter confidencialidade e acesso mínimo aos dados.",
            "Nunca minimizar suspeita de violência doméstica.",
        ] + state.get("protocol_contexts", []),
    }


def _escalate_support(state: FlowState) -> FlowState:
    escalation = (
        "Acionar equipe especializada, serviço social, rede de proteção e emergência imediatamente."
        if state["urgency"] == "emergency"
        else "Encaminhar para equipe qualificada em violência doméstica e construir plano seguro de seguimento."
    )
    return {
        **state,
        "summary": "Sinais compatíveis com possível violência doméstica; a prioridade é segurança, acolhimento e encaminhamento especializado.",
        "escalation": escalation,
        "suggested_exams": [],
    }


def build_violence_graph():
    graph = StateGraph(FlowState)
    graph.add_node("evaluate_risk", _evaluate_risk)
    graph.add_node("build_safety_protocol", _build_safety_protocol)
    graph.add_node("escalate_support", _escalate_support)
    graph.add_edge(START, "evaluate_risk")
    graph.add_edge("evaluate_risk", "build_safety_protocol")
    graph.add_edge("build_safety_protocol", "escalate_support")
    graph.add_edge("escalate_support", END)
    return graph.compile()


def run_violence_flow(flow_input: ViolenceInput) -> FlowResult:
    compiled = build_violence_graph()
    logger = AuditLogger()
    state = compiled.invoke({"input": flow_input.model_dump()})
    audit_id = logger.log_event("violence_flow", flow_input.model_dump())
    return FlowResult(
        flow_name="violencia_domestica",
        summary=state["summary"],
        urgency=state["urgency"],
        recommended_actions=state["recommended_actions"],
        suggested_exams=state["suggested_exams"],
        escalation=state["escalation"],
        notes=state["notes"],
        audit_id=audit_id,
    )
