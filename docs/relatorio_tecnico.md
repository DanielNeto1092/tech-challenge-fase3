# Relatório Técnico

## Introdução

Este projeto acadêmico propõe um assistente virtual médico especializado em saúde e segurança da mulher. O foco está em apoio informacional, triagem assistida, segurança da resposta, proteção de dados e uso de fluxos controlados com LangGraph. O sistema não substitui profissionais habilitados e foi desenhado para demonstrar arquitetura e boas práticas em IA generativa aplicada a contexto sensível.

## Metodologia

A metodologia foi dividida em cinco frentes:

1. curadoria de base sintética;
2. normalização e anonimização de conteúdo;
3. construção de uma cadeia com LangChain para recuperação e resposta explicável;
4. automação de fluxos com LangGraph;
5. validação de segurança, auditoria e testes automatizados.

## Curadoria dos Dados

A base sintética cobre:

- contraceptivos;
- sintomas ginecológicos;
- sinais de alerta em gravidez e pós-parto;
- amamentação;
- menopausa e climatério;
- rastreio de câncer de mama e colo do útero;
- saúde mental materna;
- possível violência doméstica.
- laudos sintéticos de mamografia e ultrassom;
- procedimento ginecológico sintético;
- protocolo sintético de pré-natal;
- base sintética de segurança medicamentosa sem prescrição.

Todos os registros são fictícios, anonimizados e adequados a uso acadêmico.

## Anonimização

O módulo `security/anonymizer.py` aplica:

- mascaramento de telefone, email e CPF em texto livre;
- remoção de campos identificadores em dicionários;
- propagação recursiva do processo para listas e estruturas compostas.

Essa abordagem reduz risco de exposição indevida e reforça aderência a princípios da LGPD, especialmente minimização e necessidade.

Além disso, o projeto inclui verificação de identidade simulada, monitoramento de acessos por especialidade e criptografia simulada para payloads auditados.

## Arquitetura do Assistente

O assistente foi estruturado com as seguintes camadas:

- `app/knowledge_base.py`: leitura da base sintética;
- `app/retrieval.py`: recuperação lexical de base;
- `app/vector_store.py`: recuperação híbrida com FAISS e embeddings determinísticas locais;
- `app/chains/assistant_chain.py`: cadeia em LangChain para composição da resposta;
- `app/validators/response_validator.py`: validação final e recusa segura;
- `app/security/audit.py`: trilha de auditoria;
- `app/main.py`: API FastAPI para integração.

O modelo de resposta foi desenhado para explainability, retornando resumo, justificativa, fonte, confiança, limites, encaminhamento e risco.
Também foi incluído o campo de dados adicionais necessários, para explicitar quando o caso exige mais informação clínica antes de qualquer inferência segura.

## Funcionamento do LangChain

O uso de LangChain foi aplicado na composição da cadeia principal:

1. um `ChatPromptTemplate` organiza a instrução sistêmica e a entrada do usuário;
2. o contexto recuperado localmente por busca híbrida é injetado como grounding;
3. um `RunnableLambda` produz uma resposta estruturada com foco em segurança.

Embora a geração esteja simulada de forma determinística, a arquitetura está pronta para troca por uma LLM real, preservando o contrato da cadeia.

Para demonstrar RAG sem depender de modelos externos, foi usada uma indexação FAISS com embeddings determinísticas. Isso permite reproduzir a arquitetura vetorial localmente e manter o caráter acadêmico do projeto.

## Funcionamento do LangGraph

Os fluxos foram implementados como grafos explícitos:

- triagem ginecológica;
- violência doméstica;
- fluxo obstétrico;
- prevenção.

Cada fluxo possui nós de avaliação, classificação e decisão. Essa abordagem facilita rastreabilidade, testes e manutenção.

## Infraestrutura de Execução

O projeto inclui:

- `requirements.txt` para instalação direta;
- `Dockerfile` para empacotamento da API;
- `docker-compose.yml` para subida padronizada do serviço com persistência de `logs/` e `data/`.

## Segurança e Validação

Foram implementadas regras mandatórias:

- nunca prescrever medicamentos;
- nunca fornecer diagnóstico definitivo;
- sempre recomendar atendimento presencial em sinais de alarme;
- sempre encaminhar suspeita de violência doméstica para equipe qualificada;
- manter confidencialidade em casos sensíveis.

O validador marca respostas inseguras, exige encaminhamento presencial em risco alto e bloqueia conteúdo que viole escopo assistencial.

Os módulos de segurança cobrem:

- anonimização e mascaramento;
- verificação de identidade simulada;
- criptografia simulada para trilhas de auditoria;
- monitoramento de acesso com relatório por especialidade.

## Análise de Bias e Equidade

Mesmo com base sintética, existem riscos de viés:

- simplificação excessiva de contextos sociais complexos;
- sub-representação de populações vulneráveis;
- dependência de terminologia padronizada que pode ignorar linguagem leiga.

Mitigações propostas:

- revisão multidisciplinar dos prompts e conteúdos;
- expansão do dataset sintético com linguagem inclusiva;
- avaliação periódica por cenários de equidade e sensibilidade cultural.

## Considerações Éticas

Trata-se de uma ferramenta de apoio acadêmico. O sistema não deve ser usado para decisão clínica real. Em temas como violência doméstica, saúde mental e urgências obstétricas, a automação deve servir apenas para reconhecer risco, orientar acolhimento e acionar profissionais qualificados.

## Validação por Especialistas

A validação clínica formal não foi realizada, pois o projeto é acadêmico. Ainda assim, foi incluído um fluxo de validação simulada com checklist e papéis recomendados em `docs/validacao_especialistas.md`.

## Conclusão

O projeto demonstra como combinar IA generativa, RAG local, LangChain, LangGraph, validação e proteção de dados em um domínio sensível. A solução privilegia segurança e transparência, oferecendo uma base consistente para discussão acadêmica sobre sistemas de apoio clínico responsáveis.
