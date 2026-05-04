from __future__ import annotations

import json

import streamlit as st

from app.assistant import WomensHealthAssistant
from app.graphs.obstetric_graph import run_obstetric_flow
from app.graphs.prevention_graph import run_prevention_flow
from app.graphs.triage_graph import run_triage_flow
from app.graphs.violence_graph import run_violence_flow
from app.models import AssistantRequest, ObstetricInput, PreventionInput, TriageInput, ViolenceInput
from app.protocols import ProtocolRepository
from app.security.access_monitor import AccessMonitor


assistant = WomensHealthAssistant()
protocol_repository = ProtocolRepository()
access_monitor = AccessMonitor()


st.set_page_config(
    page_title="Assistente Saúde da Mulher",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #fdf3e7 0%, #f9d8c4 45%, #f2b6a0 100%);
        padding: 1.5rem 1.6rem;
        border-radius: 20px;
        color: #402218;
        border: 1px solid rgba(64,34,24,.08);
        box-shadow: 0 18px 40px rgba(64,34,24,.08);
        margin-bottom: 1rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 2rem;
    }
    .hero p {
        margin: .35rem 0 0 0;
        font-size: 1rem;
    }
    .kpi {
        background: linear-gradient(180deg, #fffdf9 0%, #fff6ef 100%);
        border: 1px solid rgba(64,34,24,.08);
        border-radius: 18px;
        padding: 1rem 1rem .8rem 1rem;
        box-shadow: 0 10px 24px rgba(64,34,24,.06);
    }
    .kpi h3 {
        margin: 0;
        font-size: .9rem;
        color: #7d5a50;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .04em;
    }
    .kpi p {
        margin: .3rem 0 0 0;
        font-size: 1.7rem;
        font-weight: 700;
        color: #402218;
    }
    .card {
        background: #fffaf5;
        border: 1px solid rgba(64,34,24,.08);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: .8rem;
    }
    .pill {
        display: inline-block;
        padding: .2rem .6rem;
        border-radius: 999px;
        font-size: .85rem;
        font-weight: 600;
        margin-right: .4rem;
        color: white;
    }
    .risk-low { background: #3a7d44; }
    .risk-moderate { background: #b7791f; }
    .risk-high { background: #c05621; }
    .risk-critical { background: #c53030; }
    .muted { color: #6b5248; font-size: .92rem; }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: .8rem;
        margin-top: .6rem;
    }
    .feature {
        background: #fffaf5;
        border: 1px solid rgba(64,34,24,.08);
        border-radius: 16px;
        padding: .9rem 1rem;
    }
    .feature strong {
        color: #402218;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


EXAMPLE_CASES = {
    "Saúde mental no pós-parto": {
        "question": "Estou no pós-parto e sinto tristeza persistente e dificuldade para dormir. O que observar?",
        "context": {"postpartum_days": 21},
        "specialty": "saude_da_mulher",
    },
    "Violência doméstica": {
        "question": "Quais sinais exigem encaminhamento seguro em possível violência doméstica?",
        "context": {"observacao": "Parceiro monitora celular e há medo relatado"},
        "specialty": "protecao_social",
    },
    "Prevenção mamográfica": {
        "question": "Como orientar exames preventivos para mulher de 47 anos com histórico familiar de câncer de mama?",
        "context": {"idade": 47, "historico_familiar": True},
        "specialty": "ginecologia",
    },
}

RISK_LABELS = {
    "low": "baixo",
    "moderate": "moderado",
    "high": "alto",
    "critical": "crítico",
}

URGENCY_LABELS = {
    "routine": "rotina",
    "priority": "prioridade",
    "urgent": "urgente",
    "emergency": "emergência",
}

CONFIDENCE_LABELS = {
    "low": "baixa",
    "medium": "média",
    "high": "alta",
}

RED_FLAG_LABELS = {
    "request_blocked": "solicitação bloqueada por segurança",
    "unsafe_medication_guidance": "orientação medicamentosa insegura",
    "missing_in_person_referral": "faltou encaminhamento presencial",
    "missing_source": "faltou fonte de referência",
}


def init_state() -> None:
    if "history" not in st.session_state:
        st.session_state.history = []


def push_history(entry_type: str, payload: dict) -> None:
    st.session_state.history.insert(0, {"type": entry_type, "payload": payload})
    st.session_state.history = st.session_state.history[:12]


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Assistente Virtual Médico</h1>
            <p>Saúde e segurança da mulher • apoio acadêmico • LangChain • LangGraph • guardrails clínicos</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis() -> None:
    docs = protocol_repository.documents
    report = access_monitor.generate_specialty_report()
    total_accesses = sum(item.get("total_accesses", 0) for item in report.values())
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="kpi"><h3>Protocolos</h3><p>{}</p></div>'.format(len(docs)), unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<div class="kpi"><h3>Categorias</h3><p>{}</p></div>'.format(len({doc.category for doc in docs})),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="kpi"><h3>Especialidades</h3><p>{}</p></div>'.format(len({doc.specialty for doc in docs})),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown('<div class="kpi"><h3>Acessos</h3><p>{}</p></div>'.format(total_accesses), unsafe_allow_html=True)


def overview_tab() -> None:
    st.subheader("Visão geral da plataforma")
    render_kpis()
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature"><strong>Assistente clínico</strong><br/>Resposta contextualizada com fonte, risco, limites e necessidade de validação profissional.</div>
            <div class="feature"><strong>Fluxos LangGraph</strong><br/>Triagem ginecológica, obstetrícia, prevenção e violência doméstica com passos explícitos.</div>
            <div class="feature"><strong>Segurança aplicada</strong><br/>Anonimização, identidade simulada, criptografia simulada, auditoria e monitoramento de acesso.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Casos rápidos")
    quick_cols = st.columns(len(EXAMPLE_CASES))
    for col, (label, payload) in zip(quick_cols, EXAMPLE_CASES.items()):
        with col:
            if st.button(label, use_container_width=True):
                response = assistant.answer(
                    AssistantRequest(
                        question=payload["question"],
                        patient_context=payload["context"],
                        specialty=payload["specialty"],
                        requester_id="demo_clinician",
                    )
                )
                push_history("assistente", response.model_dump())
                st.session_state["last_quick_result"] = response.model_dump()
    if "last_quick_result" in st.session_state:
        render_assistant_response(st.session_state["last_quick_result"])


def risk_badge(risk: str) -> str:
    css = {
        "low": "risk-low",
        "moderate": "risk-moderate",
        "high": "risk-high",
        "critical": "risk-critical",
    }.get(risk, "risk-moderate")
    return f'<span class="pill {css}">Risco: {RISK_LABELS.get(risk, risk)}</span>'


def urgency_badge(urgency: str) -> str:
    css = {
        "routine": "risk-low",
        "priority": "risk-moderate",
        "urgent": "risk-high",
        "emergency": "risk-critical",
    }.get(urgency, "risk-moderate")
    return f'<span class="pill {css}">Urgência: {URGENCY_LABELS.get(urgency, urgency)}</span>'


def render_assistant_response(payload: dict) -> None:
    st.markdown(
        f"""
        <div class="card">
            {risk_badge(payload["risk_level"])}
            <p><strong>Resumo:</strong> {payload["summary"]}</p>
            <p><strong>Justificativa:</strong> {payload["justification"]}</p>
            <p><strong>Fonte:</strong> {payload["source"]}</p>
            <p><strong>Confiança:</strong> {CONFIDENCE_LABELS.get(payload["confidence"], payload["confidence"])}</p>
            <p><strong>Limites:</strong> {payload["limits"]}</p>
            <p><strong>Dados adicionais necessários:</strong> {payload["data_needs"]}</p>
            <p><strong>Encaminhamento:</strong> {payload["referral"]}</p>
            <p><strong>Validação profissional obrigatória:</strong> {"Sim" if payload["professional_validation_required"] else "Não"}</p>
            <p><strong>Resposta segura:</strong> {"Sim" if payload["safe"] else "Não"}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if payload["red_flags"]:
        st.warning(
            "Alertas de segurança: "
            + ", ".join(RED_FLAG_LABELS.get(flag, flag) for flag in payload["red_flags"])
        )


def render_flow_result(result) -> None:
    data = result.model_dump()
    st.markdown(
        f"""
        <div class="card">
            {urgency_badge(data["urgency"])}
            <p><strong>Resumo:</strong> {data["summary"]}</p>
            <p><strong>Escalonamento:</strong> {data["escalation"]}</p>
            <p><strong>ID de auditoria:</strong> {data["audit_id"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Ações recomendadas**")
        for action in data["recommended_actions"]:
            st.write(f"- {action}")
    with col2:
        st.markdown("**Exames sugeridos**")
        if data["suggested_exams"]:
            for exam in data["suggested_exams"]:
                st.write(f"- {exam}")
        else:
            st.write("- Não se aplica")
    if data["notes"]:
        st.info(" | ".join(data["notes"]))


def assistant_tab() -> None:
    st.subheader("Pergunta clínica contextualizada")
    example = st.selectbox("Carregar exemplo rápido", ["Nenhum"] + list(EXAMPLE_CASES.keys()))
    default_question = ""
    default_context = '{"nome":"Paciente Exemplo"}'
    default_specialty = "saude_da_mulher"
    if example != "Nenhum":
        selected = EXAMPLE_CASES[example]
        default_question = selected["question"]
        default_context = json.dumps(selected["context"], ensure_ascii=False)
        default_specialty = selected["specialty"]
    with st.form("assistant_form"):
        question = st.text_area(
            "Pergunta",
            value=default_question,
            placeholder="Ex.: Tenho sangramento no pós-parto e febre. O que fazer?",
        )
        context_text = st.text_area("Contexto do caso (JSON opcional)", value=default_context)
        requester_id = st.selectbox("Solicitante", ["demo_clinician", "demo_gineco", "demo_obstetrica", "usuario_externo"])
        requester_role = st.selectbox("Perfil", ["profissional_saude", "ginecologista", "obstetra", "assistente_social"])
        specialty = st.selectbox(
            "Especialidade",
            ["saude_da_mulher", "ginecologia", "obstetricia", "protecao_social"],
            index=["saude_da_mulher", "ginecologia", "obstetricia", "protecao_social"].index(default_specialty),
        )
        access_reason = st.text_input("Motivo de acesso", value="apoio_clinico_academico")
        auth_token = st.text_input("Token de acesso (opcional)", type="password")
        submitted = st.form_submit_button("Gerar orientação")

    if submitted and question.strip():
        try:
            context = json.loads(context_text) if context_text.strip() else {}
        except json.JSONDecodeError:
            st.error("O contexto precisa ser um JSON válido.")
            return

        response = assistant.answer(
            AssistantRequest(
                question=question,
                patient_context=context,
                requester_id=requester_id,
                requester_role=requester_role,
                specialty=specialty,
                access_reason=access_reason,
                auth_token=auth_token or None,
            )
        )
        response_payload = response.model_dump()
        push_history("assistente", response_payload)
        render_assistant_response(response_payload)


def triage_tab() -> None:
    st.subheader("Fluxo de triagem ginecológica")
    sintomas = st.text_area("Sintomas", placeholder="Um por linha", key="triage_symptoms")
    contexto = st.text_area("Contexto", key="triage_context")
    idade = st.number_input("Idade", min_value=10, max_value=100, value=29, key="triage_age")
    gestante = st.checkbox("Gestante", key="triage_pregnant")
    if st.button("Executar triagem ginecológica"):
        result = run_triage_flow(
            TriageInput(
                sintomas=[item.strip() for item in sintomas.splitlines() if item.strip()],
                contexto=contexto,
                idade=int(idade),
                gestante=gestante,
            )
        )
        push_history("triagem", result.model_dump())
        render_flow_result(result)


def violence_tab() -> None:
    st.subheader("Fluxo de violência doméstica")
    sinais = st.text_area("Sinais de alerta", placeholder="Um por linha", key="violence_signs")
    contexto = st.text_area("Contexto de segurança", key="violence_context")
    risco_imediato = st.checkbox("Risco imediato", key="violence_immediate")
    if st.button("Executar fluxo de violência doméstica"):
        result = run_violence_flow(
            ViolenceInput(
                sinais_alerta=[item.strip() for item in sinais.splitlines() if item.strip()],
                contexto=contexto,
                risco_imediato=risco_imediato,
            )
        )
        push_history("violencia", result.model_dump())
        render_flow_result(result)


def obstetric_tab() -> None:
    st.subheader("Fluxo obstétrico")
    semanas = st.number_input("Idade gestacional (semanas)", min_value=1, max_value=42, value=30)
    sintomas = st.text_area("Sintomas obstétricos", placeholder="Um por linha", key="ob_symptoms")
    comorbidades = st.text_area("Comorbidades", placeholder="Uma por linha", key="ob_comorbidities")
    contexto = st.text_area("Contexto obstétrico", key="ob_context")
    if st.button("Executar fluxo obstétrico"):
        result = run_obstetric_flow(
            ObstetricInput(
                idade_gestacional_semanas=int(semanas),
                sintomas=[item.strip() for item in sintomas.splitlines() if item.strip()],
                comorbidades=[item.strip() for item in comorbidades.splitlines() if item.strip()],
                contexto=contexto,
            )
        )
        push_history("obstetrico", result.model_dump())
        render_flow_result(result)


def prevention_tab() -> None:
    st.subheader("Fluxo preventivo")
    idade = st.number_input("Idade", min_value=10, max_value=100, value=45, key="prev_age")
    historico = st.text_area("Histórico relevante", placeholder="Um por linha", key="prev_history")
    exames = st.text_area("Exames já realizados", placeholder="Um por linha", key="prev_exams")
    contexto = st.text_area("Observações", key="prev_context")
    if st.button("Executar fluxo de prevenção"):
        result = run_prevention_flow(
            PreventionInput(
                idade=int(idade),
                historico=[item.strip() for item in historico.splitlines() if item.strip()],
                exames_realizados=[item.strip() for item in exames.splitlines() if item.strip()],
                contexto=contexto,
            )
        )
        push_history("prevencao", result.model_dump())
        render_flow_result(result)


def protocols_tab() -> None:
    st.subheader("Protocolos e datasets sintéticos")
    category = st.selectbox(
        "Filtrar por categoria",
        ["todas"] + sorted({doc.category for doc in protocol_repository.documents}),
    )
    docs = protocol_repository.list_protocols(None if category == "todas" else category)
    for doc in docs:
        with st.expander(f"{doc.title} · {doc.specialty} · {doc.document_type}"):
            st.write(doc.content)
            st.caption(f"Fonte: {doc.source}")
            st.write("Palavras-chave:", ", ".join(doc.keywords))
            st.write("Etiquetas de segurança:", ", ".join(doc.safety_tags))
            st.write("Representatividade:", ", ".join(doc.representativity_tags))


def audit_tab() -> None:
    st.subheader("Auditoria e monitoramento")
    report = access_monitor.generate_specialty_report()
    if not report:
        st.info("Ainda não há acessos registrados nesta sessão.")
        return
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.json(report)
    with col2:
        st.markdown("### Histórico da sessão")
        if not st.session_state.history:
            st.caption("Sem interações registradas nesta sessão.")
        for idx, item in enumerate(st.session_state.history, start=1):
            with st.expander(f"{idx}. {item['type'].title()}"):
                st.json(item["payload"])


def sidebar_content() -> None:
    st.sidebar.title("Painel")
    st.sidebar.markdown("Ferramenta acadêmica de apoio. Não substitui profissionais de saúde.")
    st.sidebar.markdown("**Acesso demo**")
    st.sidebar.code(
        "requester_id: demo_clinician\n"
        "requester_id: demo_gineco\n"
        "requester_id: demo_obstetrica",
        language="text",
    )
    st.sidebar.markdown("**Módulos visuais**")
    st.sidebar.write("- Assistente com explainability")
    st.sidebar.write("- 4 fluxos LangGraph")
    st.sidebar.write("- Protocolos sintéticos")
    st.sidebar.write("- Auditoria agregada")
    st.sidebar.markdown('<p class="muted">Tokens são opcionais para IDs demo pré-configurados.</p>', unsafe_allow_html=True)


def main() -> None:
    init_state()
    render_header()
    sidebar_content()

    tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Visão Geral",
            "Assistente",
            "Triagem Ginecológica",
            "Violência Doméstica",
            "Obstétrico",
            "Prevenção",
            "Protocolos",
            "Auditoria",
        ]
    )

    with tab0:
        overview_tab()
    with tab1:
        assistant_tab()
    with tab2:
        triage_tab()
    with tab3:
        violence_tab()
    with tab4:
        obstetric_tab()
    with tab5:
        prevention_tab()
    with tab6:
        protocols_tab()
    with tab7:
        audit_tab()


if __name__ == "__main__":
    main()
