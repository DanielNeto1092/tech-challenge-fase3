from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
PROMPTS_DIR = BASE_DIR / "prompts"
LOGS_DIR = BASE_DIR / "logs"
AUDIT_LOG_FILE = LOGS_DIR / "audit.log"
ACCESS_LOG_FILE = LOGS_DIR / "access.log"

DEMO_ACCESS_TOKENS = {
    "demo_clinician": "tc-fase3-demo-token",
    "demo_gineco": "tc-fase3-gineco-token",
    "demo_obstetrica": "tc-fase3-obstetrica-token",
}
