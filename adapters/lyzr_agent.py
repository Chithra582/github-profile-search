"""
Lyzr Agent Export Adapter for GitHub Profile Search Agent
Generated in compliance with OpenGAP spec v0.1.0
"""

import json
from typing import Any, Dict

def export_lyzr_agent() -> Dict[str, Any]:
    """Exports configuration for Lyzr Studio / Lyzr Agent API."""
    return {
        "agent_name": "github-profile-search",
        "agent_type": "developer_tools",
        "agent_role": "GitHub Profile & Repository Intelligence Copilot",
        "agent_description": "Autonomous GitHub intelligence agent for developer profile discovery, repository metrics analysis, and contribution telemetry with verifiable explainability.",
        "persona": {
            "tone": "concise, data-driven, objective",
            "values": ["empirical fact grounding", "rate-limit stewardship", "privacy-preserving"]
        },
        "features": [
            "User profile synthesis",
            "Repository ranking and velocity scoring",
            "Language breakdown percentage calculations"
        ],
        "export_target": "lyzr-agent-api",
        "spec_version": "0.1.0"
    }

if __name__ == "__main__":
    lyzr_config = export_lyzr_agent()
    print("[SUCCESS] Exported GitHub Profile Search for Lyzr:")
    print(json.dumps(lyzr_config, indent=2))

