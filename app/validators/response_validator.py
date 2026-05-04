from __future__ import annotations

from app.domain.models import AssistantResponse


BLOCKED_PATTERNS = {
    "prescrevo",
    "tome",
    "inicie o medicamento",
    "diagnóstico definitivo",
    "isso é certamente",
}


def validate_response(response: AssistantResponse) -> AssistantResponse:
    combined = " ".join(
        [
            response.summary.lower(),
            response.justification.lower(),
            response.referral.lower(),
        ]
    )
    red_flags = list(response.red_flags)

    if any(pattern in combined for pattern in BLOCKED_PATTERNS):
        response.safe = False
        red_flags.append("unsafe_medical_guidance")

    if response.risk_level in {"high", "critical"} and "presencial" not in response.referral.lower():
        response.safe = False
        red_flags.append("missing_in_person_referral")

    if "violência" in combined and "equipe qualificada" not in response.referral.lower():
        response.safe = False
        red_flags.append("missing_specialized_violence_referral")

    response.red_flags = red_flags
    return response


def build_refusal(reason: str) -> AssistantResponse:
    return AssistantResponse(
        summary="Não posso atender a essa solicitação com segurança.",
        justification=reason,
        source="Política de Segurança Assistencial Acadêmica",
        confidence="high",
        limits="O assistente não realiza prescrição, diagnóstico definitivo nem orientação que aumente risco clínico ou social.",
        data_needs="A solicitação deve ser revista por profissional habilitado com avaliação clínica presencial e dados complementares.",
        referral="Procure atendimento presencial com profissional habilitado ou serviço de urgência, conforme a gravidade.",
        risk_level="high",
        professional_validation_required=True,
        safe=False,
        red_flags=["request_blocked"],
    )
