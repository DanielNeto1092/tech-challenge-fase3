from __future__ import annotations

from pprint import pprint

from data_pipeline.loader import load_processed_datasets
from vectorstore.index import DatasetVectorIndex, run_rag_pipeline


def main() -> None:
    bundle = load_processed_datasets()
    print("Datasets carregados:")
    for dataset_name, items in bundle.items():
        print(f"- {dataset_name}: {len(items)} registros")

    print("\nExemplo 1 - consulta QA")
    pprint(run_rag_pipeline("Quais sinais no pos-parto exigem avaliacao rapida?"))

    print("\nExemplo 2 - busca de protocolo")
    index = DatasetVectorIndex.from_datasets()
    protocol_hits = index.search("dor pelvica intensa com febre", top_k=2)
    pprint([{"doc_id": hit.document["doc_id"], "title": hit.document["title"], "score": hit.score} for hit in protocol_hits])

    print("\nExemplo 3 - deteccao de violencia")
    violence_hits = index.search("medo do parceiro e controle do celular", top_k=2)
    pprint([{"doc_id": hit.document["doc_id"], "title": hit.document["title"], "score": hit.score} for hit in violence_hits])

    print("\nExemplo 4 - recomendacao de exame")
    screening_hits = index.search("historico familiar de cancer de mama e Papanicolau atrasado", top_k=2)
    pprint([{"doc_id": hit.document["doc_id"], "title": hit.document["title"], "score": hit.score} for hit in screening_hits])


if __name__ == "__main__":
    main()
