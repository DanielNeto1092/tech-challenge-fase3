# Assistente Virtual Médico - Saúde e Segurança da Mulher

Projeto acadêmico para o Tech Challenge Fase 3. O sistema simula um assistente virtual de apoio clínico especializado em saúde feminina, com foco em segurança da paciente, privacidade, LGPD, explainability e fluxos automatizados com LangGraph. A camada de dados foi organizada como um módulo próprio, com oito datasets sintéticos especializados para fine-tuning simulado, retrieval e suporte a fluxos clínicos. Ele nunca substitui profissionais de saúde, não prescreve medicamentos e não fornece diagnóstico definitivo.

## Objetivo

Desenvolver uma aplicação com LLM e automação de fluxos para:

- responder perguntas contextualizadas sobre saúde da mulher;
- consultar base de conhecimento local sintética multi-domínio;
- executar triagens e protocolos simulados com LangGraph;
- registrar auditoria e proteger dados sensíveis;
- bloquear respostas perigosas;
- demonstrar pipeline de fine-tuning ou simulação técnica equivalente com datasets estruturados.

## Arquitetura

O projeto segue separação por responsabilidades:

- `app/config/`: configuração da aplicação.
- `app/domain/`: modelos de domínio.
- `app/services/`: serviços principais do assistente e protocolos.
- `app/chains/`: organização da chain principal.
- `app/graphs/`: acesso aos fluxos LangGraph.
- `app/security/`: acesso aos módulos de segurança.
- `app/validators/`: validação e bloqueio de respostas inseguras.
- `app/logs/`: estrutura local de logs.
- `app/tests/`: ponto reservado para testes no escopo do app.
- `app/training/`: pipeline acadêmico de fine-tuning simulado.
- `datasets/`: datasets sintéticos especializados por domínio, casos demonstrativos e agregados de compatibilidade.
- `data_pipeline/`: carga, preprocessamento, anonimização, formatação e validação dos datasets.
- `vectorstore/`: embeddings locais, índice vetorial FAISS e integração com retrieval.
- `tests/`: cobertura automatizada de segurança, fluxos e auditoria.
- `docs/`: relatório técnico.

## Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- Pydantic
- LangChain
- LangChain Community
- LangGraph
- FAISS
- pytest

## Como Rodar

