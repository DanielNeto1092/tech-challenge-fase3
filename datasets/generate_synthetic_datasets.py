from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


DATASETS = {
    "womens_health_qa": [
        {
            "doc_id": "womens-health-qa-01",
            "title": "Dor pelvica e avaliacao inicial",
            "question": "Quando dor pelvica exige avaliacao presencial?",
            "context": "Pessoa adulta com dor pelvica de inicio recente e sem uso de dados reais.",
            "answer": "Dor pelvica com febre, desmaio, rigidez abdominal, sangramento importante ou piora rapida exige avaliacao presencial prioritaria.",
            "source": "guideline_simulada_saude_mulher_v1",
            "risk_level": "alto",
            "category": "womens_health_qa",
            "specialty": "saude_da_mulher",
            "keywords": ["dor pelvica", "febre", "sangramento", "desmaio"],
            "representativity_tags": ["atencao_primaria", "periferia_urbana"],
        },
        {
            "doc_id": "womens-health-qa-02",
            "title": "Leucorreia sem sinais sistemicos",
            "question": "Corrimento leve pode aguardar consulta ambulatorial?",
            "context": "Relato sintetico de corrimento leve sem febre e sem dor intensa.",
            "answer": "Sem sinais sistemicos, a orientacao segura e organizar consulta programada, reforcando retorno rapido se surgirem dor intensa, odor forte persistente ou febre.",
            "source": "guideline_simulada_saude_mulher_v1",
            "risk_level": "moderado",
            "category": "womens_health_qa",
            "specialty": "ginecologia",
            "keywords": ["corrimento", "odor forte", "febre"],
            "representativity_tags": ["atencao_secundaria"],
        },
        {
            "doc_id": "womens-health-qa-03",
            "title": "Planejamento de consulta ginecologica",
            "question": "Como organizar uma consulta preventiva de rotina?",
            "context": "Pergunta sintetica sobre prevencao em saude da mulher.",
            "answer": "A consulta preventiva deve revisar historico menstrual, vida sexual, exames em atraso, vacinacao, fatores de risco e sinais de alarme que justifiquem avaliacao presencial antecipada.",
            "source": "guideline_simulada_saude_mulher_v1",
            "risk_level": "baixo",
            "category": "womens_health_qa",
            "specialty": "saude_da_mulher",
            "keywords": ["prevencao", "consulta", "vacinacao"],
            "representativity_tags": ["saude_publica"],
        },
        {
            "doc_id": "womens-health-qa-04",
            "title": "Pos-parto e sinais de alerta",
            "question": "Quais sinais no pos-parto exigem revisao clinica rapida?",
            "context": "Pergunta sintetica sobre seguimento pos-parto.",
            "answer": "Sangramento excessivo, febre, dor mamaria intensa, tristeza persistente, falta de ar e dor abdominal forte merecem avaliacao clinica rapida.",
            "source": "guideline_simulada_saude_mulher_v1",
            "risk_level": "alto",
            "category": "womens_health_qa",
            "specialty": "obstetricia",
            "keywords": ["pos-parto", "sangramento", "febre", "falta de ar"],
            "representativity_tags": ["pos_parto", "prenatal_sus"],
        },
    ],
    "gynecological_protocols": [
        {
            "doc_id": "gineco-sintomas-01",
            "title": "Corrimento, prurido e dor pelvica",
            "condition": "Corrimento com prurido e dor pelvica",
            "symptoms": ["corrimento", "prurido", "dor pelvica", "odor forte"],
            "risk_classification": "alto",
            "recommended_actions": [
                "avaliar sinais sistemicos",
                "priorizar exame ginecologico presencial",
                "orientar retorno imediato se houver febre ou sangramento"
            ],
            "requires_referral": True,
            "source": "linha_cuidado_ginecologico_simulada_v2",
            "category": "sintomas_ginecologicos",
            "specialty": "ginecologia",
            "keywords": ["corrimento", "prurido", "dor pelvica", "febre"],
            "representativity_tags": ["atencao_secundaria", "periferia_urbana"],
        },
        {
            "doc_id": "ultrassom-pelvico-01",
            "title": "Revisao de ultrassom pelvico sintetico",
            "condition": "Achado em ultrassom pelvico com sintoma associado",
            "symptoms": ["massa anexial", "sangramento anormal", "dor intensa"],
            "risk_classification": "alto",
            "recommended_actions": [
                "correlacionar laudo com exame clinico",
                "encaminhar para ginecologia",
                "avaliar urgencia conforme intensidade da dor"
            ],
            "requires_referral": True,
            "source": "colecao_simulada_laudos_pelvicos_v1",
            "category": "documentos_especializados",
            "specialty": "ginecologia",
            "keywords": ["ultrassom", "massa anexial", "sangramento"],
            "representativity_tags": ["imagem_diagnostica"],
        },
        {
            "doc_id": "gineco-menopausa-01",
            "title": "Sangramento apos menopausa",
            "condition": "Sangramento apos menopausa",
            "symptoms": ["sangramento uterino", "menopausa", "dor pelvica"],
            "risk_classification": "alto",
            "recommended_actions": [
                "encaminhar para avaliacao ginecologica",
                "revisar historico e tempo de menopausa",
                "nao atrasar investigacao presencial"
            ],
            "requires_referral": True,
            "source": "manual_simulado_saude_mulher_adulta_v1",
            "category": "menopausa",
            "specialty": "ginecologia",
            "keywords": ["menopausa", "sangramento"],
            "representativity_tags": ["meia_idade"],
        },
        {
            "doc_id": "gineco-rastreio-ectopia-01",
            "title": "Sangramento pos-coito",
            "condition": "Sangramento apos relacao sexual",
            "symptoms": ["sangramento pos-coito", "corrimento", "dor na relacao sexual"],
            "risk_classification": "moderado",
            "recommended_actions": [
                "organizar consulta com exame especular",
                "revisar preventivos em atraso",
                "acelerar avaliacao se houver dor intensa ou sangramento persistente"
            ],
            "requires_referral": True,
            "source": "protocolo_simulado_ginecologia_ambulatorial_v1",
            "category": "sintomas_ginecologicos",
            "specialty": "ginecologia",
            "keywords": ["sangramento pos-coito", "preventivo"],
            "representativity_tags": ["atencao_primaria"],
        },
    ],
    "obstetric_guidelines": [
        {
            "doc_id": "gestacao-alerta-01",
            "title": "Sinais de alerta na gravidez e pos-parto",
            "condition": "Sinais de alerta na gestacao e no pos-parto",
            "symptoms": ["sangramento vaginal", "cefaleia intensa", "falta de ar", "convulsoes"],
            "risk_classification": "critico",
            "recommended_actions": [
                "encaminhar para atendimento imediato",
                "priorizar seguranca materno-fetal",
                "orientar servico de urgencia sem atraso"
            ],
            "requires_referral": True,
            "source": "protocolo_obstetrico_simulado_v3",
            "category": "obstetricia",
            "specialty": "obstetricia",
            "keywords": ["gravidez", "pos-parto", "cefaleia intensa", "sangramento"],
            "representativity_tags": ["alto_risco", "prenatal_sus", "zona_rural"],
        },
        {
            "doc_id": "obstetrico-hipertensao-01",
            "title": "Suspeita de sindrome hipertensiva na gestacao",
            "condition": "Gestante com cefaleia intensa e alteracao visual",
            "symptoms": ["cefaleia intensa", "visao embaçada", "edema subbito"],
            "risk_classification": "alto",
            "recommended_actions": [
                "avaliar presencialmente no mesmo dia",
                "verificar sinais de gravidade",
                "encaminhar para obstetricia se persistirem sintomas"
            ],
            "requires_referral": True,
            "source": "guideline_simulada_risco_gestacional_v1",
            "category": "obstetricia",
            "specialty": "obstetricia",
            "keywords": ["cefaleia", "visao turva", "edema"],
            "representativity_tags": ["alto_risco"],
        },
        {
            "doc_id": "obstetrico-pre-natal-01",
            "title": "Organizacao do pre-natal de rotina",
            "condition": "Gestacao sem sinais de alarme",
            "symptoms": ["consulta de rotina", "seguimento gestacional"],
            "risk_classification": "baixo",
            "recommended_actions": [
                "manter consultas programadas",
                "revisar exames do trimestre",
                "reforcar educacao sobre sinais de alarme"
            ],
            "requires_referral": False,
            "source": "guideline_simulada_pre_natal_v1",
            "category": "obstetricia",
            "specialty": "obstetricia",
            "keywords": ["pre-natal", "rotina", "exames"],
            "representativity_tags": ["atencao_primaria"],
        },
        {
            "doc_id": "obstetrico-amamentacao-01",
            "title": "Dor mamaria e dificuldade de pega",
            "condition": "Dificuldade na amamentacao com dor mamaria",
            "symptoms": ["dor mamaria", "fissura", "dificuldade de pega", "febre"],
            "risk_classification": "moderado",
            "recommended_actions": [
                "avaliar tecnica de amamentacao",
                "encaminhar para enfermagem ou banco de leite se persistir",
                "priorizar avaliacao rapida se houver febre"
            ],
            "requires_referral": True,
            "source": "guia_simulado_aleitamento_materno_v1",
            "category": "amamentacao",
            "specialty": "obstetricia",
            "keywords": ["amamentacao", "fissura", "mastite"],
            "representativity_tags": ["pos_parto", "atencao_primaria"],
        },
    ],
    "violence_detection": [
        {
            "doc_id": "violencia-domestica-01",
            "title": "Medo do parceiro e controle coercitivo",
            "text": "Pessoa relata medo do parceiro, controle do celular e isolamento social progressivo.",
            "risk_score": 0.94,
            "risk_level": "alto",
            "requires_intervention": True,
            "source": "protocolo_simulado_protecao_mulher_v3",
            "category": "violencia_domestica",
            "specialty": "protecao_social",
            "keywords": ["medo do parceiro", "isolamento", "controle do celular"],
            "representativity_tags": ["violencia_genero", "rede_protecao"],
        },
        {
            "doc_id": "violencia-domestica-02",
            "title": "Lesoes repetidas e explicacoes inconsistentes",
            "text": "Relato sintetico de lesoes frequentes com justificativas inconsistentes e ansiedade intensa na consulta.",
            "risk_score": 0.88,
            "risk_level": "alto",
            "requires_intervention": True,
            "source": "protocolo_simulado_protecao_mulher_v3",
            "category": "violencia_domestica",
            "specialty": "protecao_social",
            "keywords": ["lesoes frequentes", "ansiedade", "inconsistencia"],
            "representativity_tags": ["violencia_genero", "assistencia_social"],
        },
        {
            "doc_id": "violencia-domestica-03",
            "title": "Conflito verbal sem sinal claro de coercao",
            "text": "Pessoa descreve conflito verbal com parceiro, sem relatar ameacas, lesoes ou vigilancia constante.",
            "risk_score": 0.32,
            "risk_level": "moderado",
            "requires_intervention": False,
            "source": "protocolo_simulado_protecao_mulher_v3",
            "category": "violencia_domestica",
            "specialty": "protecao_social",
            "keywords": ["conflito verbal", "vigilancia"],
            "representativity_tags": ["acolhimento"],
        },
        {
            "doc_id": "violencia-domestica-04",
            "title": "Coercao sexual e ameaca direta",
            "text": "Relato sintetico de coercao sexual, ameacas e restricao de acesso a dinheiro e transporte.",
            "risk_score": 0.97,
            "risk_level": "alto",
            "requires_intervention": True,
            "source": "protocolo_simulado_protecao_mulher_v3",
            "category": "violencia_domestica",
            "specialty": "protecao_social",
            "keywords": ["coercao sexual", "ameacas", "controle financeiro"],
            "representativity_tags": ["violencia_genero", "rede_protecao"],
        },
    ],
    "contraceptive": [
        {
            "doc_id": "faq-contraceptivos-01",
            "title": "Contraceptivos hormonais combinados",
            "question": "Quais cuidados antecedem o uso de contraceptivo hormonal combinado?",
            "context": "Pergunta sintetica para apoio educativo em planejamento reprodutivo.",
            "answer": "Deve-se revisar risco cardiovascular, tabagismo, enxaqueca com aura, historico trombotico e necessidade de avaliacao presencial antes de iniciar ou trocar metodo.",
            "source": "protocolo_simulado_planejamento_reprodutivo_v1",
            "risk_level": "moderado",
            "category": "contraceptivos",
            "specialty": "planejamento_familiar",
            "keywords": ["contraceptivo", "hormonal", "trombose", "tabagismo"],
            "representativity_tags": ["adolescentes", "baixa_renda"],
        },
        {
            "doc_id": "faq-contraceptivos-02",
            "title": "Metodo de longa duracao",
            "question": "Quando considerar metodo contraceptivo de longa duracao?",
            "context": "Pergunta sintetica sem dados reais para educacao em saude.",
            "answer": "Metodos de longa duracao podem ser discutidos quando ha interesse em alta eficacia, dificuldade com uso diario ou necessidade de planejamento reprodutivo continuado.",
            "source": "protocolo_simulado_planejamento_reprodutivo_v1",
            "risk_level": "baixo",
            "category": "contraceptivos",
            "specialty": "planejamento_familiar",
            "keywords": ["longo prazo", "diu", "implante"],
            "representativity_tags": ["atencao_primaria"],
        },
        {
            "doc_id": "faq-contraceptivos-03",
            "title": "Pos-parto e escolha do metodo",
            "question": "Como organizar orientacao contraceptiva no pos-parto?",
            "context": "Pergunta sintetica sobre cuidado pos-parto.",
            "answer": "A orientacao deve considerar amamentacao, risco trombotico, preferencia da pessoa e necessidade de revisao presencial antes de definir metodo individual.",
            "source": "protocolo_simulado_planejamento_reprodutivo_v1",
            "risk_level": "moderado",
            "category": "contraceptivos",
            "specialty": "planejamento_familiar",
            "keywords": ["pos-parto", "amamentacao", "metodo"],
            "representativity_tags": ["pos_parto"],
        },
        {
            "doc_id": "faq-contraceptivos-04",
            "title": "Sinais para revisao do metodo",
            "question": "Quais sinais pedem revisao clinica do metodo atual?",
            "context": "Pergunta sintetica sobre seguimento em contracepcao.",
            "answer": "Dor toracica, falta de ar, cefaleia intensa, sangramento importante ou desconforto persistente exigem avaliacao profissional e nao devem ser manejados como ajuste autonomo.",
            "source": "protocolo_simulado_planejamento_reprodutivo_v1",
            "risk_level": "alto",
            "category": "contraceptivos",
            "specialty": "planejamento_familiar",
            "keywords": ["cefaleia intensa", "falta de ar", "sangramento"],
            "representativity_tags": ["seguranca_medicamentosa"],
        },
    ],
    "breast_cancer": [
        {
            "doc_id": "rastreio-cancer-01",
            "title": "Triagem de cancer de mama e colo do utero",
            "question": "Como organizar rastreio de cancer de mama e colo do utero?",
            "context": "Pergunta sintetica sobre rastreio e prevencao em saude publica.",
            "answer": "A orientacao deve considerar faixa etaria, historico, resultados anteriores e necessidade de avaliacao presencial diante de nodulo palpavel, retracao cutanea ou sangramento pos-coito.",
            "source": "protocolo_simulado_prevencao_rastreio_v2",
            "risk_level": "moderado",
            "category": "prevencao",
            "specialty": "mastologia_preventiva",
            "keywords": ["mamografia", "Papanicolau", "nodulo", "sangramento pos-coito"],
            "representativity_tags": ["saude_publica", "atencao_primaria"],
        },
        {
            "doc_id": "laudo-mamografia-01",
            "title": "Laudo sintetico de mamografia com correlacao clinica",
            "question": "Como interpretar laudo sintetico de mamografia de forma segura?",
            "context": "Pergunta sintetica sobre laudos de imagem, sem substituir avaliacao especializada.",
            "answer": "Laudos devem ser correlacionados com exame clinico, historico pessoal e familiar; achados suspeitos ou discordancia clinica exigem avaliacao presencial especializada.",
            "source": "colecao_simulada_laudos_imagem_v1",
            "risk_level": "alto",
            "category": "documentos_especializados",
            "specialty": "mastologia",
            "keywords": ["mamografia", "laudo", "correlacao clinica", "nodulo"],
            "representativity_tags": ["equidade_acesso", "rastreio_populacional"],
        },
        {
            "doc_id": "breast-cancer-qa-03",
            "title": "Nodulo mamario palpavel",
            "question": "Nodulo mamario palpavel precisa de revisao rapida?",
            "context": "Pergunta sintetica sobre sinais de alarme mamarios.",
            "answer": "Nodulo palpavel, retracao cutanea, descarga sanguinolenta ou mudanca rapida da mama justificam avaliacao presencial prioritaria.",
            "source": "guideline_simulada_mastologia_v1",
            "risk_level": "alto",
            "category": "breast_cancer",
            "specialty": "mastologia",
            "keywords": ["nodulo", "retracao", "descarga sanguinolenta"],
            "representativity_tags": ["atencao_secundaria"],
        },
        {
            "doc_id": "breast-cancer-qa-04",
            "title": "Historico familiar e rastreio",
            "question": "Historico familiar muda a organizacao do rastreio?",
            "context": "Pergunta sintetica sobre prevencao personalizada.",
            "answer": "Historico familiar pode antecipar necessidade de avaliacao individualizada e revisao profissional do plano de rastreio, sempre conforme diretrizes locais.",
            "source": "guideline_simulada_mastologia_v1",
            "risk_level": "moderado",
            "category": "breast_cancer",
            "specialty": "mastologia_preventiva",
            "keywords": ["historico familiar", "rastreamento"],
            "representativity_tags": ["equidade_acesso"],
        },
    ],
    "menstrual_health": [
        {
            "doc_id": "menstrual-health-01",
            "title": "Fluxo menstrual intenso",
            "question": "Quando fluxo menstrual intenso pede avaliacao medica?",
            "context": "Pergunta sintetica sobre saude menstrual.",
            "answer": "Fluxo muito intenso com tontura, palidez, sangramento prolongado, dor incapacitante ou piora progressiva pede avaliacao presencial.",
            "source": "guideline_simulada_saude_menstrual_v1",
            "risk_level": "alto",
            "category": "saude_menstrual",
            "specialty": "ginecologia",
            "keywords": ["fluxo intenso", "anemia", "dor incapacitante"],
            "representativity_tags": ["adolescentes", "atencao_primaria"],
        },
        {
            "doc_id": "menstrual-health-02",
            "title": "Atraso menstrual",
            "question": "Como abordar atraso menstrual de forma segura?",
            "context": "Pergunta sintetica para orientacao inicial sem diagnostico definitivo.",
            "answer": "Atraso menstrual exige revisar possibilidade de gestacao, estresse, mudancas hormonais e sinais de alarme, mantendo avaliacao profissional se persistir ou vier com dor forte.",
            "source": "guideline_simulada_saude_menstrual_v1",
            "risk_level": "moderado",
            "category": "saude_menstrual",
            "specialty": "ginecologia",
            "keywords": ["atraso menstrual", "gestacao", "dor forte"],
            "representativity_tags": ["saude_publica"],
        },
        {
            "doc_id": "menstrual-health-03",
            "title": "Dismenorreia importante",
            "question": "Colica incapacitante deve ser investigada?",
            "context": "Pergunta sintetica sobre dor menstrual.",
            "answer": "Dor que impede atividades, piora de forma progressiva, vem com desmaio ou sangramento importante deve ser investigada clinicamente.",
            "source": "guideline_simulada_saude_menstrual_v1",
            "risk_level": "alto",
            "category": "saude_menstrual",
            "specialty": "ginecologia",
            "keywords": ["colica", "dismenorreia", "desmaio"],
            "representativity_tags": ["adolescentes"],
        },
        {
            "doc_id": "menstrual-health-04",
            "title": "Registro do ciclo menstrual",
            "question": "Por que registrar duracao e sintomas do ciclo?",
            "context": "Pergunta sintetica educativa sobre autocuidado menstrual.",
            "answer": "Registrar duracao, intervalo, intensidade do fluxo e sintomas ajuda a reconhecer padroes anormais e qualificar a conversa com profissional habilitado.",
            "source": "guideline_simulada_saude_menstrual_v1",
            "risk_level": "baixo",
            "category": "saude_menstrual",
            "specialty": "ginecologia",
            "keywords": ["registro do ciclo", "autocuidado"],
            "representativity_tags": ["educacao_em_saude"],
        },
    ],
    "maternal_mental_health": [
        {
            "doc_id": "saude-mental-01",
            "title": "Saude mental materna no pos-parto",
            "question": "Tristeza persistente no pos-parto merece avaliacao profissional?",
            "context": "Pergunta sintetica sobre saude mental materna.",
            "answer": "Tristeza persistente, desesperanca, insone relevante, culpa intensa ou dificuldade de vinculo merecem acolhimento e avaliacao profissional; autoagressao e urgencia.",
            "source": "fluxo_simulado_saude_mental_materna_v1",
            "risk_level": "alto",
            "category": "saude_mental",
            "specialty": "saude_mental",
            "keywords": ["pos-parto", "tristeza persistente", "autoagressao"],
            "representativity_tags": ["psicologia", "psiquiatria", "pos_parto"],
        },
        {
            "doc_id": "maternal-mental-health-02",
            "title": "Ansiedade no puerperio",
            "question": "Ansiedade intensa no puerperio precisa de triagem?",
            "context": "Pergunta sintetica sobre sofrimento psiquico no puerperio.",
            "answer": "Ansiedade intensa com insone, exaustao, culpa, ataques de panico ou prejuizo funcional deve ser triada e encaminhada para avaliacao clinica e psicossocial.",
            "source": "fluxo_simulado_saude_mental_materna_v1",
            "risk_level": "moderado",
            "category": "saude_mental",
            "specialty": "saude_mental",
            "keywords": ["ansiedade", "puerperio", "panico"],
            "representativity_tags": ["pos_parto"],
        },
        {
            "doc_id": "maternal-mental-health-03",
            "title": "Dificuldade de vinculo com o bebe",
            "question": "Dificuldade de vinculo com o bebe e um sinal relevante?",
            "context": "Pergunta sintetica sobre alerta psicossocial no pos-parto.",
            "answer": "Dificuldade de vinculo, apatia, evitacao do cuidado e desesperanca sao sinais relevantes e devem ser avaliados por equipe multiprofissional.",
            "source": "fluxo_simulado_saude_mental_materna_v1",
            "risk_level": "moderado",
            "category": "saude_mental",
            "specialty": "saude_mental",
            "keywords": ["vinculo", "apatia", "desesperanca"],
            "representativity_tags": ["assistencia_social", "psicologia"],
        },
        {
            "doc_id": "maternal-mental-health-04",
            "title": "Ideias de ferir a si ou ao bebe",
            "question": "Ideias de ferir a si ou ao bebe configuram urgencia?",
            "context": "Pergunta sintetica sobre seguranca psiquiatrica.",
            "answer": "Sim. Ideias de autoagressao ou de ferir o bebe configuram urgencia psiquiatrica e exigem avaliacao imediata e rede de apoio.",
            "source": "fluxo_simulado_saude_mental_materna_v1",
            "risk_level": "alto",
            "category": "saude_mental",
            "specialty": "saude_mental",
            "keywords": ["autoagressao", "ferir o bebe", "urgencia psiquiatrica"],
            "representativity_tags": ["psiquiatria", "pos_parto"],
        },
    ],
}


