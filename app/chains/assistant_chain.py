from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from app.domain.models import AssistantRequest, AssistantResponse, RetrievedContext
from app.security.risk import classify_risk
from app.validators.response_validator import build_refusal, validate_response


def build_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Você responde com segurança clínica, contextualização, fonte e encaminhamento. Nunca prescreva medicamentos.",
            ),
            (
                "human",
                "Pergunta: {question}\nContexto anonimo: {context}\nTrechos recuperados: {retrieved}",
            ),
        ]
    )


def _is_blocked_request(question: str) -> bool:
    lowered = question.lower()
    return any(
        phrase in lowered
        for phrase in [
            "qual remédio",
            "qual remedio",
            "dose exata",
            "prescreva",
            "diagnóstico definitivo",
            "diagnostico definitivo",
        ]
    )


def _compose_response(payload: dict) -> AssistantResponse:
    request: AssistantRequest = payload["request"]
    contexts: list[RetrievedContext] = payload["contexts"]
    risk_level = classify_risk(
        [request.question, *[ctx.document.content for ctx in contexts]]
    )

    if _is_blocked_request(request.question):
        return build_refusal(
            "A solicitação pede prescrição ou definição diagnóstica, o que está fora do escopo seguro."
        )

    if not contexts:
        response = AssistantResponse(
            summary="Não encontrei base local suficiente para orientar com segurança além de recomendações gerais.",
            justification="A pergunta não teve correspondência forte na base sintética, então a resposta deve ser limitada.",
            source="Base Sintética Local - sem correspondência relevante",
            confidence="low",
            limits="A resposta é restrita por falta de contexto validado e não substitui avaliação presencial.",
            data_needs="São necessários dados clínicos adicionais, exame físico, histórico dirigido e revisão por profissional habilitado.",
            referral="Busque orientação de profissional habilitado, especialmente se houver piora, dor intensa, sangramento ou outros sinais de alarme.",
            risk_level=risk_level,
        )
        return validate_response(response)

    top_source = contexts[0].document
    response = AssistantResponse(
        summary=(
            f"Orientação inicial baseada em {top_source.category.replace('_', ' ')}: "
            f"{top_source.content.split('.')[0].strip()}."
        ),
        justification=(
            "A resposta foi construída a partir dos trechos sintéticos recuperados e prioriza segurança, "
            "triagem e necessidade de avaliação humana quando existem sinais de alerta."
        ),
        source=f"{top_source.source} ({top_source.title})",
        confidence="high" if contexts[0].score >= 4 else "medium",
        limits="Ferramenta acadêmica de apoio. Não confirma diagnóstico, não prescreve e pode não cobrir todo o quadro clínico.",
        data_needs=(
            "Confirmar achados com anamnese detalhada, exame físico, exames complementares e protocolo institucional atualizado."
        ),
        referral=(
            "Procure atendimento presencial com profissional habilitado. "
            "Se houver sintomas alarmantes, priorize serviço de urgência."
            if risk_level in {"high", "critical"}
            else "Agende avaliação com profissional habilitado para confirmação clínica e conduta individualizada."
        ),
        risk_level=risk_level,
    )
    return validate_response(response)


def build_assistant_chain():
    prompt = build_prompt_template()
    return RunnablePassthrough.assign(prompt_value=prompt) | RunnableLambda(_compose_response)
