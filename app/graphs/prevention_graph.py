from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.domain.models import FlowResult, PreventionInput
from app.graphs.state import FlowState
from app.security.audit import AuditLogger


def _identify_gaps(state: FlowState) -> FlowState:
    payload = PreventionInput.model_validate(state["input"])
    exams = []
    history_blob = " ".join(payload.historico).lower()
    previous_exams = " ".join(payload.exames_realizados).lower()

    if payload.idade >= 25 and "papanicolau" not in previous_exams:
        exams.append("Atualizar rastreamento de colo do útero conforme diretriz local")
    if payload.idade >= 40:
        exams.append("Verificar indicação de mamografia conforme faixa etária e risco")
    if "câncer de mama" in history_blob or "cancer de mama" in history_blob:
        exams.append("Revisar histórico familiar em consulta para individualizar rastreamento")

    return {
        **state,
        "suggested_exams": exams,
        "risk_level": "low",
    }


def _build_prevention_guidance(state: FlowState) -> FlowState:
    actions = [
        "Conferir exames preventivos pendentes com a unidade de saúde.",
        "Registrar datas prévias para acompanhamento longitudinal.",
        "Buscar avaliação antes do prazo regular se surgir sintoma novo.",
    ]
    return {
        **state,
        "urgency": "routine" if len(state["suggested_exams"]) <= 1 else "priority",
        "recommended_actions": actions,
        "summary": "Fluxo preventivo identificou oportunidades de rastreamento e organização do cuidado.",
        "escalation": "Sugerir agendamento preventivo com atenção primária ou ginecologia.",
        "notes": ["Rastreamento deve seguir diretrizes institucionais e avaliação individual."],
    }


def build_prevention_graph():
    graph = StateGraph(FlowState)
    graph.add_node("identify_gaps", _identify_gaps)
    graph.add_node("build_prevention_guidance", _build_prevention_guidance)
    graph.add_edge(START, "identify_gaps")
    graph.add_edge("identify_gaps", "build_prevention_guidance")
    graph.add_edge("build_prevention_guidance", END)
    return graph.compile()


def run_prevention_flow(flow_input: PreventionInput) -> FlowResult:
    compiled = build_prevention_graph()
    logger = AuditLogger()
    state = compiled.invoke({"input": flow_input.model_dump()})
    audit_id = logger.log_event("prevention_flow", flow_input.model_dump())
    return FlowResult(
        flow_name="fluxo_prevencao",
        summary=state["summary"],
        urgency=state["urgency"],
        recommended_actions=state["recommended_actions"],
        suggested_exams=state["suggested_exams"],
        escalation=state["escalation"],
        notes=state["notes"],
        audit_id=audit_id,
    )
