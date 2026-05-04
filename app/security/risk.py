from __future__ import annotations


CRITICAL_TERMS = {
    "convulsao",
    "convulsões",
    "sangramento excessivo",
    "falta de ar",
    "ideias de autoagressão",
    "ferir o bebê",
    "risco imediato",
}

HIGH_RISK_TERMS = {
    "febre",
    "dor pélvica intensa",
    "dor abdominal forte",
    "sangramento",
    "cefaleia intensa",
    "visão embaçada",
    "visao embaçada",
    "movimentos fetais reduzidos",
    "medo do parceiro",
    "lesões frequentes",
}


def classify_risk(texts: list[str]) -> str:
    normalized = " | ".join(item.lower() for item in texts)
    if any(term in normalized for term in CRITICAL_TERMS):
        return "critical"
    if any(term in normalized for term in HIGH_RISK_TERMS):
        return "high"
    if normalized.strip():
        return "moderate"
    return "low"
