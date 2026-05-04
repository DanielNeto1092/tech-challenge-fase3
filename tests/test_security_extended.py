import json
from pathlib import Path

from app.assistant import WomensHealthAssistant
from app.config import ACCESS_LOG_FILE
from app.main import specialty_access_report
from app.models import AssistantRequest
from app.security.crypto import encrypt_text
from app.security.identity import IdentityVerifier


def test_identity_verifier_rejects_invalid_token() -> None:
    verifier = IdentityVerifier()
    try:
        verifier.verify("demo_gineco", "token-invalido")
    except ValueError:
        assert True
        return
    assert False, "Era esperado erro para token inválido"


def test_crypto_simulation_returns_non_plaintext() -> None:
    encrypted = encrypt_text("paciente-demo")
    assert encrypted != "paciente-demo"


def test_access_report_is_generated() -> None:
    assistant = WomensHealthAssistant()
    assistant.answer(AssistantRequest(question="Como funciona o rastreio mamográfico?", patient_context={}))
    report = specialty_access_report()
    assert isinstance(report, dict)


def test_invalid_identity_blocks_assistant_request() -> None:
    assistant = WomensHealthAssistant()
    response = assistant.answer(
        AssistantRequest(
            question="Tenho febre no pos-parto",
            patient_context={},
            requester_id="usuario_externo",
            auth_token=None,
        )
    )
    assert response.safe is False
    assert "identidade" in response.justification.lower()


def test_access_log_written() -> None:
    if Path(ACCESS_LOG_FILE).exists():
        lines_before = Path(ACCESS_LOG_FILE).read_text(encoding="utf-8").splitlines()
    else:
        lines_before = []
    assistant = WomensHealthAssistant()
    assistant.answer(AssistantRequest(question="Tenho atraso menstrual", patient_context={}))
    lines_after = Path(ACCESS_LOG_FILE).read_text(encoding="utf-8").splitlines()
    assert len(lines_after) >= len(lines_before)
    json.loads(lines_after[-1])
