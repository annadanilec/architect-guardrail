from pydantic import BaseModel
from pathlib import Path
import json
import os


DEFAULT_POLICY_PATH = Path(__file__).resolve().parent.parent / "policy" / "policy.json"

class Policy(BaseModel):
    approved_libraries: dict[str, list[str]] = {}
    forbidden_libraries: list[str] = []
    secrets_handling: str = "Use Vault / AWS Secrets Manager / Doppler. Never hardcode secrets."
    preferred_patterns: dict = {}
    adrs: dict = {}

def load_policy() -> Policy:
    policy_path = Path(os.environ.get("ARCHITECT_GUARDRAIL_POLICY_PATH", DEFAULT_POLICY_PATH))
    if not policy_path.exists():
        # Default policy
        return Policy()
    
    with open(policy_path) as f:
        data = json.load(f)
    return Policy(**data)
