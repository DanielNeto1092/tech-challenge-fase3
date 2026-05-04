from app.models import AssistantResponse
from app.validators.response_validator import build_refusal, validate_response


def test_validate_unsafe_response() -> None:
    response = AssistantResponse(
        summary="Tome antibiotico agora.",
        justification="Isso e certamente uma infeccao.",
        source="fonte",
        confidence="medium",
        limits="limites",
        data_needs="Revisao presencial.",
        referral="Acompanhe em casa.",
        risk_level="high",
    )
    validated = validate_response(response)
    assert validated.safe is False
    assert "missing_in_person_referral" in validated.red_flags


def test_build_refusal() -> None:
    refusal = build_refusal("Pedido de prescricao.")
    assert refusal.safe is False
    assert refusal.risk_level == "high"
