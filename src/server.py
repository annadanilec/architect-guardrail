from mcp.server.fastmcp import FastMCP
from .config import load_policy
import sys

mcp = FastMCP("Architect-Guardrail")

# ==================== RESOURCES ====================

@mcp.resource("policy://tech-radar")
def get_tech_radar() -> str:
    """Returns current company Tech Radar"""
    policy = load_policy()
    return policy.model_dump_json(indent=2)

@mcp.resource("policy://security-rules")
def get_security_rules() -> str:
    """Core security policy"""
    policy = load_policy()
    return f"""Company Security Rules:
- Secrets: {policy.secrets_handling}
- Authentication: OAuth2 + short-lived JWT tokens
- Logging: Structured + PII masking
- Forbidden: Direct DB calls from backend services (use repository pattern)"""

# ==================== TOOLS ====================

@mcp.tool()
def get_approved_libraries(language: str = "python", category: str = None) -> str:
    """Get list of approved libraries"""
    policy = load_policy()
    libs = policy.approved_libraries.get(language, ["No data"])
    if category:
        return f"Approved {language} libraries ({category}): {libs}"
    return f"Approved {language} libraries: {libs}"


@mcp.tool()
def validate_against_policy(code_snippet: str, intent: str) -> dict:
    """Validate code snippet against company policy"""
    policy = load_policy()
    issues = []

    # Simple but effective checks
    forbidden = policy.forbidden_libraries + ["requests", "urllib3", "flask"]  # example

    for lib in forbidden:
        if lib in code_snippet.lower():
            issues.append({
                "severity": "high",
                "message": f"Library '{lib}' is not approved",
                "suggestion": "Use approved alternative from Tech Radar"
            })

    if any(x in code_snippet.lower() for x in ["api_key=", "password=", "secret="]):
        issues.append({
            "severity": "critical",
            "message": "Hardcoded secret detected",
            "suggestion": policy.secrets_handling
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "recommendation": "Follow company policy and Tech Radar" if issues else "Code looks compliant"
    }


def run_server():
    try:
        print("Starting Architect's Guardrail MCP Server...")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    run_server()
