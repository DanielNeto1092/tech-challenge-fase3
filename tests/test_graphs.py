from app.models import ObstetricInput, PreventionInput, TriageInput, ViolenceInput
from app.graphs.obstetric_graph import run_obstetric_flow
from app.graphs.prevention_graph import run_prevention_flow
from app.graphs.triage_graph import run_triage_flow
from app.graphs.violence_graph import run_violence_flow


def test_triage_flow() -> None:
    result = run_triage_flow(
        TriageInput(
            sintomas=["dor pélvica intensa", "febre"],
            contexto="Piora rapida com corrimento",
            idade=32,
        )
    )
    assert result.urgency in {"urgent", "emergency"}
    assert "presencial" in result.escalation.lower()
    assert any("base sintética consultada" in note.lower() for note in result.notes)


def test_obstetric_flow() -> None:
    result = run_obstetric_flow(
        ObstetricInput(
            idade_gestacional_semanas=30,
            sintomas=["cefaleia intensa", "visão embaçada"],
            contexto="Movimentos fetais reduzidos",
        )
    )
    assert result.urgency in {"urgent", "emergency"}
    assert any("pressão" in exam.lower() or "pressao" in exam.lower() for exam in result.suggested_exams)
    assert any("base sintética consultada" in note.lower() for note in result.notes)


def test_prevention_flow() -> None:
    result = run_prevention_flow(
        PreventionInput(
            idade=45,
            historico=["mae com cancer de mama"],
            exames_realizados=["Papanicolau ha 5 anos"],
        )
    )
    assert result.urgency in {"routine", "priority"}
    assert len(result.suggested_exams) >= 2
    assert any("base sintética consultada" in note.lower() for note in result.notes)


def test_violence_flow() -> None:
    result = run_violence_flow(
        ViolenceInput(
            sinais_alerta=["medo do parceiro", "lesões frequentes"],
            contexto="Parceiro controla o dinheiro",
            risco_imediato=True,
        )
    )
    assert result.urgency == "emergency"
    assert "equipe especializada" in result.escalation.lower()
    assert any("base sintética consultada" in note.lower() for note in result.notes)
