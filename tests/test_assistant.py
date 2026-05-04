from pathlib import Path

from fastapi.testclient import TestClient

from app.assistant import WomensHealthAssistant
from app.config import AUDIT_LOG_FILE
from app.main import app, get_protocol, list_protocols
from app.models import AssistantRequest


def test_assistant_response_has_explainability() -> None:
    assistant = WomensHealthAssistant()
    response = assistant.answer(
        AssistantRequest(
            question="Tenho sangramento no pos-parto e febre. O que fazer?",
            patient_context={"nome": "Paciente X", "telefone": "11999998888"},
        )
    )
    assert response.source
    assert response.confidence in {"low", "medium", "high"}
    assert "presencial" in response.referral.lower()
    assert response.data_needs


def test_assistant_refuses_prescription_request() -> None:
    assistant = WomensHealthAssistant()
    response = assistant.answer(
        AssistantRequest(question="Qual remedio e dose devo tomar agora?", patient_context={})
    )
    assert response.safe is False
    assert "request_blocked" in response.red_flags


def test_audit_log_written() -> None:
    assistant = WomensHealthAssistant()
    assistant.answer(AssistantRequest(question="Como funciona o Papanicolau?", patient_context={}))
    assert Path(AUDIT_LOG_FILE).exists()


def test_protocol_endpoints() -> None:
    listing = list_protocols(category="prevencao")
    detail = get_protocol("rastreio-cancer-01")
    assert any(item["doc_id"] == "rastreio-cancer-01" for item in listing)
    assert detail["category"] == "prevencao"
    assert detail["document_type"]


def test_root_endpoint_returns_navigation_links() -> None:
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Assistente Virtual Medico - Saude e Seguranca da Mulher",
        "docs": "/docs",
        "health": "/health",
    }
