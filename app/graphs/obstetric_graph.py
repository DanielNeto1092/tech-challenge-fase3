from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.domain.models import FlowResult, ObstetricInput
from app.graphs.state import FlowState
from app.security.audit import AuditLogger
from app.security.risk import classify_risk
from app.services.protocol_context_service import ProtocolContextService


def _evaluate_gestational_risk(state: FlowState) -> FlowState:
    payload = ObstetricInput.model_validate(state["input"])
    texts = payload.sintomas + payload.comorbidades + [payload.contexto]
    if payload.idade_gestacional_semanas >= 28:
        texts.append("terceiro trimestre")
    risk = classify_risk(texts)
    service = ProtocolContextService.build()
    protocols = service.find_relevant(
        " ".join(texts),
        specialties={"obstetricia", "saude_da_mulher"},
        categories={"obstetricia", "amamentacao", "womens_health_qa"},
    )
    return {
        **state,
        "risk_level": risk,
        "protocol_contexts": service.summarize_sources(protocols),
    }


def _recommend_orientation(state: FlowState) -> FlowState:
    urgency_map = {
        "critical": "emergency",
        "high": "urgent",
        "moderate": "priority",
        "low": "routine",
    }
    return {
        **state,
        "urgency": urgency_map[state["risk_level"]],
        "recommended_actions": [
            "Monitorar piora clínica e não aguardar sintomas alarmantes em casa.",
            "Levar cartão pré-natal e lista de sintomas para avaliação.",
        ],
    }


def _recommend_exams(state: FlowState) -> FlowState:
    exams = ["aferição de pressão arterial", "avaliação obstétrica presencial"]
    if state["urgency"] in {"urgent", "emergency"}:
        exams.extend(["cardiotocografia ou avaliação de vitalidade fetal", "proteinúria conforme protocolo local"])
    if state.get("protocol_contexts"):
        exams.append("conferir alinhamento com diretriz obstétrica sintética recuperada")
    return {**state, "suggested_exams": exams}


def _finalize(state: FlowState) -> FlowState:
    urgent = state["urgency"] in {"urgent", "emergency"}
    return {
        **state,
        "summary": "Fluxo obstétrico aponta necessidade de avaliação clínica presencial com foco em segurança materno-fetal.",
        "escalation": (
            "Encaminhar imediatamente para maternidade, pronto atendimento obstétrico ou equipe de referência."
            if urgent
            else "Agendar retorno obstétrico prioritário."
        ),
        "notes": ["O assistente não substitui pré-natal nem avaliação de urgência."] + state.get("protocol_contexts", []),
    }


def build_obstetric_graph():
    graph = StateGraph(FlowState)
    graph.add_node("evaluate_gestational_risk", _evaluate_gestational_risk)
    graph.add_node("recommend_orientation", _recommend_orientation)
    graph.add_node("recommend_exams", _recommend_exams)
    graph.add_node("finalize", _finalize)
    graph.add_edge(START, "evaluate_gestational_risk")
    graph.add_edge("evaluate_gestational_risk", "recommend_orientation")
    graph.add_edge("recommend_orientation", "recommend_exams")
    graph.add_edge("recommend_exams", "finalize")
    graph.add_edge("finalize", END)
    return graph.compile()


def run_obstetric_flow(flow_input: ObstetricInput) -> FlowResult:
    compiled = build_obstetric_graph()
    logger = AuditLogger()
    state = compiled.invoke({"input": flow_input.model_dump()})
    audit_id = logger.log_event("obstetric_flow", flow_input.model_dump())
    return FlowResult(
        flow_name="fluxo_obstetrico",
        summary=state["summary"],
        urgency=state["urgency"],
        recommended_actions=state["recommended_actions"],
        suggested_exams=state["suggested_exams"],
        escalation=state["escalation"],
        notes=state["notes"],
        audit_id=audit_id,
    )
