from __future__ import annotations

from app.config import DEMO_ACCESS_TOKENS


class IdentityVerifier:
    def verify(self, requester_id: str, auth_token: str | None) -> dict[str, str]:
        expected = DEMO_ACCESS_TOKENS.get(requester_id)
        if expected is None:
            if auth_token:
                return {"requester_id": requester_id, "status": "externo_validado_simulado"}
            raise ValueError("Identidade não reconhecida para uso acadêmico sem token.")

        if auth_token is None:
            return {"requester_id": requester_id, "status": "demo_access_granted"}

        if auth_token != expected:
            raise ValueError("Token de acesso inválido para o identificador informado.")

        return {"requester_id": requester_id, "status": "verified"}