1. Criar e ativar ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -e .
```

Arquivo de ambiente de exemplo:

```bash
cp .env.example .env
```

3. Gerar datasets sintéticos e preparar corpus para fine-tuning simulado:

```bash
python datasets/generate_synthetic_datasets.py
python app/training/prepare_dataset.py
python app/training/simulate_finetuning.py
python app/training/evaluate.py
```

Arquivos gerados pelo pipeline:

- `datasets/*/records.json`
- `data/train.json`, `data/validation.json`, `data/test.json`
- `data/train.jsonl`, `data/validation.jsonl`, `data/test.jsonl`
- `data/fine_tuning_manifest.json`
- `data/vector_index/index.json`

4. Executar a API:

```bash
uvicorn app.main:app --reload
```

Ou com Docker:

```bash
docker compose up --build
```

5. Executar a interface visual com Streamlit:

```bash
streamlit run streamlit_app.py
```

6. Rodar demonstrações:

```bash
python examples/run_demos.py
python examples/data_layer_examples.py
```

7. Rodar testes:

```bash
pytest
```

## Como Funciona o Assistente

O assistente usa uma cadeia com LangChain para:

1. receber a pergunta e contexto;
2. anonimizar dados sensíveis;
3. recuperar trechos relevantes dos datasets sintéticos especializados;
4. construir resposta explicável com fonte e nível de confiança;
5. validar a resposta antes do retorno.

A recuperação é híbrida:

- score lexical local para preservar previsibilidade acadêmica;
- indexação vetorial FAISS com embeddings determinísticas compatíveis com LangChain para demonstrar arquitetura RAG sem depender de modelos externos.

## Camada de Dados

Os dados foram separados em oito domínios, cada um com registros próprios em `datasets/<dominio>/records.json`:

- `womens_health_qa`
- `gynecological_protocols`
- `obstetric_guidelines`
- `violence_detection`
- `contraceptive`
- `breast_cancer`
- `menstrual_health`
- `maternal_mental_health`

O pipeline correspondente foi implementado em:

- `data_pipeline/loader.py`: carga dos oito datasets e manifesto de validação.
- `data_pipeline/preprocess.py`: limpeza de texto, normalização médica, padronização e tokenização.
- `data_pipeline/anonymizer.py`: mascaramento de nome, idade livre, CPF, telefone, e-mail e identificadores.
- `data_pipeline/validator.py`: checagem de campos obrigatórios, consistência de risco e ausência de dados sensíveis.
- `data_pipeline/formatter.py`: geração de corpus para instruction tuning e documentos para RAG.
- `vectorstore/index.py`: índice vetorial FAISS, retriever LangChain e pipeline QA.

Os fluxos LangGraph também passaram a consultar contexto protocolar derivado dos datasets por meio de um serviço dedicado, de modo que triagem, obstetrícia, prevenção e violência doméstica não dependem apenas de regras fixas.

Cada resposta retorna:

- resumo da orientação;
- justificativa;
- fonte/protocolo;
- nível de confiança;
- limites da resposta;
- dados adicionais necessários;
- recomendação de encaminhamento;
- nível de risco.

## Fluxos LangGraph

### 1. Triagem ginecológica

Sintomas relatados -> análise de risco -> classificação de urgência -> sugestão de exames -> orientações iniciais -> encaminhamento.

```mermaid
flowchart TD
    A[Sintomas relatados] --> B[Analise de risco]
    B --> C[Classificacao de urgencia]
    C --> D[Sugestao de exames]
    D --> E[Orientacoes iniciais]
    E --> F[Recomendacao de agendamento ou encaminhamento]
```

### 2. Violência doméstica

Sinais de alerta -> avaliação de risco -> protocolo de segurança -> acionamento de equipe especializada -> documentação segura -> seguimento.

```mermaid
flowchart TD
    A[Sinais de alerta] --> B[Avaliacao de risco]
    B --> C[Protocolo de seguranca]
    C --> D[Acionamento de equipe especializada]
    D --> E[Documentacao segura]
    E --> F[Recomendacao de seguimento]
```

### 3. Fluxo obstétrico

Dados da gestante -> avaliação de risco gestacional -> orientações -> exames recomendados -> alertas de urgência -> acompanhamento.

```mermaid
flowchart TD
    A[Dados da gestante] --> B[Avaliacao de risco gestacional]
    B --> C[Orientacoes gerais]
    C --> D[Sugestao de exames]
    D --> E[Alertas de urgencia]
    E --> F[Acompanhamento continuo]
```

### 4. Prevenção

Histórico da paciente -> identificação de exames em atraso -> orientações preventivas -> sugestão de agendamento -> lembretes organizacionais.

```mermaid
flowchart TD
    A[Historico da paciente] --> B[Identificacao de exames devidos]
    B --> C[Orientacoes preventivas]
    C --> D[Agendamento sugerido]
    D --> E[Lembretes personalizados]
```

## Endpoints Disponíveis

- `GET /health`: status da aplicação.
- `GET /`: endpoint raiz com links úteis.
- `POST /assist`: resposta assistida com explainability.
- `POST /assistente/pergunta`: alias no formato solicitado pelo enunciado.
- `GET /protocols`: lista protocolos sintéticos; aceita filtro `category`.
- `GET /protocols/{doc_id}`: detalhe de um protocolo local.
- `GET /auditoria/relatorio-especialidade`: relatório agregado de acesso por especialidade.
- `POST /flows/triage`
- `POST /flows/obstetric`
- `POST /flows/prevention`
- `POST /flows/violence`
- `POST /fluxo/triagem-ginecologica`
- `POST /fluxo/violencia-domestica`
- `POST /fluxo/obstetrico`
- `POST /fluxo/prevencao`

## Interface Visual

O projeto inclui uma interface em Streamlit com:

- pergunta clínica contextualizada;
- abas para os quatro fluxos LangGraph;
- visualização de risco, confiança, fonte e limites;
- navegação pelos protocolos derivados dos datasets sintéticos;
- painel de auditoria agregada por especialidade.

Arquivo principal:

- `streamlit_app.py`

## Fine-Tuning ou Simulação

O projeto inclui uma simulação técnica de fine-tuning em `app/training/`:

- `prepare_dataset.py`: consome os oito datasets, aplica preprocessamento, validação e exporta treino, validação e teste em JSON e JSONL.
- `simulate_finetuning.py`: gera histórico de epochs e métricas sintéticas de grounding, segurança e consistência.
- `evaluate.py`: resume métricas finais.

Em ambiente real, esse pipeline seria substituído por treinamento supervisionado de um modelo open-source pequeno com dados sintéticos, validação clínica, avaliação de segurança e revisão humana.

O dataset sintético inclui:

- perguntas e respostas em saúde da mulher;
- protocolos ginecológicos;
- diretrizes obstétricas;
- padrões de detecção de violência doméstica;
- conhecimento contraceptivo;
- rastreio de câncer de mama;
- saúde menstrual;
- saúde mental materna.

## Exemplos de Uso

Pergunta clínica contextualizada:

```json
{
  "question": "Estou no pós-parto e com tristeza persistente. Isso é sinal de alerta?",
  "patient_context": {
    "postpartum_days": 21
  }
}
```

Caso de recusa por segurança:

```json
{
  "question": "Qual remédio e dose exata devo tomar agora?",
  "patient_context": {}
}
```

## Cuidados com LGPD e Segurança

- uso exclusivo de dados sintéticos e anonimizados;
- mascaramento de telefone, email e CPF;
- remoção de campos identificadores em payloads;
- verificação de identidade simulada para o solicitante;
- criptografia simulada para trilhas de auditoria e acesso;
- auditoria com log mínimo necessário;
- monitoramento de acessos por especialidade;
- confidencialidade reforçada em casos sensíveis;
- encaminhamento obrigatório em risco alto, urgência obstétrica ou suspeita de violência doméstica.

## Integração Hospitalar Simulada

- não existe integração real com prontuário, hospital, farmácia ou agenda;
- a arquitetura demonstra onde protocolos, histórico, fluxos e auditoria seriam conectados;
- toda integração descrita é meramente ilustrativa e acadêmica.

## Referências do Módulo de Dados

- visão geral da camada: [datasets/README.md](/mnt/c/desenvolvimento/repositorio/tech-challenge-fase3/datasets/README.md)
- exemplo de uso programático: [examples/data_layer_examples.py](/mnt/c/desenvolvimento/repositorio/tech-challenge-fase3/examples/data_layer_examples.py)
- testes da camada de dados: [tests/test_data_pipeline.py](/mnt/c/desenvolvimento/repositorio/tech-challenge-fase3/tests/test_data_pipeline.py)

## Casos de Uso

- apoio à triagem ginecológica;
- apoio ao seguimento obstétrico;
- orientação preventiva e rastreamento;
- detecção de sinais de violência doméstica com encaminhamento seguro;
- apoio documental e consulta a protocolos sintéticos por especialidade.

## Avaliação, Bias e Equidade

- métricas sintéticas de grounding e segurança são geradas em `data/finetuning_metrics.json`;
- o manifesto `data/fine_tuning_manifest.json` resume balanceamento por categoria, especialidade e representatividade;
- a avaliação de equidade é acadêmica e deve evoluir com revisão multidisciplinar e ampliação da base sintética.

## Feedback Profissional

- a validação por especialistas está simulada e descrita em [docs/validacao_especialistas.md](/mnt/c/desenvolvimento/repositorio/tech-challenge-fase3/docs/validacao_especialistas.md:1);
- o uso real exigiria revisão formal de ginecologia, obstetrícia, saúde mental, assistência social e governança clínica.

## Limitações Éticas

- o sistema não substitui consulta médica, psicológica, social ou jurídica;
- a base é sintética e acadêmica, sem valor assistencial real;
- não há prescrição, diagnóstico definitivo nem personalização terapêutica;
- recomendações preventivas dependem de diretrizes institucionais e avaliação individual.

## Demonstração em Vídeo

Para um vídeo de até 15 minutos:

1. apresentar objetivo, escopo acadêmico e guardrails.
2. mostrar a arquitetura e pastas principais.
3. executar `python examples/run_demos.py`.
4. demonstrar chamada à API `POST /assist`.
5. executar um fluxo de triagem e um de violência doméstica.
6. mostrar o pipeline de fine-tuning simulado.
7. encerrar com limitações éticas, LGPD e próximos passos.
