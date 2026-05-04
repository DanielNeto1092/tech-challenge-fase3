from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.domain.models import FlowResult, TriageInput
from app.graphs.state import FlowState
from app.security.audit import AuditLogger
from app.security.risk import classify_risk
from app.services.protocol_context_service import ProtocolContextService


def _analyze_risk(state: FlowState) -> FlowState:
    payload = TriageInput.model_validate(state["input"])
    risk = classify_risk(payload.sintomas + [payload.contexto])
    service = ProtocolContextService.build()
    protocols = service.find_relevant(
        " ".join(payload.sintomas + [payload.contexto]),
        specialties={"ginecologia", "saude_da_mulher"},
        categories={"sintomas_ginecologicos", "womens_health_qa", "saude_menstrual"},
    )
    return {
        **state,
        "risk_level": risk,
        "notes": ["Triagem sintética focada em segurança e encaminhamento."],
        "protocol_contexts": service.summarize_sources(protocols),
    }


def _classify_urgency(state: FlowState) -> FlowState:
    urgency_map = {
        "critical": "emergency",
        "high": "urgent",
        "moderate": "priority",
        "low": "routine",
    }
    return {
        **state,
        "urgency": urgency_map[state["risk_level"]],
    }


def _suggest_exams(state: FlowState) -> FlowState:
    exams = ["exame ginecológico presencial"]
    if state["risk_level"] in {"high", "critical"}:
        exams.extend(["hemograma", "ultrassom pélvico", "avaliação de infecção conforme protocolo local"])
    if state.get("protocol_contexts"):
        exams.append("correlacionar achados com protocolo sintético recuperado")
    return {**state, "suggested_exams": exams}


def _build_guidance(state: FlowState) -> FlowState:
    urgent = state["urgency"] in {"urgent", "emergency"}
    actions = [
        "Não automedicar e não retardar avaliação clínica.",
        "Levar histórico de início, duração e intensidade dos sintomas.",
    ]
    escalation = (
        "Encaminhar imediatamente para atendimento presencial em pronto atendimento ginecológico."
        if urgent
        else "Agendar consulta ginecológica prioritária com avaliação presencial."
    )
    summary = (
        "Sintomas ginecológicos com potencial sinal de alerta e necessidade de avaliação presencial rápida."
        if urgent
        else "Quadro requer avaliação ambulatorial prioritária e monitoramento de piora."
    )
    return {
        **state,
        "summary": summary,
        "recommended_actions": actions,
        "escalation": escalation,
        "notes": state.get("notes", []) + state.get("protocol_contexts", []),
    }


def build_triage_graph():
    graph = StateGraph(FlowState)
    graph.add_node("analyze_risk", _analyze_risk)
    graph.add_node("classify_urgency", _classify_urgency)
    graph.add_node("suggest_exams", _suggest_exams)
    graph.add_node("build_guidance", _build_guidance)
    graph.add_edge(START, "analyze_risk")
    graph.add_edge("analyze_risk", "classify_urgency")
    graph.add_edge("classify_urgency", "suggest_exams")
    graph.add_edge("suggest_exams", "build_guidance")
    graph.add_edge("build_guidance", END)
    return graph.compile()


def run_triage_flow(flow_input: TriageInput) -> FlowResult:
    compiled = build_triage_graph()
    logger = AuditLogger()
    state = compiled.invoke({"input": flow_input.model_dump()})
    audit_id = logger.log_event("triage_flow", flow_input.model_dump())
    return FlowResult(
        flow_name="triagem_ginecologica",
        summary=state["summary"],
        urgency=state["urgency"],
        recommended_actions=state["recommended_actions"],
        suggested_exams=state["suggested_exams"],
        escalation=state["escalation"],
        notes=state["notes"],
        audit_id=audit_id,
    )
