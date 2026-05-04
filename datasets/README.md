# Datasets Sinteticos de Saude da Mulher

## Origem dos dados

Todos os registros desta pasta sao sinteticos e foram criados para simulacao academica baseada em guidelines, protocolos assistenciais e fluxos clinicos amplamente conhecidos no dominio de saude da mulher. Nenhum dado real de paciente e utilizado.

## Estrutura

- `womens_health_qa/`: perguntas e respostas gerais de saude da mulher.
- `gynecological_protocols/`: protocolos estruturados para sinais e sintomas ginecologicos.
- `obstetric_guidelines/`: diretrizes sinteticas para gestacao, pos-parto e amamentacao.
- `violence_detection/`: padroes textuais de risco para violencia domestica.
- `contraceptive/`: base de conhecimento sobre contracepcao e planejamento reprodutivo.
- `breast_cancer/`: rastreio, sinais de alerta e leitura segura de laudos sinteticos.
- `menstrual_health/`: dados educacionais e de risco sobre saude menstrual.
- `maternal_mental_health/`: sofrimento psiquico, puerperio e saude mental materna.

Arquivos auxiliares:

- `generate_synthetic_datasets.py`: gera todos os datasets sinteticos e atualiza os agregados de compatibilidade.
- `synthetic_womens_health_knowledge.json`: compilado legado para compatibilidade com componentes antigos.
- `synthetic_cases.json`: casos demonstrativos para interface e demos.

## Pipeline de dados

O pipeline esta dividido em tres camadas:

1. `data_pipeline/loader.py`
   Carrega os oito datasets por dominio e executa preprocessamento, anonimização e validacao.

2. `data_pipeline/preprocess.py`
   Faz limpeza textual, normalizacao medica, padronizacao de termos e tokenizacao basica.

3. `data_pipeline/anonymizer.py`
   Remove nomes, identificadores numericos, telefones, emails, CPFs e outros marcadores sensiveis.

4. `data_pipeline/validator.py`
   Garante campos obrigatorios, classificacao de risco valida, ausencia de dados sensiveis e coerencia clinica basica.

5. `data_pipeline/formatter.py`
   Converte registros para:
   - instruction tuning (`instruction`, `input`, `output`)
   - documentos de retrieval para RAG

## Uso com LangChain e RAG

- `vectorstore/embeddings.py` implementa embeddings deterministicas locais por hashing, compatíveis com a interface de embeddings do LangChain.
- `vectorstore/index.py` constroi um indice vetorial FAISS real, permite busca semantica e expõe:
  - `DatasetVectorIndex`
  - `build_langchain_retriever`
  - `build_qa_chain`
  - `run_rag_pipeline`

Essa abordagem evita dependencia de dados reais e funciona offline. O índice persistido gera os artefatos `dataset_index.faiss` e `dataset_index.pkl`, além do manifesto `index.json`. Caso um provider externo seja introduzido no futuro, a camada de embeddings pode ser trocada sem alterar o formato dos datasets.

## Exemplos de uso

Gerar datasets:

```bash
python3 datasets/generate_synthetic_datasets.py
```

Preparar corpus de fine-tuning:

```bash
python3 app/training/prepare_dataset.py
```

Criar indice vetorial:

```bash
python3 - <<'PY'
from pathlib import Path
from vectorstore.index import DatasetVectorIndex

index = DatasetVectorIndex.from_datasets()
index.save(Path("data/vector_index"))
PY
```

Executar pipeline RAG:

```bash
python3 - <<'PY'
from vectorstore.index import run_rag_pipeline

print(run_rag_pipeline("Tenho sangramento no pos-parto e febre"))
PY
```

## Limitacoes eticas

- O material nao substitui julgamento clinico.
- O pipeline nao realiza prescricao.
- A base usa apenas simulacao academica e nao valida protocolos institucionais reais.
- A classificacao de risco e orientativa e sempre exige validacao profissional.
