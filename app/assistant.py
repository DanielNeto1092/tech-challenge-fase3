from __future__ import annotations

from app.knowledge_base import load_knowledge_base
from app.models import AssistantRequest, AssistantResponse
from app.vector_store import HybridRetriever
from app.chains.assistant_chain import build_assistant_chain
from app.security.access_monitor import AccessMonitor
from app.security.anonymizer import anonymize_payload
from app.security.audit import AuditLogger
from app.security.identity import IdentityVerifier
from app.validators.response_validator import build_refusal


class WomensHealthAssistant:
    def __init__(self) -> None:
        self.documents = load_knowledge_base()
        self.retriever = HybridRetriever(self.documents)
        self.chain = build_assistant_chain()
        self.audit_logger = AuditLogger()
        self.identity_verifier = IdentityVerifier()
        self.access_monitor = AccessMonitor()

    def answer(self, request: AssistantRequest) -> AssistantResponse:
        try:
            self.identity_verifier.verify(request.requester_id, request.auth_token)
            self.access_monitor.log_access(
                endpoint="/assistente/pergunta",
                specialty=request.specialty,
                requester_id=request.requester_id,
                outcome="granted",
                reason=request.access_reason,
            )
        except ValueError as exc:
            self.access_monitor.log_access(
                endpoint="/assistente/pergunta",
                specialty=request.specialty,
                requester_id=request.requester_id,
                outcome="denied",
                reason=str(exc),
            )
            return build_refusal(f"Falha na verificação de identidade simulada: {exc}")

        sanitized_context = anonymize_payload(request.patient_context)
        contexts = self.retriever.retrieve(request.question)
        audit_id = self.audit_logger.log_event(
            "assistant_question",
            {
                "question": request.question,
                "requester_id": request.requester_id,
                "requester_role": request.requester_role,
                "specialty": request.specialty,
                "patient_context": sanitized_context,
                "sources": [ctx.document.doc_id for ctx in contexts],
            },
        )
        response = self.chain.invoke(
            {
                "request": AssistantRequest(question=request.question, patient_context=sanitized_context),
                "question": request.question,
                "context": sanitized_context,
                "retrieved": [ctx.document.content for ctx in contexts],
                "contexts": contexts,
            }
        )
        response.justification = f"{response.justification} Audit ID: {audit_id}."
        return response
