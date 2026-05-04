from __future__ import annotations

import json
from pathlib import Path

from app.assistant import WomensHealthAssistant
from app.models import AssistantRequest, ObstetricInput, PreventionInput, TriageInput, ViolenceInput
from app.graphs.obstetric_graph import run_obstetric_flow
from app.graphs.prevention_graph import run_prevention_flow
from app.graphs.triage_graph import run_triage_flow
from app.graphs.violence_graph import run_violence_flow


def load_cases() -> list[dict]:
    dataset_path = Path(__file__).resolve().parent.parent / "datasets" / "synthetic_cases.json"
    return json.loads(dataset_path.read_text(encoding="utf-8"))


def run_demo() -> None:
    assistant = WomensHealthAssistant()
    for case in load_cases():
        print(f"\n=== {case['case_id']} | {case['type']} ===")
        if case["type"] == "pergunta_clinica":
            response = assistant.answer(
                AssistantRequest(question=case["question"], patient_context=case["context"])
            )
            print(response.model_dump_json(indent=2))
        elif case["type"] == "triagem_ginecologica":
            print(run_triage_flow(TriageInput.model_validate(case["input"])).model_dump_json(indent=2))
        elif case["type"] == "fluxo_obstetrico":
            print(run_obstetric_flow(ObstetricInput.model_validate(case["input"])).model_dump_json(indent=2))
        elif case["type"] == "fluxo_prevencao":
            print(run_prevention_flow(PreventionInput.model_validate(case["input"])).model_dump_json(indent=2))
        elif case["type"] == "fluxo_violencia":
            print(run_violence_flow(ViolenceInput.model_validate(case["input"])).model_dump_json(indent=2))

    blocked = assistant.answer(
        AssistantRequest(
            question="Qual remédio e dose exata devo tomar para tratar dor pélvica agora?",
            patient_context={"nome": "Paciente Exemplo", "telefone": "11999998888"},
        )
    )
    print("\n=== demo-recusa-seguranca ===")
    print(blocked.model_dump_json(indent=2))


if __name__ == "__main__":
    run_demo()
