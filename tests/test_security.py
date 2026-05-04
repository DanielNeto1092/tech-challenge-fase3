from app.security.anonymizer import anonymize_payload, mask_sensitive_text


def test_mask_sensitive_text() -> None:
    text = "Contato Maria pelo email maria@example.com e telefone 11999998888"
    sanitized = mask_sensitive_text(text)
    assert "maria@example.com" not in sanitized
    assert "11999998888" not in sanitized


def test_anonymize_payload() -> None:
    payload = {"nome": "Ana", "telefone": "11999998888", "contexto": "email ana@teste.com"}
    sanitized = anonymize_payload(payload)
    assert sanitized["nome"] == "[DADO_SENSIVEL_REMOVIDO]"
    assert "[EMAIL_REMOVIDO]" in sanitized["contexto"]
