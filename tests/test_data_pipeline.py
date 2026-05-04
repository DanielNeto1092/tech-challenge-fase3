from __future__ import annotations

from pathlib import Path

from data_pipeline.anonymizer import anonymize_text
from data_pipeline.loader import load_processed_datasets
from data_pipeline.validator import validate_record
from vectorstore.index import DatasetVectorIndex, run_rag_pipeline


def test_anonymizer_masks_identifiers() -> None:
    text = "Paciente Maria Souza, 32 anos, telefone 11999998888 e cpf 123.456.789-10."
    masked = anonymize_text(text)
    assert "Maria" not in masked
    assert "11999998888" not in masked
    assert "123.456.789-10" not in masked
    assert "[ANON]" in masked
    assert "idade 30-35" in masked


def test_processed_datasets_load_all_domains() -> None:
    bundle = load_processed_datasets()
    assert len(bundle) == 8
    assert all(bundle.values())


def test_records_are_valid_after_generation() -> None:
    bundle = load_processed_datasets()
    for records in bundle.values():
        for record in records:
            assert validate_record(record) == []


def test_vector_index_returns_relevant_doc() -> None:
    index = DatasetVectorIndex.from_datasets()
    hits = index.search("sangramento no pos-parto e febre", top_k=3)
    assert hits
    assert any(hit.document["doc_id"] == "gestacao-alerta-01" for hit in hits)


def test_rag_pipeline_contains_context_and_alert() -> None:
    result = run_rag_pipeline("medo do parceiro e isolamento social")
    assert result["context"]
    assert "Validacao profissional obrigatoria" in result["answer"]


def test_vector_index_persists_real_faiss_files(tmp_path: Path) -> None:
    index = DatasetVectorIndex.from_datasets()
    metadata_path = index.save(tmp_path)

    assert metadata_path.name == "index.json"
    assert (tmp_path / "dataset_index.faiss").exists()
    assert (tmp_path / "dataset_index.pkl").exists()