DEMO_CASES = [
    {
        "case_id": "demo-clinico-01",
        "type": "pergunta_clinica",
        "question": "Estou no pos-parto e sinto muita tristeza e dificuldade para dormir. Isso pode ser preocupante?",
        "context": {"postpartum_days": 21, "identified_name": "Paciente Exemplo"},
    },
    {
        "case_id": "demo-gineco-01",
        "type": "triagem_ginecologica",
        "input": {
            "sintomas": ["dor pelvica intensa", "febre", "corrimento com odor forte"],
            "contexto": "Sintomas ha 2 dias com piora progressiva",
            "idade": 29,
            "gestante": False,
        },
    },
    {
        "case_id": "demo-obstetrico-01",
        "type": "fluxo_obstetrico",
        "input": {
            "idade_gestacional_semanas": 31,
            "sintomas": ["cefaleia intensa", "visao embaçada", "inchaco subbito"],
            "comorbidades": ["hipertensao gestacional previa"],
            "contexto": "Reducao da movimentacao fetal desde ontem",
        },
    },
    {
        "case_id": "demo-prevencao-01",
        "type": "fluxo_prevencao",
        "input": {
            "idade": 47,
            "historico": ["mae com cancer de mama apos os 50 anos"],
            "exames_realizados": ["Papanicolau ha 4 anos"],
            "contexto": "Sem queixas atuais",
        },
    },
    {
        "case_id": "demo-violencia-01",
        "type": "fluxo_violencia",
        "input": {
            "sinais_alerta": ["medo do parceiro", "isolamento social", "lesoes frequentes"],
            "contexto": "Parceiro monitora o celular",
            "risco_imediato": True,
        },
    },
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def main() -> None:
    for dataset_name, items in DATASETS.items():
        write_json(BASE_DIR / dataset_name / "records.json", items)
    write_json(BASE_DIR / "synthetic_cases.json", DEMO_CASES)
    compiled = []
    for items in DATASETS.values():
        for item in items:
            if "answer" in item:
                content = item["answer"]
            elif "condition" in item:
                content = (
                    "Condicao: "
                    + item["condition"]
                    + ". Sintomas: "
                    + ", ".join(item["symptoms"])
                    + ". Acoes: "
                    + "; ".join(item["recommended_actions"])
                )
            else:
                content = item["text"]
            compiled.append(
                {
                    "doc_id": item["doc_id"],
                    "title": item.get("title", item.get("question", item.get("condition", item["doc_id"]))),
                    "category": item.get("category", "dataset"),
                    "content": content,
                    "source": item["source"],
                    "specialty": item.get("specialty", "saude_da_mulher"),
                    "document_type": item.get("document_type", "protocolo"),
                    "keywords": item.get("keywords", []),
                    "safety_tags": item.get("safety_tags", []),
                    "representativity_tags": item.get("representativity_tags", []),
                }
            )
    write_json(BASE_DIR / "synthetic_womens_health_knowledge.json", compiled)
    print("Datasets sinteticos gerados com sucesso.")


if __name__ == "__main__":
    main()
